"""Dual router — S1 + Coordinator (multi-agent Phase 8)."""

import re
import time

from app.agents.schemas import AgentResponse, ChatResponse
from app.core.belief_state import ConversationBeliefState, get_belief
from app.core.context_aggregator import build_context_prompt
from app.core.state_transitioner import update_belief
from app.memory.working import save_working_memory, load_working_memory
from app.memory.episodic import build_greeting_from_episodes
from app.memory.user_model import build_personalized_context
from app.routers.system1 import format_response, match_pattern
from app.agents.agent import process_message, process_message_multistep
from app.agents.coordinator import coordinate
from app.agents.conversation_manager import (
    save_specialist_state,
    get_saved_state,
    clear_saved_state,
)

S1_CONFIDENCE_THRESHOLD = 0.70


def _clear_scheduling_state(belief: ConversationBeliefState) -> None:
    """Clear scheduling state after completion or escape."""
    belief.scheduling_name = ""
    belief.scheduling_phone = ""
    belief.scheduling_day = ""
    belief.scheduling_time = ""
    belief.scheduling_loop_count = 0
    belief.active_intents.discard("scheduling")


def _extract_property_data(belief, result_text: str) -> None:
    """Extract key property data lines from a get_property_details result."""
    import re
    lines = result_text.split("\n")
    key_lines = [l.strip() for l in lines if any(
        kw in l.lower() for kw in ["$", "córdoba", "san martín", "misiones", 
                                     "servicios", "electricidad", "agua", "gas", 
                                     "internet", "dormitorio", "m²"]
    )][:5]
    if key_lines:
        belief.last_property_data = " | ".join(key_lines)[:300]


