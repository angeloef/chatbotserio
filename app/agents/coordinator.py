"""Coordinator agent — classifies intent and delegates to specialists (Phase 8).

Uses regex-first + LLM-fallback hybrid classification, then routes
to the appropriate specialist with its own tool subset and system prompt.
"""

import re
from dataclasses import dataclass
from typing import Optional

from app.agents.llm_client import get_client
from app.agents.schemas import AgentResponse
from app.core.config import settings

# ── Specialist registry ──────────────────────────────────────

@dataclass
class Specialist:
    name: str
    description: str
    system_prompt: str
    tool_names: list[str]  # subset of available tools

SPECIALISTS: dict[str, Specialist] = {
    "search": Specialist(
        name="search",
        description="Property search, details, and images",
        system_prompt="""Eres el especialista en búsqueda de propiedades de ChatbotSerio.
Tu trabajo es buscar propiedades, mostrar detalles y fotos en Oberá.

Herramientas: search_properties, get_property_details, get_property_images

Reglas:
- SIEMPRE usá search_properties cuando el usuario quiera buscar con criterios NUEVOS.
- NUNCA vuelvas a buscar si el usuario hace una pregunta sobre resultados que YA mostraste (ej: "cuál tiene más ambientes", "cuál es el más barato"). Respondé analizando los resultados previos.
- Si el usuario confirma un ofrecimiento ("si porfavor", "dale, mostrame"), ejecutá la acción que ofreciste (detalles o fotos).
- Cuando pidan detalles o fotos, usá la herramienta correspondiente con el ID.
- Si no hay resultados, sugerí ajustar filtros.
- Respondé en español, sé conciso y profesional.""",
        tool_names=["search_properties", "get_property_details", "get_property_images"],
    ),
    "scheduling": Specialist(
        name="scheduling",
        description="Visit scheduling and calendar coordination",
        system_prompt="""Eres el especialista en agendamiento de visitas de ChatbotSerio.
Tu trabajo es coordinar visitas para ver propiedades.

Herramienta: schedule_visit

Reglas:
- Extraé TODA la información en un solo turno: propiedad, nombre, teléfono, día, horario.
- Si falta algún dato, preguntalo específicamente.
- Confirmá la visita con todos los datos antes de finalizar.
- Respondé en español, sé cálido y eficiente.""",
        tool_names=["schedule_visit"],
    ),
    "knowledge": Specialist(
        name="knowledge",
        description="FAQ, zone info, market data, requirements",
        system_prompt="""Eres el especialista en conocimiento inmobiliario de ChatbotSerio.
Tu trabajo es responder preguntas sobre alquiler, compra, requisitos, zonas y precios en Oberá.

Herramienta: get_faq_answer

Reglas:
- Usá get_faq_answer para consultas sobre requisitos, garantías, contratos, zonas, precios.
- Complementá con tu conocimiento de las 4 zonas (Centro, UNAM, Barrio Schuster, Ruta 14).
- Respondé en español, sé informativo y claro.""",
        tool_names=["get_faq_answer"],
    ),
    "rapport": Specialist(
        name="rapport",
        description="Greetings, small talk, tone management",
        system_prompt="""Eres el especialista en rapport de ChatbotSerio.
Tu trabajo es saludar, mantener una conversación amable y derivar al usuario
al especialista adecuado cuando tenga una necesidad concreta.

NO tenés herramientas. Solo conversación.

Reglas:
- Para saludos, respondé con calidez y preguntá en qué podés ayudar.
- Si el usuario expresa una necesidad concreta (buscar, agendar, preguntar),
  indicá que lo vas a derivar al especialista adecuado.
- Respondé en español, sé empático y cordial.""",
        tool_names=[],
    ),
    "negotiator": Specialist(
        name="negotiator",
        description="Price discussion, budget advice, negotiation",
        system_prompt="""Eres el especialista en negociación de ChatbotSerio.
Tu trabajo es ayudar con discusiones de precio y presupuesto.

Herramienta: search_properties (para consultar precios de referencia)

Reglas:
- Si el usuario dice que algo es caro, ofrecé alternativas más económicas.
- Consultá precios de referencia con search_properties.
- Sugerí ajustar criterios (zona más económica, menos dormitorios, etc.).
- Respondé en español, sé comprensivo y orientado a soluciones.""",
        tool_names=["search_properties"],
    ),
}


