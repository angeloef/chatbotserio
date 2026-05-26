# ChatbotSerio — Building Roadmap
## From Bare Skeleton to Full Agentic AI Chatbot

> **Project:** Greenfield build of InmuebleBot v2.0 architecture in isolated test environment
> **Location:** `C:\Users\angelo\Documents\alemai\ChatbotSerio`
> **Target:** Dockerized, locally testable, production-migratable
> **Architecture basis:** Imagine-v2.md (stratified autonomy, skill ecosystem, 4-tier memory, multi-agent)
> **LLM Model:** `gpt-5.4-mini` (OpenAI, released March 2026)

---

## LLM Strategy: gpt-5.4-mini

**Model version:** `gpt-5.4-mini` (snapshot `gpt-5.4-mini-2026-03-17` available for pinning)

### Key differences from legacy models (gpt-4o-mini, gpt-3.5-turbo)

| Parameter | Legacy | gpt-5.4-mini |
|-----------|--------|--------------|
| Token limit | `max_tokens` | `max_completion_tokens` |
| Reasoning effort | N/A | `reasoning.effort`: `"low"` / `"medium"` / `"high"` |
| Structured output | `response_format: {type: "json_object"}` | Full `json_schema` support with `strict: true` |
| Tool calling | Basic function calling | Parallel tool calls + structured tool output |
| Temperature default | 1.0 | 1.0 (same) |
| Context window | 128K | 256K tokens |

### ChatbotSerio-specific optimizations

1. **`max_completion_tokens` not `max_tokens`** — gpt-5.4+ rejects `max_tokens`. Fixed in `agent.py`.
2. **Reasoning effort = `"low"` for Phase 1** — Agent is simple tool dispatch, not complex reasoning. Saves latency + cost. Can escalate to `"medium"` in Phase 5+ when belief state gets complex.
3. **Temperature = 0.3** — Deterministic enough for tool routing, creative enough for natural conversation. This is already set.
4. **Future: `strict: true` structured output** — Phase 3+ should use `response_format` with `json_schema` + `strict: true` instead of prompt-engineering JSON. gpt-5.4-mini supports this natively.
5. **256K context** — Phase 7 (multi-tier memory) can hold entire conversation history + 4 tiers of memory in context without summarization for most sessions.

---

## Phase 0: Project Skeleton + Docker Foundation ✅ COMPLETED

**Goal:** Empty project that boots in Docker, responds to health checks, has database + Redis.

**Deliverables:**
```
ChatbotSerio/
  docker-compose.yml          # app + db + redis
  Dockerfile                  # Python 3.12, FastAPI
  requirements.txt            # fastapi, uvicorn, sqlalchemy, redis, openai, pydantic
  .env.example                # OPENAI_API_KEY, DB_URL, REDIS_URL
  app/
    __init__.py
    main.py                   # FastAPI app, /health, /health/ready
    core/
      __init__.py
      config.py               # Settings from env
      database.py             # SQLAlchemy async engine + session
    models/
      __init__.py
      base.py                 # DeclarativeBase
  tests/
    __init__.py
    test_health.py            # pytest: GET /health → 200
```

**Test criteria:**
```bash
# Boot everything
docker compose up -d

# Verify health
curl http://localhost:8000/health
# → {"status": "ok", "db": "connected", "redis": "connected"}

# Verify DB migration ran
docker compose exec db psql -U chatbotserio -c "\dt"
# → (empty, but connected)

# Tear down
docker compose down
```

**Done when:** `docker compose up -d` boots 3 services, `/health` returns 200 with DB+Redis connected.

---

## Phase 1: Bare Agent Loop — Single LLM + Tool Calling ✅ COMPLETED

**Goal:** Simplest possible agent: message in, LLM thinks, tool calls, response out. No router yet. No state machine yet. Just the core loop.

