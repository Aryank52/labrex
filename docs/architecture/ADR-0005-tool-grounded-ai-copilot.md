# ADR-0005: Tool-Grounded AI Policy Copilot Architecture

**Status:** APPROVED  
**Date:** 2026-10-20  
**Deciders:** Principal Engineering Agent  

---

## Context
Deploying Generative AI / Large Language Models (LLMs) in public policy decision-support carries severe risks of numerical hallucinations, fabricated statistics, and prompt injection attacks. An LLM must never be allowed to invent labour-market figures, budget numbers, or policy rankings.

## Decision
We architect the **LABREX Copilot** around Gemini 3.8 using **Strict Tool Grounding**:
1. The LLM has zero direct database credentials and cannot execute raw SQL or shell commands.
2. All platform actions are declared as strongly typed Pydantic tool schemas (`get_district_snapshot`, `get_forecast`, `run_budget_optimization`, etc.).
3. The LLM acts solely as a natural language intent router, translator, and explainer.
4. An output verification layer checks that every numerical claim in the LLM response is grounded in the payload returned by the executed tool. Mismatched claims trigger an automated warning.
5. User inputs and retrieved text are encapsulated in immutable boundary delimiters to defend against prompt injection.

## Consequences
### Positive
- Eliminates numerical hallucination in policy advice.
- Provides complete auditability of all tool actions.
- Enforces strict security boundaries against prompt injection.

### Negative / Trade-offs
- Requires explicit definition and maintenance of Pydantic tool schemas for every query type.
- Adds slight latency for two-stage tool-calling roundtrips.
