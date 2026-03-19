---
name: sweep-config
description: sweep-config
---

# sweep-config

Generate and validate wandb sweep config YAML.

## Input

Obtain sweep configuration from one of the following:

- Planning results from `/sweep plan` (in conversation or latest entry in `docs/LOGS/log_sweep.md`)
- Direct specification from the user (parameter names and values)

## Procedure

### 1. Discover project context

Before generating, read the project to understand its conventions:

1. **Existing sweep configs**: Glob `configs/sweep_*.yaml` and read 1-2 examples to learn the project's YAML style (header comments, parameter naming, command section format)
2. **Training entry point**: Identify the training script and how it accepts arguments (from existing configs or project structure)
3. **Config classes**: If the project uses typed configs (dataclass, pydantic, etc.), read them to understand parameter names, types, and defaults
4. **wandb project name**: Extract from existing configs or ask the user

### 2. Generate YAML

Follow the discovered conventions. A typical structure looks like:

```yaml
# Sweep config for <brief description of objective>
# Base: <base config name>
# <summary of search space>
#
# Usage:
#   wandb sweep configs/<filename>.yaml
#   wandb agent <sweep_id>

project: <wandb_project>
name: <sweep_name>
program: <training_script>
method: <grid/random/bayes>
metric:
  name: <metric_name>
  goal: <minimize/maximize>

parameters:
  # Fixed parameters
  ...

  # === Sweep parameters ===
  <parameter>:
    values: [...]

command:
  - ${env}
  - python3
  - ${program}
  - ${args}
```

Adapt this template to match the project's existing sweep config style. If the project
uses a different format (e.g., `--config` flag, nested parameters), follow that convention.

### 3. Validation

Verify the generated YAML:

1. **Parameter name format**: Match the CLI argument convention used by the training script (kebab-case, snake_case, dot-notation, etc.) — infer from existing configs
2. **Value type check**: Verify int/float/bool/str types match the config class definitions
3. **Combination count**: For grid search, compute and display the Cartesian product count
4. **Metric name**: Infer from existing configs or wandb project. If ambiguous, ask the user
5. **Command section**: Ensure consistency with existing sweep configs

### 4. Output

1. Write the generated YAML to `configs/sweep_<name>.yaml`
2. Present to the user:
   - Generated file path
   - Execution commands (`wandb sweep` + `wandb agent`)
   - Expected run count and list of search parameters
3. Ask: "Register this sweep and launch agents now? (`/sweep run`)"

## Rules

- Match the style and structure of existing sweep configs in the project
- Infer project-specific details (entry point, config passing method, parameter naming) from existing files rather than assuming
- Use the CLI format the project actually uses for parameter names
- If no existing sweep configs exist, ask the user about the training script interface