**Deliverables:**
```
app/
  agents/
    __init__.py
    agent.py                  # SimpleAgent: process_message() → response
    llm_client.py             # OpenAI chat completions wrapper
    schemas.py                # AgentResponse, ToolCall, StructuredToolCall
  tools/
    __init__.py
    registry.py               # Dict[str, Callable] — 2 tools: echo, get_time
    echo_tool.py
    time_tool.py
  api/
    __init__.py
    routes/
      __init__.py
      chat.py                 # POST /chat {message, session_id} → {response}
tests/
  test_agent.py               # Hello → greeting, "what time" → time tool
  test_tools.py               # Each tool returns expected output
```

**Test criteria:**
```bash
# Basic chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hola", "session_id": "test-1"}'
# → {"response": "¡Hola! ¿En qué puedo ayudarte?", "tools_called": []}

# Tool call
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "qué hora es", "session_id": "test-1"}'
# → {"response": "Son las 15:30.", "tools_called": ["get_time"]}

# Structured output verification
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "quiero buscar departamentos en Palermo", "session_id": "test-2"}'
# → response includes tool_call attempt to search_properties (even if it fails gracefully)
```

**Done when:** Agent responds to greetings, calls tools when appropriate, returns structured AgentResponse.

---

## Phase 2: Real Estate Domain — Property Search + Core Tools ✅ COMPLETED

**Goal:** Replace echo/time with real estate tools. Mimics InmuebleBot's core search flow but simpler.

**Deliverables:**
```
app/
  tools/
    search_properties.py      # Filters: operation, type, zone, budget, bedrooms
    get_property_details.py    # Returns full property info by ID
    get_property_images.py     # Returns image URLs by ID
    get_faq_answer.py          # Returns FAQ response by keyword
  models/
    property.py               # Property: id, title, location, price, bedrooms, etc.
    seed.py                    # Seed 20 test properties in Oberá (matching InmuebleBot's seed)
  db/
    migrations/                # Alembic: create properties table
scripts/
  seed_data.py                 # python scripts/seed_data.py → populates 20 properties
```

**Seed data:** Copy InmuebleBot's `scripts/seed_obera.py` pattern — 20 properties across Oberá zones (Centro, UNAM, Barrio Schuster, Ruta 14), mix of departamentos and casas, alquiler and venta.

**Test criteria:**
```bash
# Seed data
docker compose exec app python scripts/seed_data.py
# → "Seeded 20 properties in Oberá"

# Search flow
curl -X POST http://localhost:8000/chat \
  -d '{"message": "busco departamento en alquiler en Oberá hasta 100 lucas", "session_id": "t3"}'
# → Calls search_properties, returns list of matching properties

# Details flow
curl -X POST http://localhost:8000/chat \
  -d '{"message": "mostrame más del depto 3", "session_id": "t3"}'
# → Calls get_property_details(3), returns full description

# FAQ
curl -X POST http://localhost:8000/chat \
  -d '{"message": "qué necesito para alquilar", "session_id": "t4"}'
# → Calls get_faq_answer("requisitos"), returns requirements list
```

**Done when:** Agent searches properties, shows details, answers FAQs. Tool results are typed dataclasses.

---

## Phase 3: Structured Output + Progressive Escalation ✅ COMPLETED

**Goal:** Enforce JSON schema on LLM responses, add confidence-based escalation. This is the foundation of the stratified autonomy.

**Deliverables:**
```
app/
  agents/
    schemas.py                # Enhanced: AgentResponse with confidence field
    escalation.py             # ConfidenceGauge, EscalationDecider
  core/
    response_parser.py        # Parse LLM → AgentResponse, fallback handling
tests/
  test_structured_output.py   # All responses parse as valid AgentResponse JSON
  test_escalation.py          # Low confidence → clarification, very low → handoff
```

**Confidence thresholds:**
| Confidence | Action | Example |
|-----------|--------|---------|
| ≥ 0.95 | Execute autonomously | Greeting, confirmed tool call |
| 0.70–0.95 | Verify with user | "¿Entendí bien que querés buscar en Centro?" |
| 0.50–0.70 | Ask clarifying question | "¿Alquiler o compra?" |
| < 0.50 | Handoff / fallback | "No estoy seguro de entenderte. ¿Podrías decirlo de otra forma?" |

