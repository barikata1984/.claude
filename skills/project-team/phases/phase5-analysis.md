# Phase 5: Analysis and Interpretation

Task generation template for the data analysis phase.
SKILL.md reads this file when entering Phase 5 and generates tasks dynamically
based on the Phase 4 experiment data.

## Input

- Phase 4 deliverable: **Experiment data** (wandb logs, CSV files, videos, etc.)
- Phase 2 deliverable: **Experiment plan** (which tests to run, metrics, significance thresholds)
- If entering via Loop B (additional experiments): previous Phase 5 partial analysis

## Task Generation Rules

### Both Modes

1. **Data preprocessing and validation** (1 task)
   - Agent: Analyst (execute)
   - Dependencies: none
   - Instruction: Load experiment data, check for missing values and outliers, document outlier handling policy. Verify that the data matches the experiment plan (correct number of runs, conditions, etc.)

2. **Primary analysis** (1 task per hypothesis or primary metric in the experiment plan)
   - Agent: Analyst (execute)
   - Dependencies: data preprocessing complete
   - Instruction: Run the planned statistical tests. For each comparison, report: test used, p-value, effect size, 95% CI, and verdict. Apply multiple comparison correction as specified in the experiment plan. Follow the Statistical Rigor Checklist from the Analyst agent definition
   - Delegation: If the experiment used `/sweep run`, delegate to `/sweep analyze` for initial result extraction

3. **Ablation / secondary analysis** (1 task per ablation or secondary metric, if specified in the plan)
   - Agent: Analyst (execute)
   - Dependencies: primary analysis complete
   - Instruction: Run ablation or secondary analyses. These verify which components contribute to the result

4. **Figure and table generation** (1 task)
   - Agent: Analyst (execute)
   - Dependencies: primary analysis complete
   - Instruction: Generate publication-quality figures (matplotlib/seaborn) and LaTeX tables summarizing results. All figures must have axis labels, units, legends, and error bars

5. **Statistical code review** (1 task)
   - Agent: Engineer (critique)
   - Dependencies: primary analysis complete
   - Instruction: Review the Analyst's analysis scripts for implementation correctness. Verify that the right test functions were called, data was loaded correctly, and results match the raw data

6. **Hypothesis verdict** (1 task — approval gate)
   - Agent: none (human task — lead interprets results)
   - Dependencies: all analysis tasks + code review complete
   - Instruction: Lead reviews analysis results and decides the verdict:
     - **Supported** → proceed to Phase 6
     - **Rejected** → Loop A (return to Phase 2 for hypothesis revision)
     - **Inconclusive** → Loop B (return to Phase 4 for additional experiments)

## Task Granularity Guidelines

- 1 task = 1 agent invocation
- For primary analysis: 1 task per independent hypothesis (not per metric — a hypothesis may have multiple metrics)
- Figure generation is a single task unless there are 10+ figures (then split by figure group)
- The hypothesis verdict is a mandatory human decision — SKILL.md must not auto-advance

## Completion Condition

Analysis report complete with statistical summary.
See `references/phase_transitions.md` for transition rules and loop triggers (Loop A / Loop B).

## Output Format

All agent reports must follow `references/handoff_protocol.md`.
Analyst reports must include the Statistical Summary table.
