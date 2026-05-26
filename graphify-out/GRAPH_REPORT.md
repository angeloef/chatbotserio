# Graph Report - .  (2026-05-26)

## Corpus Check
- Corpus is ~34,391 words - fits in a single context window. You may not need a graph.

## Summary
- 988 nodes · 1528 edges · 72 communities (57 shown, 15 thin omitted)
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 499 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Test Router Suite|Test Router Suite]]
- [[_COMMUNITY_Agentic Loop Evaluator|Agentic Loop Evaluator]]
- [[_COMMUNITY_Memory System|Memory System]]
- [[_COMMUNITY_Skills & MCP|Skills & MCP]]
- [[_COMMUNITY_Router & Property Tools|Router & Property Tools]]
- [[_COMMUNITY_Belief State & Working Memory|Belief State & Working Memory]]
- [[_COMMUNITY_NLP Layer|NLP Layer]]
- [[_COMMUNITY_Core Infrastructure|Core Infrastructure]]
- [[_COMMUNITY_Memory Consolidation & User Model|Memory Consolidation & User Model]]
- [[_COMMUNITY_Multi-Agent Coordinator|Multi-Agent Coordinator]]
- [[_COMMUNITY_Escalation System|Escalation System]]
- [[_COMMUNITY_Conversation Manager|Conversation Manager]]
- [[_COMMUNITY_State Transitioner|State Transitioner]]
- [[_COMMUNITY_Main Agent Loop|Main Agent Loop]]
- [[_COMMUNITY_API Schemas|API Schemas]]
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

## God Nodes (most connected - your core abstractions)
1. `ConversationBeliefState` - 61 edges
2. `s1_handles()` - 33 edges
3. `StructuredToolCall` - 23 edges
4. `Observation` - 20 edges
5. `run_agentic_loop()` - 19 edges
6. `update_belief()` - 19 edges
7. `s1_delegates()` - 19 edges
8. `classify_intent()` - 18 edges
9. `parse_llm_response()` - 18 edges
10. `route_message()` - 18 edges

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

## Communities (72 total, 15 thin omitted)

### Community 0 - "Test Router Suite"
Cohesion: 0.05
Nodes (20): Tests for System 1 + System 2 dual router.  Verifies: - S1 catches greetings, co, Does S1 match this message (at any confidence tier)?, Does S1 match AND handle (not delegate) this message?, Verify 80%+ S1 routing on the 50 test messages., At least 80% of messages should be handled by S1 (handle + delegate)., Print detailed coverage breakdown., Does S1 match but delegate to S2?, s1_delegates() (+12 more)

### Community 1 - "Agentic Loop Evaluator"
Cohesion: 0.06
Nodes (36): build_replan_context(), _build_success_summary(), evaluate(), Evaluation, LoopEvaluator — expected vs actual, replan logic (Phase 9).  After executing the, Build a replan hint for the LLM context.      This tells the LLM what to do diff, Result of evaluating an execution plan., Evaluate whether the plan achieved its goals.      Replanning triggers:     - Se (+28 more)

### Community 2 - "Memory System"
Cohesion: 0.06
Nodes (44): build_greeting_from_episodes(), get_episodes(), get_last_episode(), _get_redis(), EpisodicMemory — past session summaries for cross-session recall.  Redis: episod, Build a personalized greeting based on past episodes.      Returns empty string, Get Redis connection or None if unavailable., Save a session episode to PostgreSQL and Redis cache. (+36 more)

### Community 3 - "Skills & MCP"
Cohesion: 0.06
Nodes (22): _error(), _execute_skill_tool(), handle_mcp_request(), handle_mcp_request_raw(), MCPResponse, MCP (Model Context Protocol) JSON-RPC 2.0 server.  Exposes all registered skills, JSON-RPC 2.0 response., Handle a JSON-RPC 2.0 MCP request.      Supported methods:     - initialize: MCP (+14 more)

