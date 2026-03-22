# Phase 7: Review / Improvement Loop

Task generation template for the cross-critique and quality assurance phase.
SKILL.md reads this file when entering Phase 7 and generates tasks dynamically
based on the Phase 6 output draft.

## Input

- Phase 6 deliverable: **Output draft** (paper draft or product deliverables)
- Phase 3 deliverable: **Implementation code** (for code-paper/code-product consistency checks)
- Phase 5 deliverable: **Analysis report** (for claim-evidence verification)

## Task Generation Rules

### Both Modes

Tasks are generated in two rounds: external verification first, then cross-critique.
This ordering ensures critique agents have objective evidence available.

#### Round 1: External Verification

1. **Automated code verification** (1 task)
   - Agent: Engineer (execute)
   - Dependencies: none
   - Instruction: Run full verification suite on the codebase:
     - `python -m pytest tests/ -v`
     - `ruff check .`
     - `ruff format --check .`
     - `pyright` (if installed)
   - If any check fails, this task produces REVISE status automatically. SKILL.md creates a fix task before proceeding to Round 2

#### Round 2: Cross-Critique

Cross-critique dispatch follows `references/handoff_protocol.md` (Cross-Critique Dispatch table).
Self-review is prohibited — each agent reviews a different agent's output.

2. **Engineer reviews Research output** (1 task)
   - Agent: Engineer (critique)
   - Dependencies: Round 1 complete (or PASS)
   - Instruction: Review the paper draft / documentation. Focus on:
     - Method section accuracy: does it match the actual implementation?
     - Code snippets and pseudocode correctness
     - Reproducibility: can someone reproduce results from the description?

3. **Research reviews Engineer output** (1 task)
   - Agent: Research (critique)
   - Dependencies: Round 1 complete (or PASS)
   - Instruction: Review the implementation code. Focus on:
     - Code-paper consistency: does the code implement what the paper claims?
     - Citation accuracy: are referenced algorithms correctly implemented?
     - README and documentation completeness

4. **Analyst reviews overall output** (1 task)
   - Agent: Analyst (critique)
   - Dependencies: Round 1 complete (or PASS)
   - Instruction: Review all deliverables for statistical integrity. Focus on:
     - Claim-evidence alignment: every quantitative claim backed by data
     - Figure accuracy: correct values, appropriate error bars, matching captions
     - Statistical interpretation: no p-hacking, no overstated significance

#### Round 3: Verdict and Resolution

5. **Verdict aggregation** (1 task — human decision)
   - Agent: none (human task — lead aggregates verdicts)
   - Dependencies: all critique tasks complete
   - Instruction: Lead reviews all critique verdicts and external verification results:
     - **All PASS** → proceed to Phase 8 (approval gate)
     - **Any REVISE** → Loop D: create revision tasks for the original agents, then re-review
     - **Any BLOCK** → Loop C: regress to Phase 3 or 4 (lead decides which)

6. **Revision tasks** (generated only if verdict includes REVISE — Loop D)
   - Agent: the original agent whose output received REVISE (execute mode)
   - Dependencies: verdict aggregation
   - Instruction: Address the specific issues identified in the critique. Each REVISE verdict generates one revision task for the responsible agent

7. **Re-review** (generated only after revision tasks complete — Loop D continuation)
   - Agent: the same critic who issued REVISE (critique mode)
   - Dependencies: corresponding revision task complete
   - Instruction: Re-review the revised output. Only check the issues from the original critique — do not expand scope

## Task Granularity Guidelines

- 1 task = 1 agent invocation
- External verification is always 1 task (all checks run together)
- Cross-critiques are 1 task per critic (3 tasks total)
- Loop D revision: 1 task per REVISE verdict (may be multiple if multiple critics issued REVISE)
- Loop D re-review: 1 task per revision (matching the critic who issued the original REVISE)
- Maximum Loop D iterations: 3. After 3 rounds of REVISE on the same issue, escalate to lead

## Completion Condition

All critiques resolved to PASS.
See `references/phase_transitions.md` for transition rules, Loop C, and Loop D.

## Approval Gate

Phase 7 → Phase 8 requires explicit user approval (irreversible publication/release decision).
See `references/phase_transitions.md` for the approval gate definition.

## Output Format

All agent reports must follow `references/handoff_protocol.md`.
Critique reports must include Verdict (PASS / REVISE / BLOCK) and specific findings with evidence.