**Test criteria:**
```bash
# Structured output always valid
curl -X POST http://localhost:8000/chat -d '{"message": "hola", ...}'
# Response is ALWAYS valid AgentResponse JSON (never raw text)

# Clarification on low confidence
curl -X POST http://localhost:8000/chat -d '{"message": "quiero algo", ...}'
# → {"action": "ask_question", "confidence": 0.45, "message": "¿Alquiler o compra?"}

# Successful escalation
curl -X POST http://localhost:8000/chat -d '{"message": "alquiler", ...}'
# → {"action": "ask_question", "confidence": 0.72, "message": "¿En qué zona?"}
```

**Done when:** Every response is valid structured JSON. Confidence gates prevent bad tool calls.

---

## Phase 4: Dual-Router — System 1 (<1ms) + System 2 (LLM) ✅ COMPLETED

**Goal:** 80% of messages never hit the LLM. Regex trie catches greetings, confirmations, simple patterns. Only ambiguous/complex messages go to LLM.

**Deliverables:**
```
app/
  routers/
    __init__.py
    system1.py                # PatternMatcher, ResponseTemplate, EscalationGate
    system2.py                # LLM-based intent classifier
    patterns/
      greetings.py            # "hola", "buenos días", "cómo estás"
      confirmations.py        # "si", "dale", "bueno", "ok"
      faq_patterns.py         # "requisitos", "garantía", "contrato"
      search_patterns.py      # "busco", "quiero", "necesito" + operation/type/zone
      scheduling_patterns.py  # "agendar", "visitar", "cuándo"
      implicit_patterns.py    # "muy caro", "me queda lejos", "más grande"
  core/
    confidence.py             # ConfidenceScorer: score all patterns, return top match
tests/
  test_router.py              # 50 canned messages → verify S1/S2 routing
```

**System 1 patterns (regex + keyword scoring):**
```python
PATTERNS = [
    ("greeting", r"^(hola|buenos días|buenas tardes|buenas noches)[!.]?$", 0.98),
    ("confirm_yes", r"^(s[ií]|dale|bueno|ok|claro|obvio|por supuesto)", 0.95),
    ("faq_requisitos", r"(requisitos|necesito|garant[ií]a|recibo)", 0.90),
    ("search_with_criteria", r"(busco|quiero|necesito|buscando).{0,30}(depto|departamento|casa|ph|terreno)", 0.85),
    ("scheduling_intent", r"(agendar|visita|coordinar|cu[aá]ndo|horario)", 0.82),
    ("implicit_too_expensive", r"(muy caro|cuesta mucho|excede|presupuesto)", 0.75),
    ("implicit_too_far", r"(lejos|queda lejos|zona fea)", 0.72),
]
```

**Test criteria:**
```bash
# S1 handles greetings (no LLM call, <1ms)
curl -X POST http://localhost:8000/chat -d '{"message": "hola"}'
# → {"response": "...", "router": "s1", "latency_ms": <5}
# Verify in logs: "S1 routed | pattern=greeting | confidence=0.98 | 0.8ms"

# S1 catches implicit intent
curl -X POST http://localhost:8000/chat -d '{"message": "es muy caro"}'
# → {"router": "s1", "pattern": "implicit_too_expensive"} (no LLM call!)

# S2 handles ambiguity
curl -X POST http://localhost:8000/chat -d '{"message": "la zona es linda pero no sé si me conviene"}'
# → {"router": "s2", "latency_ms": ~200} (S1 confidence <0.70, escalated)
```

**Done when:** `grep "router=s1"` shows 80%+ of test messages routed by S1. S2 latency ~150-300ms.

---

## Phase 5: Dynamic Belief State — Beyond 15-State Enum ✅ COMPLETED

**Goal:** Replace rigid state machine with ConversationBeliefState vector. Context-aware guard functions instead of hardcoded transitions.

**Deliverables:**
```
app/
  core/
    belief_state.py           # ConversationBeliefState dataclass
    guard_functions.py        # 12 guard functions: can_search(), can_schedule(), etc.
    state_transitioner.py     # TransitionEngine: belief → capabilities
  agents/
    context_aggregator.py     # Builds LLM context from belief state
tests/
  test_belief_state.py        # State transitions, guard logic, context building
```