async def _try_pre_llm_shortcut(
    belief: ConversationBeliefState, message: str, session_id: str, phone: str = ""
) -> tuple | None:
    """Try to handle the message deterministically without calling the LLM.
    
    Returns (ChatResponse, tools_called, confidence, router_label) or None.
    """
    import re
    from app.agents.schemas import MessageChunk
    from app.tools.get_property_details import get_property_details
    from app.tools.schedule_visit import schedule_visit
    
    msg_lower = message.lower().strip()
    
    # Case 1: Property resolved by description → show details immediately
    if "resolved_by_description" in (belief.active_intents or set()) and belief.selected_property_id:
        # Check if user is asking for something DIFFERENT (new criteria)
        msg_lower = message.lower().strip()
        new_search_kw = ["busca", "buscando", "estoy buscando", "tienen", "alguno", "algun", "otro", "otra", 
                         "diferente", "2 ambientes", "3 dormitorios", "habitacion",
                         "1 habitacion", "1 dormitorio", "2 dormitorios", "de 1", "de 2"]
        if any(kw in msg_lower for kw in new_search_kw):
            belief.active_intents.discard("resolved_by_description")
            belief.selected_property_id = None  # Prevent re-resolution
            belief.last_search_context = ""     # Clear context so state_transitioner can't re-match
            return None  # Let LLM handle the new search
        
        pid = belief.selected_property_id
        result_text = await get_property_details(property_id=pid)
        belief.last_tool_called = "get_property_details"
        belief.active_intents.discard("resolved_by_description")  # ONE-SHOT: clear after use
        # Extract key data for future cost questions
        _extract_property_data(belief, result_text)
        return (
            ChatResponse(
                response=result_text,
                tools_called=["get_property_details"],
                confidence=0.99,
            ),
            ["get_property_details"],
            0.99,
            "pre-llm::resolved",
        )
    
    # Case 1b: Photo request for currently selected property
    if belief.selected_property_id:
        photo_kw = ["fotos", "foto", "imagenes", "imágenes", "imagen", "mostrame fotos", "ver fotos"]
        if any(kw in msg_lower for kw in photo_kw):
            from app.tools.get_property_images import get_property_images
            result_text = await get_property_images(property_id=belief.selected_property_id)
            belief.last_tool_called = "get_property_images"
            return (
                ChatResponse(
                    response=result_text,
                    tools_called=["get_property_images"],
                    confidence=0.99,
                ),
                ["get_property_images"],
                0.99,
                "pre-llm::photos",
            )
    
    # Case 1c: Scheduling in progress — accumulate data from message
    if "scheduling" in (belief.active_intents or set()):
        msg_lower = message.lower().strip()
        
        # Don't intercept if this is the very first scheduling turn and no property selected yet.
        # Let the LLM run first to resolve property references.
        first_scheduling = not belief.selected_property_id and not belief.scheduling_name and not belief.scheduling_day and not belief.scheduling_time and belief.scheduling_loop_count == 0
        if first_scheduling:
            return None  # Let LLM handle first scheduling message
        
        # ── Loop count: increment BEFORE field extraction so Q&A sees updated count
        if belief.last_tool_called == "schedule_visit":
            belief.scheduling_loop_count += 1
        else:
            belief.scheduling_loop_count = 0
        
        # Auto-fill phone from request (WhatsApp webhook provides it)
        if phone and not belief.scheduling_phone:
            belief.scheduling_phone = phone
        
        # Detect property ID — also from "id N" patterns
        id_m = re.search(r"\b(?:id\s*#?\s*)?(\d+)\b", msg_lower)
        if id_m and not belief.selected_property_id:
            pid = int(id_m.group(1))
            if 1 <= pid <= 100:  # Sanity check: avoid capturing years/dates as IDs
                belief.selected_property_id = pid
        
        # Detect name — standard pattern with prefix
        name_m = re.search(r"\b(?:me llamo|mi nombre es|soy)\s+(.+?)(?:\s*(?:y|,|\.|$|puedo|quiero|mañana|tarde|\d))", msg_lower)
        if name_m and not belief.scheduling_name:
            belief.scheduling_name = name_m.group(1).strip().title()
        
        # Q&A name capture: if scheduling in progress and user replied with short text
        # that doesn't look like a question, property ID, or number
        if not belief.scheduling_name and belief.scheduling_loop_count >= 1:
            # Exclude messages that are property ID references
            looks_like_id = re.match(r"^\s*(?:id|nro|número|nº|numero|el|la|propiedad|#)?\s*\d+\s*$", msg_lower)
            not_a_question = not re.search(r"\b(busco|quiero|necesito|buscando|me interesa|agendar|visita|fotos|detalles|precio|cuanto|donde)\b", msg_lower)
            short_reply = len(msg_lower.split()) <= 3
            not_just_number = not re.match(r"^\d+$", msg_lower)
            if not looks_like_id and not_a_question and short_reply and not_just_number:
                belief.scheduling_name = message.strip().title()
        
        # Detect day
        day_m = re.search(r"\b(lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo|ma[nñ]ana|pasado)\b", msg_lower)
        if day_m and not belief.scheduling_day:
            belief.scheduling_day = day_m.group(1).strip()
        
        # Detect time
        time_m = re.search(r"\b(\d{1,2}[:h]\d{2}|\d{1,2}\s*(?:am|pm)|ma[nñ]ana|tarde|noche|atarde)\b", msg_lower)
        if time_m and not belief.scheduling_time:
            t = time_m.group(1).strip()
            if t == "atarde": t = "tarde"
            if t in ("mañana", "mañana") and belief.scheduling_day in ("mañana", "mañana"):
                rest = msg_lower[time_m.end():]
                time2 = re.search(r"\b(tarde|noche|atarde|\d{1,2}[:h]\d{2})\b", rest)
                if time2:
                    t = time2.group(1).strip()
                    if t == "atarde": t = "tarde"
                else:
                    t = ""
            if t:
                belief.scheduling_time = t
        
        # Show progress and ask for missing — natural language
        missing = []
        if not belief.selected_property_id:
            missing.append("el ID de la propiedad")
        if not belief.scheduling_name:
            missing.append("nombre")
        if not belief.scheduling_day:
            missing.append("día")
        if not belief.scheduling_time:
            missing.append("horario")
        if not belief.scheduling_phone and not phone:
            missing.append("teléfono")
        
        # Check if user is asking something unrelated to scheduling
        other_topics = re.search(
            r"\b(busco|quiero|necesito|buscando|me interesa|mostrame|pasame|listas?|propiedades|de nuevo|otra vez|buscar|volver)\b",
            msg_lower
        )
        if other_topics and belief.scheduling_loop_count >= 2:
            # User wants to change topic — exit scheduling gracefully
            _clear_scheduling_state(belief)
            return None  # Let LLM handle the new request
        
        # ── Infinite loop detection ────────────────────────────
        if belief.scheduling_loop_count >= 5:
            _clear_scheduling_state(belief)
            return (
                ChatResponse(
                    response=(
                        f"Disculpá, no pude completar el agendamiento. "
                        f"Si querés, escribime con todos los datos juntos: "
                        f"nombre, día, horario y el número de propiedad. "
                        f"También podés llamarnos al +54 9 3755 123456. "
                        f"¿Necesitás algo más mientras tanto?"
                    ),
                    tools_called=["schedule_visit"],
                    confidence=0.5,
                ),
                ["schedule_visit"], 0.5, "pre-llm::scheduling-escape",
            )
        
        if missing:
            # Natural language progress messages
            if len(missing) >= 3:
                # Many fields missing
                if "nombre" in missing and "día" in missing:
                    response_text = (
                        f"¡Dale! Para agendar la visita necesito algunos datos. "
                        f"¿Me decís tu nombre y qué día te queda cómodo?"
                    )
                else:
                    response_text = f"Genial. Para coordinar la visita necesito: {', '.join(missing)}. ¿Me los pasás?"
            elif "nombre" in missing:
                response_text = f"¡Perfecto! ¿Me decís tu nombre completo para agendar la visita?"
            elif "día" in missing:
                name_ref = f" {belief.scheduling_name}" if belief.scheduling_name else ""
                response_text = f"Gracias{name_ref}. ¿Qué día te queda cómodo para la visita?"
            elif "horario" in missing:
                response_text = f"¿A qué horario preferís? (mañana, tarde, o una hora específica)"
            elif "el ID de la propiedad" in missing:
                response_text = "¿Qué propiedad querés visitar? Decime el número que aparece entre corchetes."
            else:
                response_text = f"Falta: {missing[0]}. ¿Me lo decís?"
            
            belief.last_tool_called = "schedule_visit"
            return (
                ChatResponse(response=response_text, tools_called=["schedule_visit"], confidence=0.95),
                ["schedule_visit"], 0.95, "pre-llm::scheduling-progress",
            )
    
    # Case 2: Scheduling with all fields collected → call schedule_visit
    if (belief.scheduling_name and belief.scheduling_phone and 
        belief.scheduling_day and belief.scheduling_time):
        result_text = await schedule_visit(
            property_id=belief.selected_property_id or 0,
            nombre=belief.scheduling_name,
            telefono=belief.scheduling_phone,
            dia=belief.scheduling_day,
            horario=belief.scheduling_time,
        )
        belief.last_tool_called = "schedule_visit"
        _clear_scheduling_state(belief)  # Reset for next interaction
        return (
            ChatResponse(
                response=result_text,
                tools_called=["schedule_visit"],
                confidence=0.99,
            ),
            ["schedule_visit"],
            0.99,
            "pre-llm::scheduled",
        )
    
    # Case 3: Cost question with known property data → respond from memory
    if belief.selected_property_id and belief.last_property_data:
        cost_kw = ["cuanto", "cuánto", "precio", "cuesta", "sale", "servicios", 
                    "incluye", "entrar", "ingresar", "valor", "mensual"]
        if any(kw in msg_lower for kw in cost_kw):
            response_text = (
                f"Según los datos de la propiedad #{belief.selected_property_id} "
                f"que vimos: {belief.last_property_data}\n\n"
                "¿Querés que te busque info más específica sobre requisitos o forma de pago?"
            )
            return (
                ChatResponse(
                    response=response_text,
                    tools_called=[],
                    confidence=0.95,
                ),
                [],
                0.95,
                "pre-llm::cost-data",
            )
    
    return None


