# Phase 1: Literature / Market Research

Task generation template for the research and survey phase.
SKILL.md reads this file when entering Phase 1 and generates tasks dynamically
based on the Phase 0 problem definition.

## Input

- Phase 0 deliverable: **Problem definition document** (one-page, states what to solve and why)

## Task Generation Rules

### Academic Mode

1. **Core literature survey** (1 task per sub-topic identified in the problem definition)
   - Agent: Research (execute)
   - Dependencies: none
   - Instruction: Search systematically across three temporal tiers (Recent / Established / Foundational). Verify every paper before reporting. Follow `/literature-survey` methodology
   - Delegation: If the lead expects 30+ papers, delegate to `/literature-survey` skill instead of generating individual tasks

2. **Gap analysis** (1 task)
   - Agent: Research (execute)
   - Dependencies: all survey tasks complete
   - Instruction: Synthesize survey results into a gap analysis. Clearly articulate what is known, what is unknown, and where the proposed approach fits

### Startup Mode

1. **Competitor analysis** (1 task per major competitor or competitor cluster)
   - Agent: Research (execute)
   - Dependencies: none
   - Instruction: Analyze competitor products, pricing, technical approach, and market positioning

2. **Patent and IP search** (1 task)
   - Agent: Research (execute)
   - Dependencies: none
   - Instruction: Search patent databases for relevant filings. Identify freedom-to-operate risks

3. **Market sizing and positioning** (1 task)
   - Agent: Research (execute)
   - Dependencies: competitor analysis tasks complete
   - Instruction: Estimate TAM/SAM/SOM. Identify target segments and positioning strategy

### Both Modes

4. **Survey report compilation** (1 task)
   - Agent: Research (execute)
   - Dependencies: all above tasks complete
   - Instruction: Compile all findings into a single structured report. This becomes the input for Phase 2

## Task Granularity Guidelines

- 1 task = 1 agent invocation
- For literature surveys: 1 task per sub-topic (e.g., "sim-to-real transfer methods", "reward shaping approaches")
- For competitor analysis: group similar competitors into 1 task (max 3-4 competitors per task)
- If the lead identifies more than 5 sub-topics, propose grouping related sub-topics

## Completion Condition

Gap between existing work and proposed approach is clearly articulated.
See `references/phase_transitions.md` for transition rules.

## Output Format

All agent reports must follow `references/handoff_protocol.md`.