**Guard functions (12 total, replacing 168 transitions):**
```python
def can_search(belief: ConversationBeliefState) -> bool:
    """User has enough criteria OR is asking to search"""
    return (len(belief.search_criteria) >= 4 or 
            "searching" in belief.active_intents)

def can_schedule(belief: ConversationBeliefState) -> bool:
    """User has selected a property AND expressed scheduling intent"""
    return (belief.selected_property_id is not None and 
            "scheduling" in belief.active_intents)

def can_view_photos(belief: ConversationBeliefState) -> bool:
    """Property selected AND user wants visual info"""
    return (belief.selected_property_id is not None and 
            any(i in belief.active_intents for i in ["viewing", "photos"]))

# ... 9 more guards
```

**Test criteria:**
```bash
# Belief state evolves with conversation
# Turn 1: "busco depto alquiler Oberá centro" → belief.search_criteria = {tipo, op, zona}
#         guards: can_search=True, can_schedule=False

# Turn 2: "hasta 80 lucas" → belief.search_criteria adds budget
#         guards: can_search=True (4 criteria now)

# Turn 3: After search, user clicks "ID 5" → belief.selected_property_id = "5"
#         guards: can_view_photos=True, can_schedule=False

# Turn 4: "quiero agendar visita" → belief.active_intents adds "scheduling"
#         guards: can_schedule=True
```

**Done when:** Belief state correctly reflects conversation state at every turn. All 12 guards pass/fail as expected.

---

## Phase 6: SKILL.md Ecosystem + MCP ✅ COMPLETED

**Goal:** Convert tools to portable skills with progressive disclosure. Hot-reload skills without restarting. MCP server for external tools.

**Deliverables:**
```
skills/
  search_properties/
    SKILL.md                  # YAML frontmatter + 3-level progressive disclosure
    handler.py                # Actual implementation
    schema.py                 # Input/output Pydantic models
  schedule_visit/
    SKILL.md
    handler.py
    schema.py
  get_property_details/
    SKILL.md
    handler.py
    schema.py
  get_property_images/
    SKILL.md (+ handler, schema)
  get_faq_answer/
    SKILL.md (+ handler, schema)
  compare_properties/
    SKILL.md (+ handler, schema)
  
app/
  skills/
    __init__.py
    registry.py               # SkillRegistry: load, hot-reload, version, TTL
    loader.py                 # Parse SKILL.md → SkillDefinition
    composer.py               # Compose skills: find_similar + schedule
    mcp_server.py             # MCP JSON-RPC server exposing all skills
  core/
    progressive.py            # Progressive disclosure: select level based on context
tests/
  test_skills.py              # Load, execute, compose, hot-reload skills
  test_mcp.py                 # MCP JSON-RPC protocol compliance
```

**SKILL.md format (per Xu & Yan P11):**
```yaml
---
name: search_properties
version: 1.0.0
description: Search real estate properties by criteria
ttl: permanent
category: search
security: read_only
---

# search_properties

## Summary (Level 1 — ~120 tokens, always loaded)
Search properties by operation (rent/buy), type (apartment/house), zone,
budget range, and bedrooms. Returns ranked list with prices and key features.

## Instructions (Level 2 — ~2K tokens, loaded when skill is relevant)
[Full parameter docs, examples, edge cases, ranking logic]

## Implementation (Level 3 — full code, loaded on execution)
[handler.py reference]
```

**Test criteria:**
```bash
# Hot-reload: modify a SKILL.md while server is running
vim skills/search_properties/SKILL.md  # change description
curl -X POST http://localhost:8000/skills/reload
# → {"reloaded": ["search_properties"], "version": "1.0.1"}

# Progressive disclosure: only summary loaded for 80% of turns
# Context tokens: v1.x ~4000/skill × 13 = 52K → v2.0 ~120/skill × 13 summaries + 2000 × 2 active = ~5600

# MCP: list tools
curl -X POST http://localhost:8000/mcp -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
# → Returns all 6 skills as MCP tools
```