async def route_message(
    message: str, session_id: str, phone: str = ""
) -> tuple[ChatResponse, ConversationBeliefState, str, float]:
    """Route message through S1 → Coordinator with memory integration."""
    t0 = time.perf_counter()

    # ── Load belief state ─────────────────────────────────────
    belief = await load_working_memory(session_id)
    if belief is None:
        belief = get_belief(session_id)

    # ── Cross-session context ─────────────────────────────────
    cross_session_context = ""
    if phone and belief.turn_count == 0:
        greeting = await build_greeting_from_episodes(phone)
        if greeting:
            cross_session_context = greeting
        persona_ctx = await build_personalized_context(phone)
        if persona_ctx:
            cross_session_context += "\n\n" + persona_ctx

    belief = update_belief(belief, message)
    context_prompt = build_context_prompt(belief)
    if cross_session_context:
        context_prompt = cross_session_context + "\n\n" + context_prompt

    # ── Pre-LLM interception: when system deterministically knows what to do ──
    shortcut = await _try_pre_llm_shortcut(belief, message, session_id, phone)
    if shortcut:
        resp, tools, conf, router_label = shortcut
        latency = (time.perf_counter() - t0) * 1000
        await save_working_memory(belief)
        return (resp, belief, router_label, round(latency, 2))

    # ── System 1: regex match ─────────────────────────────────
    pattern = match_pattern(message)

    if pattern and pattern.confidence >= S1_CONFIDENCE_THRESHOLD:
        belief.last_tool_called = pattern.name

        if not pattern.needs_llm:
            # If greeting matched but message contains search keywords, delegate to S2
            if pattern.name.startswith("greeting"):
                search_kw = r"\b(busco|quiero|necesito|buscando|estoy buscando|me interesa|alquilar|alquiler|venta|comprar|departamento|depto|casa|ph|terreno)\b"
                msg_lower = message.lower().strip()
                if re.search(search_kw, msg_lower):
                    # Override context: tell LLM to process the full request, not just greet
                    override_context = (
                        "⚠️ El usuario combinó un saludo con una consulta de propiedades. "
                        "Ya lo saludaste — AHORA respondé a su consulta de búsqueda. "
                        "Si el usuario no especificó alquiler o venta, mostrale TODAS las propiedades "
                        "disponibles (tanto en alquiler como en venta). NO preguntes alquiler/compra "
                        "a menos que sea ambiguo — si dice 'departamento disponible', buscá todo.\n\n"
                    )
                    full_context = override_context + (context_prompt or "")
                    multistep_result = await process_message_multistep(message, session_id, full_context)
                    s2_result = multistep_result
                    latency = (time.perf_counter() - t0) * 1000
                    _update_belief_from_result(belief, s2_result)
                    await save_working_memory(belief)
                    return (
                        ChatResponse(
                            response=s2_result.response,
                            tools_called=s2_result.tools_called,
                            confidence=max(pattern.confidence, s2_result.confidence),
                            messages=s2_result.messages,
                        ),
                        belief, "s1→search", round(latency, 2),
                    )
            response_text = format_response(pattern, message)
            latency = (time.perf_counter() - t0) * 1000

            if pattern.name.startswith("greeting") and cross_session_context:
                parts = cross_session_context.split(".")
                greeting_part = parts[0].strip() + "."
                response_text = greeting_part + "\n\n" + response_text

            await save_working_memory(belief)
            return (
                ChatResponse(response=response_text, tools_called=[], confidence=pattern.confidence),
                belief, "s1", round(latency, 2),
            )
        else:
            # S1 identified intent → try multistep (falls back to normal agent if single tool)
            multistep_result = await process_message_multistep(message, session_id, context_prompt)
            s2_result = multistep_result
            specialist_name = "search"
            latency = (time.perf_counter() - t0) * 1000
            _update_belief_from_result(belief, s2_result)
            await save_working_memory(belief)
            return (
                ChatResponse(
                    response=s2_result.response,
                    tools_called=s2_result.tools_called,
                    confidence=max(pattern.confidence, s2_result.confidence),
                    messages=s2_result.messages,
                ),
                belief, f"s1→{specialist_name}", round(latency, 2),
            )

    # ── Coordinator: try multistep first (falls back to normal agent if single tool)
    multistep_result = await process_message_multistep(message, session_id, context_prompt)
    s2_result = multistep_result
    specialist_name = "search"
    latency = (time.perf_counter() - t0) * 1000
    _update_belief_from_result(belief, s2_result)
    await save_working_memory(belief)

    return (
        ChatResponse(
            response=s2_result.response,
            tools_called=s2_result.tools_called,
            confidence=s2_result.confidence,
            messages=s2_result.messages,
        ),
        belief, specialist_name, round(latency, 2),
    )