### Community 4 - "Router & Property Tools"
Cohesion: 0.07
Nodes (28): _extract_property_data(), Dual router — S1 + Coordinator (multi-agent Phase 8)., Route message through S1 → Coordinator with memory integration., Extract key property data lines from a get_property_details result., Try to handle the message deterministically without calling the LLM.          Re, route_message(), _try_pre_llm_shortcut(), _update_belief_from_result() (+20 more)

### Community 5 - "Belief State & Working Memory"
Cohesion: 0.08
Nodes (27): clear_session(), get_belief(), ConversationBeliefState — dynamic multi-turn state tracking (Phase 5).  Replaces, Get or create a belief state for a session., Persist belief state to the store., Remove a session from the store., save_belief(), clear_working_memory() (+19 more)

### Community 6 - "NLP Layer"
Cohesion: 0.09
Nodes (16): adjust_tone(), detect_emotion(), EmotionalState, get_empathetic_prefix(), Empathy detection — sentiment analysis + adaptive tone (Phase 10).  Detects emot, Adjust response tone based on detected emotion.      If emotion is frustrated: b, Detect the user's emotional state from their message.      Returns the strongest, Get an empathetic response prefix based on detected emotion. (+8 more)

### Community 7 - "Core Infrastructure"
Cohesion: 0.08
Nodes (25): consolidate_session(), ConsolidateRequest, get_user_memory(), health_ready(), lifespan(), mcp_endpoint(), _ping_redis(), proactive_check() (+17 more)

### Community 8 - "Memory Consolidation & User Model"
Cohesion: 0.11
Nodes (24): consolidate_session(), MemoryConsolidator — summarize session → update memory → prune (Phase 7).  Runs, Run the full memory consolidation pipeline after a session.      Args:         b, Generate a compact summary of the session., _summarize_session(), build_personalized_context(), get_persona(), _get_redis() (+16 more)

### Community 9 - "Multi-Agent Coordinator"
Cohesion: 0.1
Nodes (6): classify_intent(), Classify user intent using regex-first approach.      Returns the specialist nam, Tests for coordinator intent classification and specialist routing., TestIntentClassification, TestIntentPatterns, TestSpecialists