# ── Intent classification (regex-first, LLM-fallback) ─────────

INTENT_PATTERNS = [
    ("scheduling", r"\b(agendar|visita|coordinar|turno|cu[áa]ndo|horario|martes|miércoles|jueves|viernes|lunes|s[áa]bado|domingo)\b"),
    ("knowledge", r"\b(requisitos|garant[ií]a|contrato|zonas?|precios?|cu[áa]nto (cuesta|sale)|mascotas|contacto)\b"),
    ("negotiator", r"\b(muy caro|muy barato|cuesta mucho|presupuesto|no llego|se me va|rebaja|descuento|negoci|barato)\b"),
    ("rapport", r"\b(hola|chau|gracias|buenos d[ií]as|c[óo]mo (est[áa]s|andas)|ayuda|qu[ée] pod[ée]s hacer)\b"),
    ("search", r"\b(busco|quiero|necesito|buscando|alquilar|comprar|alquiler|venta|mostrame|detalles?|fotos?)\b"),
]


def classify_intent(message: str) -> str:
    """Classify user intent using regex-first approach.

    Returns the specialist name to delegate to.
    """
    msg = message.lower().strip()

    # Check each pattern category
    for intent, pattern in INTENT_PATTERNS:
        if re.search(pattern, msg):
            return intent

    # Default: search (most common action)
    return "search"


async def classify_intent_llm(message: str, context_prompt: str = "") -> str:
    """Use LLM for finer-grained intent classification (fallback)."""
    client = get_client()

    prompt = f"""Clasificá la intención del usuario en UNA de estas categorías:
- search: buscar propiedades, ver detalles o fotos
- scheduling: agendar una visita, coordinar horario
- knowledge: preguntar sobre requisitos, garantías, zonas, precios
- negotiator: discutir precios, decir que algo es caro/barato
- rapport: saludar, despedirse, charla casual

{context_prompt}

Mensaje del usuario: "{message}"

Respondé SOLO con una palabra: search, scheduling, knowledge, negotiator, o rapport."""

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_completion_tokens=10,
    )

    result = (response.choices[0].message.content or "search").strip().lower()
    if result in SPECIALISTS:
        return result
    return "search"


# ── Coordinator main entry ───────────────────────────────────

async def coordinate(
    message: str,
    session_id: str,
    context_prompt: str = "",
    use_agentic: bool = False,
) -> tuple[AgentResponse, str]:
    """Classify intent and delegate to the appropriate specialist.

    Args:
        use_agentic: If True, use the full Plan→Act→Observe→Evaluate loop.
    """
    # Fast classification
    intent = classify_intent(message)

    # For ambiguous cases, use LLM
    if intent in ("search",) and not _has_clear_signal(message):
        try:
            llm_intent = await classify_intent_llm(message, context_prompt)
            if llm_intent in SPECIALISTS:
                intent = llm_intent
        except Exception:
            pass

    specialist = SPECIALISTS.get(intent, SPECIALISTS["search"])

    if use_agentic:
        from app.agents.agentic_loop import run_agentic_loop
        result = await run_agentic_loop(
            message=message,
            session_id=session_id,
            context_prompt=context_prompt,
            belief_summary=context_prompt[:500] if context_prompt else "",
            available_tools=specialist.tool_names,
        )
    else:
        from app.agents.agent import process_message_with_specialist
        result = await process_message_with_specialist(
            message=message,
            session_id=session_id,
            context_prompt=context_prompt,
            specialist=specialist,
        )

    return result, specialist.name


def _has_clear_signal(message: str) -> bool:
    """Check if the message has a clear signal that doesn't need LLM re-classification."""
    msg = message.lower()
    return any(kw in msg for kw in [
        "busco", "quiero alquilar", "quiero comprar", "necesito",
        "mostrame", "detalles", "fotos", "agendar", "visita",
        "requisitos", "garantía", "hola", "chau",
    ])