def _update_belief_from_result(belief: ConversationBeliefState, result: AgentResponse) -> None:
    import re
    if result.tools_called:
        belief.last_tool_called = result.tools_called[-1]
        
        # Extract selected_property_id from ALL tool calls
        for tr in result.raw_tool_results:
            args = tr.get("arguments", {})
            pid = args.get("property_id")
            if pid and isinstance(pid, (int, float)) and int(pid) > 0:
                belief.selected_property_id = int(pid)
                break  # First property_id found wins
        
        if "search_properties" in result.tools_called:
            for tr in result.raw_tool_results:
                if tr.get("name") == "search_properties":
                    result_text = str(tr.get("result", ""))
                    if "Encontré" in result_text:
                        m = re.search(r"Encontré (\d+)", result_text)
                        if m:
                            belief.last_search_count = int(m.group(1))
                    ids = re.findall(r"\[(\d+)\]", result_text)
                    belief.last_search_ids = [int(x) for x in ids]
                    # Build a rich lookup string including type, price, and TITLE
                    # Format: "  [1] Departamento en Centro — Alquiler $85,000/mes\n       1 dorm | 45m² | Depto 2 amb céntrico"
                    result_lines = result_text.split("\n")
                    summaries = []
                    for i, line in enumerate(result_lines):
                        m = re.match(r"\s*\[(\d+)\]\s+(.+?)\s+—\s+(.+?)$", line)
                        if m:
                            pid = m.group(1)
                            type_zone = m.group(2).strip()  # "Departamento en Centro"
                            price_info = m.group(3).strip()  # "Alquiler $85,000/mes"
                            # Peek at next line for the title
                            title = ""
                            if i + 1 < len(result_lines):
                                next_line = result_lines[i + 1].strip()
                                # Format: "1 dormitorio | 45m² | Depto 2 ambientes céntrico"
                                parts = next_line.split("|")
                                if len(parts) >= 3:
                                    title = parts[-1].strip()  # Last part is the title
                                else:
                                    title = next_line
                            summary = f"[{pid}] {type_zone} ({price_info})"
                            if title:
                                summary += f" — {title}"
                            summaries.append(summary)
                    if summaries:
                        belief.last_search_context = " | ".join(summaries)

        if "get_property_details" in result.tools_called:
            # Track that we showed details for this property (to avoid redundant re-show)
            belief.last_shown_detail_id = belief.selected_property_id
            # Extract property summary from the raw tool result for context injection
            for tr in result.raw_tool_results:
                if tr.get("name") == "get_property_details":
                    result_text = str(tr.get("result", ""))
                    # Extract key lines: price, address, services
                    lines = result_text.split("\n")
                    key_lines = [l.strip() for l in lines if any(
                        kw in l.lower() for kw in ["$", "córdoba", "san martín", "misiones", "servicios", "electricidad", "agua", "gas", "internet", "dormitorio", "m²"]
                    )][:5]
                    if key_lines:
                        belief.last_property_data = " | ".join(key_lines)[:300]

        if "schedule_visit" in result.tools_called:
            # Extract property ID from the response if not already set
            # LLM often says "la propiedad [7]" in scheduling context
            if not belief.selected_property_id:
                response_text = result.response.lower()
                prop_m = re.search(r"propiedad\s*(?:#|n[úu]mero|nro)?\s*\[?(\d+)\]?", response_text)
                if prop_m:
                    belief.selected_property_id = int(prop_m.group(1))