### Community 10 - "Escalation System"
Cohesion: 0.12
Nodes (10): assess_confidence(), build_clarification_message(), EscalationLevel, Confidence-based escalation system (Phase 3).  Implements the stratified autonom, Clamp and classify confidence into an escalation level.      Returns (level, cla, Modify or replace the response based on the escalation level.      - EXECUTE: pa, Enum, Tests for escalation module — confidence thresholds and clarification messages. (+2 more)

### Community 11 - "Conversation Manager"
Cohesion: 0.12
Nodes (17): build_interruption_prompt(), clear_saved_state(), ConversationSnapshot, detect_topic_switch(), get_saved_state(), Conversation manager — handles topic switching and state save/restore (Phase 8)., Saved state when a conversation is interrupted., Save the current specialist context before switching topics. (+9 more)

### Community 12 - "State Transitioner"
Cohesion: 0.13
Nodes (11): _fuzzy_normalize(), _parse_bedrooms(), _parse_budget(), State transitioner — extracts entities from messages and updates belief state., Extract minimum bedrooms from text., Normalize common typos and merged words for regex matching.      Handles:     -, Extract entities from message and accumulate into belief state.      Criteria ar, Extract a budget amount from text. Returns None if no budget found. (+3 more)

### Community 13 - "Main Agent Loop"
Cohesion: 0.13
Nodes (20): _format_tool_result_for_user(), process_message(), process_message_multistep(), process_message_with_specialist(), SimpleAgent — LLM + tool calling + structured output + escalation (Phase 3)., Format a raw tool result into user-friendly text.      For get_property_details, Process a message that may require multiple tool calls, emitting each result as, Process a message through a specialist agent with filtered tools.      Args: (+12 more)

### Community 14 - "API Schemas"
Cohesion: 0.14
Nodes (14): AgentResponse, ChatRequest, ChatResponse, MessageChunk, Agent response and tool call schemas., Structured response from the agent after processing a message., A single message bubble in a multi-message response sequence., Incoming chat request. (+6 more)

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
Cohesion: 0.13
Nodes (10): check_response_quality(), enrich_with_argentinisms(), get_preferred_term(), is_argentine_term(), Argentine Spanish vocabulary and regional adaptations (Phase 10).  Maps generic, Replace generic terms with Argentine equivalents where possible., Check if a word is in the Argentine vocabulary., Get the preferred Argentine term for a generic word. (+2 more)

### Community 19 - "Community 19"
Cohesion: 0.13
Nodes (10): can_schedule(), can_view_details(), needs_clarify_operation(), A property is selected, can show details., Property selected AND scheduling intent expressed., Search intent but no operation (alquiler/venta) specified., Multiple turns without progress → suggest human handoff., should_handoff() (+2 more)

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (15): can_ask_faq(), can_confirm(), can_greet(), can_view_photos(), needs_clarify_budget(), needs_clarify_type(), needs_clarify_zone(), Guard functions — 12 boolean predicates on ConversationBeliefState.  Replace 168 (+7 more)

### Community 21 - "Community 21"
Cohesion: 0.21
Nodes (7): ConversationBeliefState, Accumulated conversation state across multiple turns.      Updated each turn via, Human-readable summary for debugging / context injection., _classify_outcome(), Classify the session outcome based on state., TestBeliefState, TestClassifyOutcome

### Community 22 - "Community 22"
Cohesion: 0.17
Nodes (10): get_active_skills_summary(), get_context_tokens(), Progressive disclosure — selects skill detail level based on context.  Level 1 (, Estimate token cost for loading skills at a given level.      Args:         skil, Token count for a skill at a given level., Decide which disclosure level to use.      Default: Level 1 (summary only) — for, Build a compact summary of all skills for the system prompt.      This is the Le, select_level() (+2 more)

### Community 23 - "Community 23"
Cohesion: 0.17
Nodes (9): build_context_prompt(), detect_clarification_loop(), _get_missing_criteria(), Context aggregator — builds enriched LLM system prompt from belief state.  Injec, Detect if we're stuck in a clarification loop (re-asking same questions).     Re, Return list of missing search criteria names., Build an additional context block to prepend to the LLM system prompt.      Give, Tests for Phase 5: belief state, guards, state transitioner, context aggregator. (+1 more)

### Community 24 - "Community 24"
Cohesion: 0.21
Nodes (11): A structured tool call from the LLM (OpenAI format)., StructuredToolCall, Tests for real estate tools — search, details, images, FAQ., test_execute_faq(), TestToolExecution, Tests for the tool registry and individual tools., test_execute_bad_arguments(), test_execute_echo() (+3 more)

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
Cohesion: 0.22
Nodes (10): clear_session_trace(), end_span(), Span-based tracing — every decision logged (Phase 11)., Start a trace span for a session., End a trace span and record it., Clear traces for a session., start_span(), TraceSpan (+2 more)

### Community 32 - "Community 32"
Cohesion: 0.24
Nodes (7): _run_search(), TestDescribeFilters, _describe_filters(), Search properties by criteria — filters: operation, type, zone, budget, bedrooms, Search properties in Oberá matching the given filters.      All filters are opti, Build a human-readable description of active filters., search_properties()

### Community 33 - "Community 33"
Cohesion: 0.27
Nodes (9): ensure_log_dir(), get_session_logs(), log_turn(), Conversation logger — records every turn to a JSONL file for debugging., Create the log directory if it doesn't exist., Log a single conversation turn to the JSONL file.      Returns the logged entry, Read the most recent conversation turns from the log file., Get all turns for a specific session. (+1 more)

### Community 34 - "Community 34"
Cohesion: 0.2
Nodes (9): get_metrics(), Metrics collection — latency histograms, routing stats, error rates (Phase 11)., Record a single request's metrics., Get current metrics summary., record_request(), admin_diagnostics(), admin_stats(), Get system metrics: routing, latency, error rate. (+1 more)

### Community 35 - "Community 35"
Cohesion: 0.2
Nodes (9): clear_logs(), Clear the log file. Returns number of entries removed., conversations_clear(), conversations_recent(), conversations_session(), Admin routes — stats, traces, A/B testing, diagnostics (Phase 11)., View recent conversation turns for debugging., View all turns for a specific session. (+1 more)

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
Cohesion: 0.25
Nodes (8): get_latest_traces(), get_session_trace(), Get all spans for a session., Get the most recent session traces., admin_traces_latest(), admin_traces_session(), Get the 10 most recent session traces., Get the full trace for a specific session.

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
Cohesion: 0.29
Nodes (4): can_search(), can_search_with_partial(), User has enough criteria OR explicitly asking to search., User has at least 2 criteria — enough for a broad search.

### Community 44 - "Community 44"
Cohesion: 0.33
Nodes (4): BaseSettings, Application settings from environment variables., ChatbotSerio configuration loaded from environment., Settings

### Community 45 - "Community 45"
Cohesion: 0.33
Nodes (5): build_coherence_context(), check_coherence(), Multi-turn coherence checker (Phase 10).  Ensures responses reference prior conv, Check if a response is coherent with the conversation history.      Returns:, Build a coherence hint for the LLM to maintain multi-turn consistency.      Incl

### Community 46 - "Community 46"
Cohesion: 0.4
Nodes (4): Simulate endpoint — test the chatbot without WhatsApp (Phase 11)., Simulate with extra metadata — returns belief state + trace., simulate_multi(), SimulateRequest

### Community 47 - "Community 47"
Cohesion: 0.5
Nodes (3): System 2 router — delegates to the existing LLM agent loop (Phase 5).  Now accep, Forward to the full LLM agent loop with optional belief context.      The contex, route_s2()

### Community 48 - "Community 48"
Cohesion: 0.5
Nodes (3): chat(), POST /chat — dual-router with multi-tier memory + conversation logging., Route message through S1 → S2 with multi-turn belief + cross-session memory.

### Community 49 - "Community 49"
Cohesion: 0.5
Nodes (3): Parsed representation of a SKILL.md file., Convert to MCP tool definition., SkillDefinition

## Knowledge Gaps
- **304 isolated node(s):** `FastAPI application entry point — ChatbotSerio.`, `MCP JSON-RPC 2.0 endpoint — exposes all skills as MCP tools.`, `Hot-reload all skills from SKILL.md files.`, `List all loaded skills with metadata.`, `Run memory consolidation after a session ends.      Saves episode summary, updat` (+299 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `route_message()` connect `Router & Property Tools` to `Memory System`, `Belief State & Working Memory`, `Memory Consolidation & User Model`, `State Transitioner`, `Main Agent Loop`, `Community 46`, `API Schemas`, `Community 48`, `Community 23`, `Community 31`?**
  _High betweenness centrality (0.432) - this node is a cross-community bridge._
- **Why does `process_message_multistep()` connect `Main Agent Loop` to `Router & Property Tools`, `NLP Layer`, `Escalation System`, `API Schemas`, `Community 16`, `Community 18`, `Community 24`, `Community 26`?**
  _High betweenness centrality (0.289) - this node is a cross-community bridge._
- **Why does `run_agentic_loop()` connect `Main Agent Loop` to `Agentic Loop Evaluator`, `Community 38`, `Escalation System`, `API Schemas`, `Community 16`, `Community 24`, `Community 26`, `Community 30`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `ConversationBeliefState` (e.g. with `TestBeliefState` and `TestStateTransitioner`) actually correct?**
  _`ConversationBeliefState` has 57 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `StructuredToolCall` (e.g. with `TestSchemas` and `TestFAQ`) actually correct?**
  _`StructuredToolCall` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Observation` (e.g. with `Evaluation` and `TestPlanner`) actually correct?**
  _`Observation` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `run_agentic_loop()` (e.g. with `get_tools_schema()` and `think()`) actually correct?**
  _`run_agentic_loop()` has 17 INFERRED edges - model-reasoned connections that need verification._