**Done when:** Skills load dynamically, hot-reload works, MCP interface exposes all tools.

---

## Phase 7: Multi-Tier Memory Architecture ✅ COMPLETED

**Goal:** Implement Zheng's 4-tier memory pyramid. Rich user personas. Cross-session awareness.

**Deliverables:**
```
app/
  memory/
    __init__.py
    working.py                # WorkingMemory: current conversation + active search
    episodic.py               # EpisodicMemory: past sessions, decisions, outcomes
    semantic.py               # SemanticMemory: zone knowledge, market data, FAQ cache
    procedural.py             # ProceduralMemory: skill execution history, what works
    user_model.py             # UserPersona: preferences, expertise, behavior patterns
    consolidation.py          # MemoryConsolidator: summarize → update → prune
    kgraph.py                 # KnowledgeGraph: Property↔Zone↔Amenity relationships
  models/
    user_episode.py           # UserEpisode ORM model
    zone.py                   # Zone + ZoneAmenity ORM models
tests/
  test_memory.py              # All 4 tiers read/write correctly
  test_persona.py             # Persona builds over multiple sessions
  test_consolidation.py       # Consolidation pipeline runs without errors
```

**Redis + PostgreSQL schema:**
```
Redis:
  working:{session_id}        # Current conversation state (TTL: 1h)
  episodic:{phone}            # Last 10 session summaries (TTL: 90d)
  persona:{phone}             # User persona (persistent)
  kgraph:zone:{name}          # Zone node (persistent)
  kgraph:amenity:{zone}       # Amenity set (persistent)

PostgreSQL:
  user_episodes               # Full session records (never pruned)
  zone_popularity             # Search/inquiry counts per zone
  search_failures             # Dead-end criteria combos (avoid suggesting)
  user_objections             # Pattern: what objections each user raises
```

**Test criteria:**
```bash
# Session 1: User searches, views, leaves
# Session 2: Same user returns — bot remembers
curl -X POST http://localhost:8000/chat \
  -d '{"message": "hola, sigo buscando", "session_id": "s2", "phone": "5491155550999"}'
# → "¡Bienvenido de nuevo! La última vez estabas buscando depto en alquiler en Centro
#    hasta $80k. ¿Seguís con ese presupuesto o lo ajustamos?"

# Memory consolidation (run after session ends)
curl -X POST http://localhost:8000/admin/consolidate -d '{"phone": "5491155550999"}'
# → {"consolidated": true, "episodes_updated": 1, "persona_updated": true}
```

**Done when:** Bot remembers users across sessions, persona builds over time, knowledge graph queries return zone↔amenity info.

---

## Phase 8: Multi-Agent Orchestration ✅ COMPLETED

**Goal:** Coordinator + 5 specialists. Natural conversation flow without rigid wizard.

**Deliverables:**
```
app/
  agents/
    coordinator.py            # CoordinatorAgent: understands user, delegates
    specialists/
      __init__.py
      search_specialist.py    # Property search + ranking
      scheduling_specialist.py # Calendar + availability (flexible slot-filling)
      knowledge_specialist.py  # FAQ, zone info, market data
      negotiator_specialist.py # Price discussion, offer handling
      rapport_specialist.py    # Tone, empathy, personality
    conversation_manager.py   # Interruption handling, topic switching
  core/
    proactive_engine.py       # Price drops, new listings, re-engagement
tests/
  test_multi_agent.py         # Coordinator routes to correct specialist
  test_scheduling_flow.py     # Flexible: "martes 11, Juan Pérez" → parsed in one turn
  test_interruption.py        # Mid-scheduling topic switch → save state → return
```

**Agent topology:**
```
User Message
    │
    ▼
┌─────────────────┐
│  Coordinator     │  "What does this user need?"
│  (System 2 LLM)  │  Delegates to specialists
└──────┬──────────┘
       │
   ┌───┼───────────┬──────────────┬──────────────┐
   ▼   ▼           ▼              ▼              ▼
┌────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐
│Srch│ │Sched   │ │Knowledge │ │Negotiator│ │Rapport │
│    │ │        │ │          │ │          │ │        │
└────┘ └────────┘ └──────────┘ └──────────┘ └────────┘
```

