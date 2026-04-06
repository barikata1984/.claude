# Phase 2: Hypothesis Formulation / Experiment Design

Task generation template for the hypothesis and experiment planning phase.
SKILL.md reads this file when entering Phase 2 and generates tasks dynamically
based on the Phase 1 survey report.

## Input

- Phase 1 deliverable: **Survey report** (literature gaps or market analysis)
- If entering via Loop A (hypothesis revision): Phase 5 analysis report with rejection rationale

## Task Generation Rules

### Both Modes

1. **Hypothesis formulation** (1 task)
   - Agent: none (human task — lead formulates the hypothesis)
   - Dependencies: none
   - Instruction: Lead defines a testable hypothesis based on the survey gaps. SKILL.md prompts the lead to provide the hypothesis in one sentence

### Academic Mode

2. **Baseline and evaluation criteria collection** (1 task)
   - Agent: Research (execute)
   - Dependencies: hypothesis formulated
   - Instruction: Identify published baselines to compare against. Collect standard evaluation metrics and benchmark datasets from the survey report

3. **Experiment design — academic** (1 task)
   - Agent: Analyst (execute)
   - Dependencies: hypothesis formulated, baseline collection complete
   - Instruction: Design the experiment plan including:
     - Independent / dependent variables
     - Control conditions and baselines
     - Evaluation metrics with statistical test selection
     - Sample size determination (power analysis)
     - Multiple comparison correction strategy
     - Ablation study plan (which components to ablate)
     - Compute cost estimate (GPU hours × unit cost)

### Startup Mode

2. **Current system baseline** (1 task)
   - Agent: Research (execute)
   - Dependencies: hypothesis formulated
   - Instruction: Document the current system's performance metrics. Identify the minimum improvement threshold for practical significance

3. **Experiment design — startup** (1 task)
   - Agent: Analyst (execute)
   - Dependencies: hypothesis formulated, baseline collection complete
   - Instruction: Design the experiment plan including:
     - A/B test structure (treatment vs control)
     - Primary metric and guardrail metrics
     - Minimum detectable effect (practical significance threshold)
     - Sample size and duration estimate
     - Rollout strategy (percentage ramp)
     - Compute and infrastructure cost estimate

### Both Modes

4. **Experiment plan review** (1 task)
   - Agent: none (human task — approval gate)
   - Dependencies: experiment design complete
   - Instruction: Lead reviews the experiment plan. This is an approval gate: the lead must approve cost/time tradeoffs before proceeding to Phase 3

## Task Granularity Guidelines

- 1 task = 1 agent invocation
- Hypothesis formulation is always a human task (not delegated to agents)
- If the experiment plan covers multiple independent experiments, consider splitting the design task (1 per experiment)
- The approval gate is mandatory — SKILL.md must not auto-advance to Phase 3

## Completion Condition

Experiment plan approved by user (approval gate).
See `references/phase_transitions.md` for transition rules.

## Output Format

All agent reports must follow `references/handoff_protocol.md`.
