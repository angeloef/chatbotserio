# Graph Report - ChatbotSerio  (2026-05-27)

## Corpus Check
- 96 files · ~35,383 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1124 nodes · 1654 edges · 99 communities (76 shown, 23 thin omitted)
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 499 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `11be2705`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]

## God Nodes (most connected - your core abstractions)
1. `ConversationBeliefState` - 61 edges
2. `s1_handles()` - 33 edges
3. `StructuredToolCall` - 23 edges
4. `route_message()` - 22 edges
5. `Observation` - 20 edges
6. `update_belief()` - 20 edges
7. `run_agentic_loop()` - 19 edges
8. `s1_delegates()` - 19 edges
9. `ChatbotSerio — Building Roadmap` - 19 edges
10. `classify_intent()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `TestConsolidateSession` --uses--> `ConversationBeliefState`  [INFERRED]
  tests/test_consolidation.py → app/core/belief_state.py
- `TestWorkingMemory` --uses--> `ConversationBeliefState`  [INFERRED]
  tests/test_memory.py → app/core/belief_state.py
- `TestEpisodicMemory` --uses--> `ConversationBeliefState`  [INFERRED]
  tests/test_memory.py → app/core/belief_state.py
- `TestSemanticMemory` --uses--> `ConversationBeliefState`  [INFERRED]
  tests/test_memory.py → app/core/belief_state.py
- `TestProceduralMemory` --uses--> `ConversationBeliefState`  [INFERRED]
  tests/test_memory.py → app/core/belief_state.py

## Communities (99 total, 23 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (5): Does S1 match AND handle (not delegate) this message?, s1_handles(), TestFAQ, TestGreetings, TestImplicitFeedback

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (36): build_replan_context(), _build_success_summary(), evaluate(), Evaluation, LoopEvaluator — expected vs actual, replan logic (Phase 9).  After executing the, Build a replan hint for the LLM context.      This tells the LLM what to do diff, Result of evaluating an execution plan., Evaluate whether the plan achieved its goals.      Replanning triggers:     - Se (+28 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (46): get_user_memory(), Get all memory tiers for a user (debug/diagnostic)., build_greeting_from_episodes(), get_episodes(), get_last_episode(), _get_redis(), EpisodicMemory — past session summaries for cross-session recall.  Redis: episod, Build a personalized greeting based on past episodes.      Returns empty string (+38 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (24): _error(), _execute_skill_tool(), handle_mcp_request(), handle_mcp_request_raw(), MCPResponse, MCP (Model Context Protocol) JSON-RPC 2.0 server.  Exposes all registered skills, JSON-RPC 2.0 response., Handle a JSON-RPC 2.0 MCP request.      Supported methods:     - initialize: MCP (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (30): _clear_scheduling_state(), _extract_property_data(), Dual router — S1 + Coordinator (multi-agent Phase 8)., Route message through S1 → Coordinator with memory integration., Route message through S1 → Coordinator with memory integration., Extract key property data lines from a get_property_details result., Clear scheduling state after completion or escape., Route message through S1 → Coordinator with memory integration. (+22 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (34): consolidate_session(), Run memory consolidation after a session ends.      Saves episode summary, updat, clear_session(), get_belief(), ConversationBeliefState — dynamic multi-turn state tracking (Phase 5).  Replaces, Get or create a belief state for a session., Get or create a belief state for a session., Persist belief state to the store. (+26 more)

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (9): adjust_tone(), detect_emotion(), EmotionalState, get_empathetic_prefix(), Empathy detection — sentiment analysis + adaptive tone (Phase 10).  Detects emot, Adjust response tone based on detected emotion.      If emotion is frustrated: b, Detect the user's emotional state from their message.      Returns the strongest, Get an empathetic response prefix based on detected emotion. (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (21): ConsolidateRequest, health_ready(), lifespan(), mcp_endpoint(), _ping_redis(), proactive_check(), FastAPI application entry point — ChatbotSerio., Check for proactive alerts across all zones. (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (24): consolidate_session(), MemoryConsolidator — summarize session → update memory → prune (Phase 7).  Runs, Run the full memory consolidation pipeline after a session.      Args:         b, Generate a compact summary of the session., _summarize_session(), build_personalized_context(), get_persona(), _get_redis() (+16 more)

### Community 9 - "Community 9"
Cohesion: 0.1
Nodes (6): classify_intent(), Classify user intent using regex-first approach.      Returns the specialist nam, Tests for coordinator intent classification and specialist routing., TestIntentClassification, TestIntentPatterns, TestSpecialists

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (10): assess_confidence(), build_clarification_message(), EscalationLevel, Confidence-based escalation system (Phase 3).  Implements the stratified autonom, Clamp and classify confidence into an escalation level.      Returns (level, cla, Modify or replace the response based on the escalation level.      - EXECUTE: pa, Enum, Tests for escalation module — confidence thresholds and clarification messages. (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (17): build_interruption_prompt(), clear_saved_state(), ConversationSnapshot, detect_topic_switch(), get_saved_state(), Conversation manager — handles topic switching and state save/restore (Phase 8)., Saved state when a conversation is interrupted., Save the current specialist context before switching topics. (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.24
Nodes (7): ConversationBeliefState, Accumulated conversation state across multiple turns.      Updated each turn via, Extract entities from message and accumulate into belief state.      Criteria ar, Extract entities from message and accumulate into belief state.      Criteria ar, update_belief(), First extracted value for a field should persist., TestStateTransitioner

### Community 13 - "Community 13"
Cohesion: 0.17
Nodes (14): _format_tool_result_for_user(), process_message(), process_message_multistep(), process_message_with_specialist(), SimpleAgent — LLM + tool calling + structured output + escalation (Phase 3)., Format a raw tool result into user-friendly text.      For get_property_details, Process a message that may require multiple tool calls, emitting each result as, Process a message through a specialist agent with filtered tools.      Args: (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (16): AgentResponse, ChatRequest, ChatResponse, MessageChunk, Agent response and tool call schemas., Structured response from the agent after processing a message., A single message bubble in a multi-message response sequence., Incoming chat request. (+8 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (18): Base, DeclarativeBase, Base, SQLAlchemy declarative base., Base class for all ORM models., Property, Property model — matches InmuebleBot Oberá seed pattern., Real estate property in Oberá. (+10 more)

### Community 16 - "Community 16"
Cohesion: 0.13
Nodes (9): parse_llm_response(), Parse LLM responses into structured output (Phase 3).  Handles gpt-5.4-mini's js, Extract respuesta and confianza with type coercion., Parse the LLM's response into (text, confidence).      Tries multiple strategies, _safe_extract(), Tests for response parser — JSON extraction and fallback handling., Parser should extract the JSON even with surrounding text., Verify the json_schema dict has the required structure. (+1 more)

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (21): Agent, Api, Architecture, Chatbot, Database, Docker, Inmueble, Memory (+13 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (17): check_response_quality(), enrich_with_argentinisms(), get_preferred_term(), is_argentine_term(), Argentine Spanish vocabulary and regional adaptations (Phase 10).  Maps generic, Replace generic terms with Argentine equivalents where possible., Check if a word is in the Argentine vocabulary., Get the preferred Argentine term for a generic word. (+9 more)

### Community 19 - "Community 19"
Cohesion: 0.1
Nodes (14): can_schedule(), can_search(), can_search_with_partial(), can_view_details(), needs_clarify_operation(), User has enough criteria OR explicitly asking to search., User has at least 2 criteria — enough for a broad search., A property is selected, can show details. (+6 more)

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (15): can_ask_faq(), can_confirm(), can_greet(), can_view_photos(), needs_clarify_budget(), needs_clarify_type(), needs_clarify_zone(), Guard functions — 12 boolean predicates on ConversationBeliefState.  Replace 168 (+7 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (6): Does S1 match but delegate to S2?, s1_delegates(), TestConfirmations, TestDetailsDelegation, TestSchedulingDelegation, TestSearchDelegation

### Community 22 - "Community 22"
Cohesion: 0.17
Nodes (10): get_active_skills_summary(), get_context_tokens(), Progressive disclosure — selects skill detail level based on context.  Level 1 (, Estimate token cost for loading skills at a given level.      Args:         skil, Token count for a skill at a given level., Decide which disclosure level to use.      Default: Level 1 (summary only) — for, Build a compact summary of all skills for the system prompt.      This is the Le, select_level() (+2 more)

### Community 23 - "Community 23"
Cohesion: 0.16
Nodes (11): build_context_prompt(), detect_clarification_loop(), _get_missing_criteria(), Context aggregator — builds enriched LLM system prompt from belief state.  Injec, Detect if we're stuck in a clarification loop (re-asking same questions).     Re, Return list of missing search criteria names., Return list of missing search criteria names., Return list of missing search criteria names. (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.22
Nodes (13): A structured tool call from the LLM (OpenAI format)., StructuredToolCall, Tests for real estate tools — search, details, images, FAQ., test_execute_faq(), TestToolExecution, Tests for the tool registry and individual tools., test_execute_bad_arguments(), test_execute_echo() (+5 more)

### Community 25 - "Community 25"
Cohesion: 0.21
Nodes (5): Central registry for all loaded skills.      Supports hot-reload: detect changed, Return all skills as MCP tool definitions., Get OpenAI tool schemas with progressive disclosure.          Args:, SkillRegistry, TestSkillRegistry

### Community 26 - "Community 26"
Cohesion: 0.2
Nodes (5): TestToolsRegistry, TestToolSchemas, get_tools_schema(), Tool registry — maps tool names to callables and provides OpenAI tool schemas., Return the OpenAI tool schemas for all registered tools.

### Community 27 - "Community 27"
Cohesion: 0.23
Nodes (6): find_similar_skills(), Skill composer — chains skills for compound workflows.  Examples: - search_prope, Suggest logical next skills after executing the current one.      Args:, Find skills whose descriptions match a query string.      Uses Spanish keyword a, suggest_next_skills(), TestComposer

### Community 28 - "Community 28"
Cohesion: 0.21
Nodes (6): load_skill(), Parse a SKILL.md file into a SkillDefinition.      Expected format:     ---, Check for modified SKILL.md files and reload them.          Returns:, Tests for skill ecosystem — loader, registry, progressive, composer., Summary should be compact (~120 tokens target)., TestLoader

### Community 29 - "Community 29"
Cohesion: 0.24
Nodes (6): extract_scheduling_info(), Tests for flexible scheduling flow — parsed in ONE turn., agendame para ver el depto 5 el martes a las 11, soy Juan, Verify all extraction methods work on a variety of messages., Extract scheduling details from a free-form message., TestSchedulingExtraction

### Community 30 - "Community 30"
Cohesion: 0.2
Nodes (6): Hidden CoT reasoning — internal thought process never shown to user (Phase 9)., Extract a one-line summary of the thinking for logging., summarize_thinking(), Tests for hidden CoT thinking — must NEVER reach the user., Verify that think() is properly defined as an async function returning str., TestThinkingModule

### Community 31 - "Community 31"
Cohesion: 0.05
Nodes (48): clear_logs(), ensure_log_dir(), get_session_logs(), log_turn(), Conversation logger — records every turn to a JSONL file for debugging., Clear the log file. Returns number of entries removed., Create the log directory if it doesn't exist., Log a single conversation turn to the JSONL file.      Returns the logged entry (+40 more)

### Community 32 - "Community 32"
Cohesion: 0.39
Nodes (3): _classify_outcome(), Classify the session outcome based on state., TestClassifyOutcome

### Community 33 - "Community 33"
Cohesion: 0.16
Nodes (12): format_response(), match_pattern(), System 1 router — sub-millisecond regex/keyword pattern matching.  Goal: 80% of, A single S1 routing pattern., A single S1 routing pattern., Find the best-matching S1 pattern for a message.      Returns the highest-confid, Find the best-matching S1 pattern for a message.      Returns the highest-confid, Format the pattern's response template.      Handles {0}, {1} substitutions from (+4 more)

### Community 34 - "Community 34"
Cohesion: 0.17
Nodes (8): Tests for System 1 + System 2 dual router.  Verifies: - S1 catches greetings, co, Does S1 match this message (at any confidence tier)?, Verify 80%+ S1 routing on the 50 test messages., At least 80% of messages should be handled by S1 (handle + delegate)., Print detailed coverage breakdown., s1_matches(), TestCoverage, TestS2Fallback

### Community 35 - "Community 35"
Cohesion: 0.22
Nodes (5): _run_faq(), TestFAQ, get_faq_answer(), FAQ tool — answers common real estate questions by keyword., Answer frequently asked questions about real estate in Oberá.      Args:

### Community 36 - "Community 36"
Cohesion: 0.2
Nodes (6): _extract_section(), load_all_skills(), SKILL.md loader — parses YAML frontmatter + markdown body into SkillDefinition., Extract a markdown section by ## heading name.      Matches headings like '## Su, Load all SKILL.md files from a directory tree., Load all SKILL.md files from the skills directory.

### Community 37 - "Community 37"
Cohesion: 0.2
Nodes (7): list_skills(), List all loaded skills with metadata., Hot-reload all skills from SKILL.md files., reload_skills(), get_skill_registry(), Skill registry — manages loaded skills, hot-reload, and tool schema generation., Get or create the global skill registry.

### Community 38 - "Community 38"
Cohesion: 0.28
Nodes (8): classify_intent_llm(), coordinate(), _has_clear_signal(), Coordinator agent — classifies intent and delegates to specialists (Phase 8).  U, Use LLM for finer-grained intent classification (fallback)., Classify intent and delegate to the appropriate specialist.      Args:         u, Check if the message has a clear signal that doesn't need LLM re-classification., Specialist

### Community 39 - "Community 39"
Cohesion: 0.22
Nodes (8): code:block1 (| Prop A     | Prop B     | Prop C), compare_properties, Edge cases, Formato, Implementation (Level 3), Instructions (Level 2), Parámetros, Summary (Level 1)

### Community 40 - "Community 40"
Cohesion: 0.25
Nodes (7): Tests for health and readiness endpoints., Health endpoint returns 200 and ok status., Ready endpoint returns valid structure., OpenAPI docs are accessible., test_app_title(), test_health_ok(), test_health_ready_structure()

### Community 41 - "Community 41"
Cohesion: 0.29
Nodes (4): TestEchoTool, echo(), Echo tool — repeats a message back., Repeat the given text back to the user.      If no text is provided, returns a d

### Community 42 - "Community 42"
Cohesion: 0.29
Nodes (4): TestTimeTool, get_time(), Get current time tool., Return the current date and time in Argentina timezone (UTC-3).

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (8): code:block1 (🏠 Título), Edge cases, Formato de respuesta, get_property_details, Implementation (Level 3), Instructions (Level 2), Parámetros, Summary (Level 1 — ~120 tokens)

### Community 44 - "Community 44"
Cohesion: 0.33
Nodes (4): BaseSettings, Application settings from environment variables., ChatbotSerio configuration loaded from environment., Settings

### Community 45 - "Community 45"
Cohesion: 0.33
Nodes (5): build_coherence_context(), check_coherence(), Multi-turn coherence checker (Phase 10).  Ensures responses reference prior conv, Check if a response is coherent with the conversation history.      Returns:, Build a coherence hint for the LLM to maintain multi-turn consistency.      Incl

### Community 46 - "Community 46"
Cohesion: 0.22
Nodes (8): Comportamiento, Edge cases, Ejemplos, Implementation (Level 3 — loaded on execution), Instructions (Level 2 — ~2K tokens, loaded when skill is relevant), Parámetros, search_properties, Summary (Level 1 — ~120 tokens, always loaded)

### Community 47 - "Community 47"
Cohesion: 0.5
Nodes (3): System 2 router — delegates to the existing LLM agent loop (Phase 5).  Now accep, Forward to the full LLM agent loop with optional belief context.      The contex, route_s2()

### Community 48 - "Community 48"
Cohesion: 0.25
Nodes (7): _fuzzy_normalize(), _parse_bedrooms(), _parse_budget(), State transitioner — extracts entities from messages and updates belief state., Extract minimum bedrooms from text., Normalize common typos and merged words for regex matching.      Handles:     -, Extract a budget amount from text. Returns None if no budget found.

### Community 49 - "Community 49"
Cohesion: 0.5
Nodes (3): Parsed representation of a SKILL.md file., Convert to MCP tool definition., SkillDefinition

### Community 72 - "Community 72"
Cohesion: 0.25
Nodes (7): ChatbotSerio — Building Roadmap, code:bash (# After ANY phase, verify with:), code:block36 (Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4), From Bare Skeleton to Full Agentic AI Chatbot, Phase Dependency Graph, Quick Reference: Test After Every Phase, Token Budget (Estimated)

### Community 73 - "Community 73"
Cohesion: 0.25
Nodes (7): Edge cases, get_faq_answer, Implementation (Level 3), Instructions (Level 2), Parámetros, Summary (Level 1), Temas cubiertos

### Community 74 - "Community 74"
Cohesion: 0.25
Nodes (7): Comportamiento, Ejemplo, Implementation (Level 3), Instructions (Level 2), Parámetros, schedule_visit, Summary (Level 1)

### Community 75 - "Community 75"
Cohesion: 0.29
Nodes (6): Comportamiento, get_property_images, Implementation (Level 3), Instructions (Level 2), Parámetros, Summary (Level 1)

### Community 76 - "Community 76"
Cohesion: 0.33
Nodes (5): AgenticLoop — full Plan→Act→Observe→Evaluate cycle (Phase 9).  Orchestrates the, Execute the full Plan→Act→Observe→Evaluate agentic cycle.      Args:         mes, run_agentic_loop(), Generate hidden CoT reasoning for the current turn.      Args:         message:, think()

### Community 78 - "Community 78"
Cohesion: 0.5
Nodes (4): code:python (PATTERNS = [), code:bash (# S1 handles greetings (no LLM call, <1ms)), code:block9 (app/), Phase 4: Dual-Router — System 1 (<1ms) + System 2 (LLM) ✅ COMPLETED

### Community 79 - "Community 79"
Cohesion: 0.5
Nodes (4): code:block12 (app/), code:python (def can_search(belief: ConversationBeliefState) -> bool:), code:bash (# Belief state evolves with conversation), Phase 5: Dynamic Belief State — Beyond 15-State Enum ✅ COMPLETED

### Community 80 - "Community 80"
Cohesion: 0.5
Nodes (4): code:block15 (skills/), code:yaml (---), code:bash (# Hot-reload: modify a SKILL.md while server is running), Phase 6: SKILL.md Ecosystem + MCP ✅ COMPLETED

### Community 81 - "Community 81"
Cohesion: 0.5
Nodes (4): code:block18 (app/), code:block19 (Redis:), code:bash (# Session 1: User searches, views, leaves), Phase 7: Multi-Tier Memory Architecture ✅ COMPLETED

### Community 82 - "Community 82"
Cohesion: 0.5
Nodes (4): code:block21 (app/), code:block22 (User Message), code:bash (# Flexible scheduling (no wizard!)), Phase 8: Multi-Agent Orchestration ✅ COMPLETED

### Community 83 - "Community 83"
Cohesion: 0.5
Nodes (4): code:block24 (app/), code:block25 (User Message), code:bash (# Complex multi-step query), Phase 9: Agentic Loop — Plan→Act→Observe→Evaluate ✅ COMPLETED

### Community 84 - "Community 84"
Cohesion: 0.5
Nodes (4): code:block27 (app/), code:python (# Formality levels), code:bash (# Argentine vocabulary), Phase 10: Natural Language Quality + Argentine Spanish ✅ COMPLETED

### Community 85 - "Community 85"
Cohesion: 0.5
Nodes (4): code:block32 (docker-compose.prod.yml     # Production overrides (no debug), code:block33 (□ Skills are portable: copy skills/* to inmueblebot/skills/), code:bash (# Production build), Phase 12: Production Hardening + Migration Path

### Community 86 - "Community 86"
Cohesion: 0.67
Nodes (3): ChatbotSerio-specific optimizations, Key differences from legacy models (gpt-4o-mini, gpt-3.5-turbo), LLM Strategy: gpt-5.4-mini

### Community 87 - "Community 87"
Cohesion: 0.67
Nodes (3): code:block1 (ChatbotSerio/), code:bash (# Boot everything), Phase 0: Project Skeleton + Docker Foundation ✅ COMPLETED

### Community 88 - "Community 88"
Cohesion: 0.67
Nodes (3): code:block3 (app/), code:bash (# Basic chat), Phase 1: Bare Agent Loop — Single LLM + Tool Calling ✅ COMPLETED

### Community 89 - "Community 89"
Cohesion: 0.67
Nodes (3): code:block30 (app/), code:bash (# Run full test suite), Phase 11: Observability + Testing Infrastructure ✅ COMPLETED

### Community 90 - "Community 90"
Cohesion: 0.67
Nodes (3): code:block5 (app/), code:bash (# Seed data), Phase 2: Real Estate Domain — Property Search + Core Tools ✅ COMPLETED

### Community 91 - "Community 91"
Cohesion: 0.67
Nodes (3): code:block7 (app/), code:bash (# Structured output always valid), Phase 3: Structured Output + Progressive Escalation ✅ COMPLETED

## Knowledge Gaps
- **400 isolated node(s):** `FastAPI application entry point — ChatbotSerio.`, `MCP JSON-RPC 2.0 endpoint — exposes all skills as MCP tools.`, `Hot-reload all skills from SKILL.md files.`, `List all loaded skills with metadata.`, `Run memory consolidation after a session ends.      Saves episode summary, updat` (+395 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `route_message()` connect `Community 4` to `Community 33`, `Community 2`, `Community 5`, `Community 8`, `Community 12`, `Community 13`, `Community 14`, `Community 23`, `Community 31`?**
  _High betweenness centrality (0.400) - this node is a cross-community bridge._
- **Why does `process_message_multistep()` connect `Community 13` to `Community 4`, `Community 6`, `Community 10`, `Community 14`, `Community 16`, `Community 18`, `Community 24`, `Community 26`?**
  _High betweenness centrality (0.265) - this node is a cross-community bridge._
- **Why does `run_agentic_loop()` connect `Community 76` to `Community 1`, `Community 38`, `Community 10`, `Community 13`, `Community 14`, `Community 16`, `Community 24`, `Community 26`, `Community 30`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `ConversationBeliefState` (e.g. with `TestBeliefState` and `TestStateTransitioner`) actually correct?**
  _`ConversationBeliefState` has 57 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `StructuredToolCall` (e.g. with `TestSchemas` and `TestFAQ`) actually correct?**
  _`StructuredToolCall` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `route_message()` (e.g. with `chat()` and `simulate_chat()`) actually correct?**
  _`route_message()` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Observation` (e.g. with `Evaluation` and `TestPlanner`) actually correct?**
  _`Observation` has 17 INFERRED edges - model-reasoned connections that need verification._