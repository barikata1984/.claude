---
name: sweep
description: Orchestrate wandb sweep experiments end-to-end - plan → config YAML → launch agents → analyze results. This is the top-level entry point that auto-detects the current phase from conversation context (plan needed, YAML to generate, agents to launch, or results to analyze) and routes to the right sub-skill (/sweep-config, /sweep-run, /sweep-analyze) or handles planning inline. Use this skill whenever the user mentions wandb sweeps, hyperparameter search, hyperparameter tuning, trying multiple values for training parameters, grid/random/bayesian search, or comparing model performance across hyperparameter settings. Also trigger on phrases like "I want to try different learning rates", "run a sweep for X", "sweep over batch sizes", "compare these hyperparameters", "ハイパラ探索", "スイープ", or any request to systematically explore an ML training configuration space.
---

# sweep

Unified entry point for wandb sweep experiment management. Routes to sub-skills or handles planning inline.

## Usage

```
/sweep              → Auto-detect from context
/sweep plan         → Plan the experiment (inline)
/sweep config       → Generate sweep config YAML (/sweep-config)
/sweep run          → Launch sweep agents + monitoring (/sweep-run)
/sweep analyze      → Analyze sweep results (/sweep-analyze)
/sweep full         → Run plan → config → run → analyze in sequence
```

## Auto-detection logic

When called without arguments, determine the action in the following priority order:

1. Conversation mentions sweep results or a sweep ID → **analyze**
2. A sweep is running (check `tmux ls` for sweep sessions) → offer status check or analyze
3. Conversation already contains selected parameters → **config**
4. None of the above → start with **plan** (below)

## Planning (inline)

When planning is needed, guide the user through these phases. The goal is to go from
a vague idea ("I want to try different learning rates") to a concrete, testable sweep plan.

### Quick-start check

If the user already specifies parameters and values (e.g., "sweep lr over 1e-3, 1e-4, 1e-5"),
skip the objective clarification and go directly to the execution plan. Planning exists to
help users who need it, not to slow down users who already know what they want.

### Phase 1: Clarify objectives (skip if user already has parameters)

Ask the user to articulate the experiment objective:

- **What to improve**: Task performance? Training efficiency? Generalization?
- **Current issues**: What is unsatisfactory about the current model?
- **Hypothesis**: Why do you think this problem is occurring?

Dig deeper based on responses rather than asking everything at once.

### Phase 2: Parameter selection

1. Read the project's config files (model config, training config) to understand available parameters
2. Propose candidates relevant to the user's objective, explaining why each matters
3. Present type, default value, and feasible range for each candidate
4. Determine parameters and value ranges through dialogue

### Phase 3: Execution plan

1. Decide search method (grid / random / bayes)
   - Calculate combination count; suggest random/bayes for > 100 runs
2. Confirm base config file and dataset
3. Check existing sweep records (`notes/LOGS/log_sweep.md`) to avoid duplicating past experiments
4. Present the plan and obtain user approval

### Phase 4: Record

After approval, append to `notes/LOGS/log_sweep.md`:

```markdown
## YYYY-MM-DD: <sweep_name>

### Objective
<Experiment objective and hypothesis>

### Search parameters
| Parameter | Values | Selection rationale |
|-----------|--------|---------------------|
| ...       | ...    | ...                 |

### Execution plan
- method: <grid/random/bayes>
- base config: `<path>`
- dataset: `<name>`
- expected run count: <N>

### Results
_(to be filled by /sweep analyze)_
```

Then offer to proceed to `/sweep config`.

## Full mode

When `/sweep full` is specified, execute in sequence with user approval between each phase:

1. **Plan** — Clarify objectives and select parameters (inline, above)
2. **Config** — Generate and validate YAML (`/sweep-config`)
3. **Run** — GPU status → launch agents + monitoring (`/sweep-run`)
4. (After sweep completion) **Analyze** — Results analysis (`/sweep-analyze`)

## Shared context

To locate project-specific references, read the project's existing files:

- **Config classes**: Find via `grep -r "class.*Config" src/` or similar
- **Existing sweep configs**: `configs/sweep_*.yaml` (match their style)
- **Experiment logs**: `notes/LOGS/log_sweep.md`
- **GPU monitoring data**: `notes/LOGS/gpu_monitor_*.csv`

## Rules

- Respect the user's intuition and hypotheses — translate them into testable experiments
- Parameter selection should be objective-driven; avoid "explore everything just in case"
- If existing sweep results are available in `log_sweep.md`, incorporate those insights
