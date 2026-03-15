# sweep-plan

Plan sweep experiments. Clarify objectives through dialogue with the user and select parameters to explore.

## Phase 1: Clarify objectives

Ask the user the following questions to articulate the macro-level experiment objective:

- **What to improve**: Task performance? Training efficiency? Generalization? Inference speed?
- **Current issues**: What is unsatisfactory about the current model? What behavior to improve?
- **Hypothesis**: Why do you think this problem is occurring?

Do not ask all questions at once; dig deeper based on responses. Continue the dialogue until the objective is sufficiently clear.

## Phase 2: Parameter selection

Once the objective is clear:

1. Read `src/models/configs/multi_modal_config.py` and `src/training/config.py` to understand the full landscape of available parameters
2. Propose parameter candidates relevant to the user's objective
   - Explain "why this parameter is relevant to the objective" for each candidate
   - Present the type, default value, and feasible range for each parameter
3. Determine the parameters and value ranges to explore through dialogue with the user

**Note**: Parameter proposals should be derived from the user's objective. Do not impose a pre-determined tier structure.

## Phase 3: Execution plan

Once parameters are determined:

1. Decide the search method (grid / random / bayes)
   - Calculate the number of combinations and evaluate whether grid is realistic
   - Suggest random/bayes for more than 100 runs
2. Confirm the base config file and dataset
3. Check existing sweep records (`docs/LOGS/log_sweep.md`) to avoid duplicates
4. Present the plan in conversation and obtain user approval

## Phase 4: Record

After approval, append to `docs/LOGS/log_sweep.md`:

```markdown
## YYYY-MM-DD: <sweep_name>

### Objective
<Experiment objective and hypothesis clarified through user dialogue>

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
_(to be filled by sweep-analyze)_
```

## Rules

- Do not proceed with a vague objective. Do not skip Phase 1
- Parameter selection is objective-driven. Avoid "explore everything just in case"
- If existing sweep results (log_sweep.md) are available, incorporate those insights into proposals
- Respect the user's intuition and hypotheses, and translate them into testable experiments