**Test criteria:**
```bash
# Flexible scheduling (no wizard!)
curl -X POST http://localhost:8000/chat \
  -d '{"message": "agendame para ver el depto 5 el martes a las 11, soy Juan"}'
# → Scheduling specialist parses ALL info in ONE turn
# → "✅ Listo Juan, martes 11:00 en [dirección depto 5]"

# Interruption handling
curl -X POST http://localhost:8000/chat \
  -d '{"message": "cuánto sale el de 3 ambientes?"}'  # mid-scheduling
# → Saves scheduling state, answers question
# → "¿Seguimos con el agendamiento? Me quedé en la hora."

# Proactive (triggered separately, not via /chat)
curl -X POST http://localhost:8000/admin/proactive/check -d '{"phone": "5491155550999"}'
# → {"alerts": [{"type": "price_drop", "property": "Depto 2 amb Centro", "old": 85000, "new": 78000}]}
```

**Done when:** Coordinator routes to correct specialist. Scheduling is flexible (any order). Interruptions save/restore state. Proactive alerts emerge from data changes.

---

## Phase 9: Agentic Loop — Plan→Act→Observe→Evaluate ✅ COMPLETED

**Goal:** Replace flat tool iteration with full agentic cycle. Hidden CoT thinking. Self-correction.

**Deliverables:**
```
app/
  agents/
    agentic_loop.py           # PlanActObserveEvaluate loop
    thinking.py               # THINKING state: internal CoT reasoning
    planner.py                 # ToolPlanner: sequence tools with dependencies
    observer.py                # ToolObserver: parse results, update belief
    evaluator.py               # LoopEvaluator: expected vs actual, replan if needed
tests/
  test_agentic_loop.py        # Plan→Act→Observe→Evaluate cycle
  test_replan.py               # Tool failure → replan mid-loop
  test_thinking.py             # Hidden CoT never reaches user
```

**The loop:**
```
User Message
    │
    ▼
[ROUTE] S1 (<1ms) or S2 (~150ms)
    │
    ▼
[THINK] Hidden CoT:
  • "User wants to find an apartment and schedule a visit"
  • "Missing: budget. Has: type=depto, op=alquiler, zone=centro"
  • "Plan: 1. Ask budget, 2. Search, 3. Show top 3, 4. Offer scheduling"
  • "Expected: User provides budget, sees 3+ matches, schedules"
    │
    ▼
[PLAN → ACT → OBSERVE → EVALUATE]
  PLAN:   tool_call("ask_clarification", question="¿Presupuesto?")
  ACT:    execute → returns "user said hasta 80k"
  OBSERVE: belief.criteria.budget = 80000
  EVALUATE: expected (got budget) ✓ → continue
  
  PLAN:   tool_call("search_properties", {criteria})
  ACT:    execute → returns 7 matches
  OBSERVE: belief.search_results = [7 matches]
  EVALUATE: expected (got matches) ✓ → continue
  
  PLAN:   tool_call("respond", text=format_properties(matches[:3]))
  ACT:    execute → response sent
  EVALUATE: expected ✓ → DONE
    │
    ▼
[REFLECTION] "Answered all intents? User asked to search, we searched."
[RESPOND] Format and deliver final response to user
```

**Test criteria:**
```bash
# Complex multi-step query
curl -X POST http://localhost:8000/chat \
  -d '{"message": "busco depto alquiler centro hasta 80k y si hay algo lindo quiero agendar"}'
# → Agent plans: [clarify_budget?no(user said 80k)] → [search] → [show] → [offer_scheduling]
# → Internal log shows: PLAN (3 steps) → ACT (3 tool calls) → EVALUATE (all ✓) → RESPOND

# Self-correction on tool failure
curl -X POST http://localhost:8000/chat \
  -d '{"message": "busco en XyzAbc123"}'
# → search_properties("XyzAbc123") → 0 results
# → EVALUATE: expected >0 results, got 0 → REPLAN
# → THINK: "Zone might not exist. Try fuzzy match or ask user."
# → PLAN: tool_call("respond", "No encontré 'XyzAbc123'. ¿Quisiste decir otra zona?")
```

