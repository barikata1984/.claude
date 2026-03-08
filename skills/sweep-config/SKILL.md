# sweep-config

Generate and validate wandb sweep config YAML based on a sweep plan.

## Input

Obtain sweep configuration from one of the following:

- `/sweep-plan` results (in conversation or latest entry in `docs/LOGS/log_sweep.md`)
- Direct specification from the user (list of parameter names and values)

## Procedure

### 1. Validate base config

1. Load the specified base config YAML
2. Verify compatibility between the `scripts/train.py` entry point and the `command:` section
3. Confirm that `use_wandb: true` is set in the base config

### 2. Generate YAML

Follow the format of existing sweep configs (`configs/sweep_*.yaml`) and generate with this structure:

```yaml
# Sweep config for <brief description of objective>
# Base: <base config name>
# <summary of search space>
#
# Usage:
#   cd catkin_ws/src/osx_bilateral
#   wandb sweep configs/<filename>.yaml
#   wandb agent <sweep_id>

project: phys-prop-aware
name: <sweep_name>
program: scripts/train.py
method: <grid/random/bayes>
metric:
  name: <metric_name>
  goal: minimize

parameters:
  # Dataset
  trainer.dataset-path:
    value: "<dataset_name>"

  # Base config
  config:
    value: <base_config>

  # Fixed overrides (fixed parameters differing from base config)
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

### 3. Validation

Verify the following for the generated YAML:

1. **Parameter name consistency**: CLI argument names (kebab-case) match `TrainingConfig` / `MultiModalConfig` field names
   - Under trainer: `trainer.<field-name>` (e.g., `trainer.batch-size`)
   - Under model: `model.<field-name>` (e.g., `model.embed-dim`)
   - Nested: `model.transformer.<field>`, `model.cvae.<field>`
2. **Value type check**: Verify int/float/bool/str are correct
3. **Combination count**: For grid, compute and display the Cartesian product of all parameter values
4. **Metric name**: `val/prior_loss` for ACT, `validation_loss` for non-ACT
5. **Command section**: If base config is passed via `--config`, ensure command includes `--config` / `configs/...`

### 4. Output

1. Write the generated YAML to `configs/sweep_<name>.yaml`
2. Present the following to the user:
   - Generated file path
   - Execution commands (`wandb sweep` + `wandb agent`)
   - Expected run count and list of search parameters

## Rules

- Match the style and structure of existing sweep configs (header comments, parameter ordering)
- Keep the `command` section consistent with existing files
- Infer base config `--config` specification method from existing sweep configs (`config` parameter vs within `command` section)
- Use CLI format (kebab-case) for parameter names, not Python (snake_case)
