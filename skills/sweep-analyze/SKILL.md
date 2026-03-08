# sweep-analyze

Retrieve and analyze sweep results via the wandb API, extracting insights.

## Input

Identify the sweep using one of the following:

- **sweep ID**: wandb sweep ID (e.g., `abc123de`)
- **sweep name**: entry name in `log_sweep.md`
- **project specification**: `--project phys-prop-aware` etc. (default: `phys-prop-aware`)

Ask the user for any missing information.

## Procedure

### 1. Data retrieval

Retrieve sweep metadata and run results via the wandb API:

```python
import wandb
api = wandb.Api()
sweep = api.sweep(f"<entity>/<project>/<sweep_id>")
runs = sweep.runs
```

Collect from each run:
- config (hyperparameters)
- summary metrics (final values: val/prior_loss, validation_loss, etc.)
- history (learning curves: loss progression per step)
- state (finished / crashed / running)

### 2. Core analysis

Perform the following analyses and present results:

#### a) Best model identification
- Sort by metric (val/prior_loss or validation_loss) and display top N
- Table of parameters and final metrics for each run

#### b) Per-parameter impact analysis
- Aggregate mean metrics for each value of each search parameter
- Identify which parameters have the greatest impact on performance
- Check for interactions (2-parameter combination effects) if possible

#### c) Learning curve overview
- Compare convergence speed (distribution of early stopping steps)
- Check for divergent or failed runs

#### d) Status summary
- Count of completed / running / failed runs
- Error patterns for failed runs (if any)

#### e) Early stopping configuration assessment
- **Stop step distribution**: Mean and range by parameter condition. Suggest configuration review if there are many extremely early stops or runs hitting the upper limit
- **Patience consumption pattern**: Analyze the gap between best_step and stopped_step. Insufficient if patience is always exhausted, excessive if significantly unused
- **`min_delta_relative` effectiveness**: Compare threshold (SMA × min_delta_relative) with typical val loss fluctuation range. Effectively inactive if threshold is extremely small relative to fluctuations
- **`min_steps` validity**: Compare SMA at min_steps with final SMA. Suggest lowering the value if many runs show clear divergence before min_steps

### 3. Insight extraction

Derive the following from analysis results:

- **Best parameter configuration**: Recommended hyperparameter combination
- **Next step suggestions**: Whether further exploration is needed, or search range can be narrowed
- **Unexpected findings**: Results contradicting hypotheses or interesting patterns

### 4. Record

Append results to the `### Results` section of the corresponding entry in `docs/LOGS/log_sweep.md`:

```markdown
### Results

**Best run**: `<run_id>` (val/prior_loss: <value>)
- <parameter configuration>

**Parameter impact** (by mean metric, descending):
| Parameter | Value | Mean Loss | Std |
|-----------|-------|-----------|-----|
| ...       | ...   | ...       | ... |

**Findings**:
- <key findings in bullet points>

**Early stopping assessment**:
- Stop step: mean <value>K (range <min>K–<max>K)
- Patience consumption: <analysis result>
- min_delta_relative effectiveness: <analysis result>
- Recommended changes: <proposed changes or "current settings are appropriate">

**Next steps**:
- <recommended follow-ups>
```

## Rules

- Assume `wandb login` has already been completed for wandb API access
- Retrieve entity name from `wandb.Api().default_entity`
- Local `wandb/` directory run data may also be used supplementarily
- Round numbers to 4 significant digits
- Present analysis results in conversation first, then append to logs after user confirmation
- Exclude skipped runs (runtime ≈ 0s, from unified sweep pruning) from analysis