**Done when:** Agent plans multi-step tasks, self-corrects on failures, THINKING state never leaks to user.

---

## Phase 10: Natural Language Quality + Argentine Spanish ✅ COMPLETED

**Goal:** Polished conversation. Context-aware formality. Empathy. Domain-appropriate Spanish.

**Deliverables:**
```
app/
  nlp/
    __init__.py
    formality.py              # Context-aware formality: casual → formal based on user
    empathy.py                # Sentiment detection + adaptive tone
    coherence.py              # Multi-turn coherence checker
    argentine_spanish.py      # Regional vocabulary, common phrases, real estate terms
    response_templates.py     # Template library with variants
  prompts/
    personality.py            # Core personality prompt (adapted from InmuebleBot)
    state_prompts.py           # Per-state/system prompt templates
tests/
  test_nl_quality.py          # Responses are natural, appropriate tone
  test_argentine_terms.py     # "depto" not "apartamento", "alquiler" not "renta"
```

**Key adaptations:**
```python
# Formality levels
FORMALITY_LEVELS = {
    "formal":    "usted, quisiera, podría, por favor, agradezco",
    "neutral":   "vos, querés, podés, gracias",
    "casual":    "che, dale, joya, genial, buenísimo",
}

# Empathy states
EMPATHY_RESPONSES = {
    "frustrated": "Entiendo, disculpá la confusión. Voy a ser más claro.",
    "excited":    "¡Qué bueno! Me alegra que te haya gustado.",
    "uncertain":  "Tomate tu tiempo, no hay apuro. Cuando quieras, seguimos.",
    "rushed":     "Dale, voy rápido. ¿Preferís que te mande un resumen?",
}
```

**Test criteria:**
```bash
# Argentine vocabulary
curl ... -d '{"message": "busco un depto en alquiler"}'
# → Uses "depto", "alquiler", "ambientes" (not "departamento", "renta", "habitaciones")

# Empathy detection
curl ... -d '{"message": "ya te dije tres veces que busco en centro!"}'
# → Detects frustration → "Entiendo, disculpá. Voy directo: departamentos en Centro, ¿algún presupuesto?"

# Multi-turn coherence
# Turn 5 of a long conversation — bot still remembers Turn 1's context
curl ... -d '{"message": "y el tercero?"}'  # (referring to 3rd search result from Turn 3)
# → "El tercero es un depto de 3 ambientes en Barrio Schuster a $73,664/mes."
```

**Done when:** Responses sound natural to Argentine Spanish speakers. Bot adapts tone to emotional state. Multi-turn references resolved correctly.

---

## Phase 11: Observability + Testing Infrastructure ✅ COMPLETED

**Goal:** Tracing, logging, monitoring. Conversation test suite. A/B testing framework.

**Deliverables:**
```
app/
  core/
    tracing.py                # Span-based tracing: every decision logged
    metrics.py                 # Latency histograms, routing stats, error rates
    ab_testing.py              # A/B test config, variant assignment, results
  api/
    routes/
      admin.py                 # /admin/stats, /admin/traces, /admin/ab-tests
      simulate.py              # POST /simulate {message, phone} → response (no WhatsApp)
tests/
  conversation_tests/
    test_scenarios.json        # 30 canned scenarios
    runner.py                  # Run all → report pass/fail
    fixtures/
      search.json              # Search-specific scenarios
      scheduling.json           # Scheduling-specific
      multi_intent.json         # Compound message scenarios
      edge_cases.json           # Ambiguous, error, handoff scenarios
```

**Test criteria:**
```bash
# Run full test suite
docker compose exec app python -m pytest tests/ -v
# → 120+ tests pass

# Run conversation scenarios
docker compose exec app python tests/conversation_tests/runner.py
# → 30/30 scenarios pass

# Tracing
curl http://localhost:8000/admin/traces/latest
# → Shows full trace of last conversation: route→think→plan→act×3→respond

# A/B test
curl -X POST http://localhost:8000/admin/ab-tests \
  -d '{"name": "greeting_formality", "variants": ["casual", "formal"]}'
curl http://localhost:8000/admin/ab-tests/greeting_formality/results
# → {"casual": {"count": 45, "engagement": 0.82}, "formal": {"count": 43, "engagement": 0.71}}
```

