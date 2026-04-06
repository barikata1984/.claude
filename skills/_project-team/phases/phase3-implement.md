# Phase 3: Implementation / Prototype

Task generation template for the implementation phase.
SKILL.md reads this file when entering Phase 3 and generates tasks dynamically
based on the Phase 2 experiment plan.

## Input

- Phase 2 deliverable: **Approved experiment plan** (variables, conditions, metrics, baselines)
- If entering via Loop C (critical defect): Phase 7 BLOCK verdict with defect description

## Task Generation Rules

### Both Modes

1. **Baseline implementation** (1 task per comparison target in the experiment plan)
   - Agent: Engineer (execute)
   - Dependencies: none
   - Instruction: Implement each baseline/comparison target specified in the experiment plan. Each task produces a runnable module with unit tests

2. **Proposed method implementation** (1 task per major component of the proposed approach)
   - Agent: Engineer (execute)
   - Dependencies: none
   - Instruction: Implement each core component of the proposed method. Break along module boundaries (e.g., model architecture, reward function, data pipeline)

3. **Experiment infrastructure** (1 task — can run in parallel with categories 1-2)
   - Agent: Engineer (execute)
   - Dependencies: none
   - Instruction: Set up the experiment environment: Docker config, wandb integration, training scripts, evaluation harness, GPU job submission templates

4. **External verification** (1 task)
   - Agent: Engineer (execute)
   - Dependencies: categories 1, 2 complete
   - Instruction: Run `pytest`, `ruff check`, `ruff format --check`, and `pyright` (if installed) on all new code. Fix any failures. Report results in the External Verification table

5. **Code review** (1 task)
   - Agent: Research (critique)
   - Dependencies: categories 1, 2 complete + external verification passes
   - Instruction: Review implementation for consistency with the experiment plan and any cited papers. Verify that the Method section's algorithm matches the code. Focus on correctness, not style (style is enforced by ruff)

6. **Physical integration** (conditional — only if the project uses physical robots)
   - Agent: none (human task — lead + operator)
   - Dependencies: categories 1, 2, 3 complete
   - Instruction: Integrate code with physical hardware. This is outside agent scope

## Task Granularity Guidelines

- 1 task = 1 agent invocation = roughly 1 file or 1 module
- If a baseline requires more than ~300 lines of new code, split into sub-tasks (e.g., model vs training loop)
- Infrastructure is a single task unless multi-environment setup is needed (e.g., separate sim + real configs)
- The external verification task is mandatory — SKILL.md must not skip it

## Completion Condition

All implementation tasks done, external verification (pytest/ruff/pyright) passes.
See `references/phase_transitions.md` for transition rules.

## Output Format

All agent reports must follow `references/handoff_protocol.md`.
Engineer reports must include the External Verification table.