**Done when:** Full test suite passes. Every conversation turn is traceable. A/B testing framework works.

---

## Phase 12: Production Hardening + Migration Path

**Goal:** Make ChatbotSerio production-ready. Document migration path to InmuebleBot.

**Deliverables:**
```
  docker-compose.prod.yml     # Production overrides (no debug, health checks, resource limits)
  Dockerfile.prod              # Multi-stage build, slim image
  alembic.ini                  # Migration config
  alembic/
    versions/                  # All migration scripts
  MIGRATION_GUIDE.md           # How to migrate from ChatbotSerio → InmuebleBot production
  docs/
    architecture.md            # System architecture diagram
    api.md                     # API reference
    skills.md                  # How to add a new skill
    deployment.md              # Render / Docker deployment guide
```

**Migration checklist (ChatbotSerio → InmuebleBot):**
```
□ Skills are portable: copy skills/* to inmueblebot/skills/
□ MCP server compatible with InmuebleBot's webhook path
□ Memory schema matches: same Redis keys, same PG tables
□ LLM client compatible: same model-agnostic router (gpt-5.x vs gpt-4.x)
□ Tool gating maps: ChatbotSerio guards → InmuebleBot state machine
□ Conversation format identical: same AgentResponse schema
□ Seed data matches: same property set, same zones
□ Docker compose overrides: add InmuebleBot-specific services
```

**Test criteria:**
```bash
# Production build
docker compose -f docker-compose.prod.yml up -d
# → All services healthy, no debug endpoints exposed

# Load test
# 100 concurrent messages → <2s p95 latency
# No memory leaks >24h uptime

# Migration test
# ChatbotSerio skill → copy to inmueblebot → works identically
```

**Done when:** Production Docker config works. Migration guide is complete. Load test passes.

---

## Quick Reference: Test After Every Phase

```bash
# After ANY phase, verify with:
docker compose up -d                    # Boot
curl http://localhost:8000/health       # Health check
docker compose exec app pytest tests/   # Test suite
docker compose down                     # Cleanup
```

## Phase Dependency Graph

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4
                                                 │
                                            ┌────┴────┐
                                            ▼         ▼
                                        Phase 5   Phase 6
                                            │         │
                                            └────┬────┘
                                                 ▼
                                              Phase 7
                                                 │
                                            ┌────┴────┐
                                            ▼         ▼
                                        Phase 8   Phase 9
                                            │         │
                                            └────┬────┘
                                                 ▼
                                             Phase 10
                                                 │
                                                 ▼
                                             Phase 11
                                                 │
                                                 ▼
                                             Phase 12
```

Phases 5+6, 8+9 can partially overlap (different teams/files). Phases 10-12 are sequential (need all prior phases complete).

---

## Token Budget (Estimated)

| Phase | New Files | LOC | Complexity | Test Scenarios |
|-------|-----------|-----|------------|----------------|
| 0 | 8 | ~150 | Low | 2 |
| 1 | 8 | ~400 | Low | 5 |
| 2 | 6 | ~500 | Medium | 8 |
| 3 | 4 | ~300 | Medium | 6 |
| 4 | 8 | ~600 | Medium-High | 12 |
| 5 | 4 | ~400 | Medium | 8 |
| 6 | 15 | ~1200 | High | 15 |
| 7 | 10 | ~900 | High | 12 |
| 8 | 8 | ~800 | High | 15 |
| 9 | 5 | ~500 | High | 10 |
| 10 | 7 | ~600 | Medium | 10 |
| 11 | 8 | ~700 | Medium | 15 |
| 12 | 6 | ~300 | Low-Medium | 5 |
| **Total** | **~100** | **~7,350** | | **~123** |

---

*Roadmap designed for sequential, testable implementation. Each phase produces a working system. Start at Phase 0. Ship after Phase 12.*
