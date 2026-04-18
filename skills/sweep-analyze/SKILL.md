---
name: sweep-analyze
description: Retrieve and analyze wandb sweep results via the wandb API, identify the best run by the sweep's optimization metric, compute per-parameter impact, review learning curves, flag crashed or early-stopped runs, and optionally analyze GPU resource usage from recorded monitoring CSVs. Produces a findings section appended to docs/LOGS/log_sweep.md. Use this skill whenever a sweep has finished (or has enough completed runs) and the user wants to analyze results, pick the best hyperparameter configuration, understand which parameters mattered most, or says things like "analyze the sweep", "what were the best runs", "summarize the sweep results", "which hyperparameters worked", "スイープ結果を分析", "どの設定が良かった". Also trigger when the user provides a wandb sweep ID or references sweep results in conversation.
---

# sweep-analyze

Retrieve and analyze wandb sweep results, extract insights, and optionally analyze GPU resource usage.

## Input

Identify the sweep using one of the following:

- **sweep ID**: wandb sweep ID (e.g., `abc123de` or `entity/project/abc123de`)
- **sweep name**: entry name in `docs/LOGS/log_sweep.md`
- **project specification**: `--project <name>` (default: infer from existing sweep configs or ask)

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

Retrieve entity from `wandb.Api().default_entity`. Collect from each run:
- config (hyperparameters)
- summary metrics (final values)
- history (learning curves)
- state (finished / crashed / running)

Identify the sweep's optimization metric from `sweep.config["metric"]` rather than
assuming a specific metric name.

### 2. Core analysis

#### a) Best model identification
- Sort by the sweep's optimization metric and display top N
- Table of parameters and final metrics for each run

#### b) Per-parameter impact analysis
- Aggregate mean metrics for each value of each search parameter
- Identify which parameters have the greatest impact on performance
- Check for interactions (2-parameter combination effects) if feasible

#### c) Learning curve overview
- Compare convergence speed (distribution of stopping steps)
- Check for divergent or failed runs

#### d) Status summary
- Count of completed / running / failed runs
- Error patterns for failed runs (if any)

#### e) Early stopping assessment (if applicable)

Only include this section if the training framework uses early stopping. Analyze:

- **Stop step distribution**: Mean and range by parameter condition
- **Patience consumption**: Gap between best_step and stopped_step — is patience too tight or too loose?
- **Stopping threshold effectiveness**: Is the threshold actually triggering stops, or is it effectively inactive?

### 3. GPU resource analysis (if monitoring data exists)

Check for `docs/LOGS/gpu_monitor_*<sweep_id>*.csv`. If found:

1. Stop the monitoring session if still running:
   ```bash
   tmux kill-session -t "sweep-monitor-<short_id>" 2>/dev/null
   ```

2. Read the CSV and present:

   **Per-GPU summary**:
   | GPU | Util% (mean/p95) | Memory (mean/max) | Power (mean) |
   |-----|------------------|-------------------|--------------|

   **Key observations**:
   - Memory stability (any signs of leaks?)
   - GPU idle valleys during batch loading
   - Whether any GPU was underutilized enough to share

3. Include in the log entry under `### Resource usage`.

If no monitoring data exists, skip this section silently.

### 4. Insight extraction

Derive from the analysis:

- **Best parameter configuration**: Recommended hyperparameter combination
- **Next step suggestions**: Further exploration needed, or narrow the range?
- **Unexpected findings**: Results contradicting hypotheses or interesting patterns

### 5. Record

Present results in conversation first, then after user confirmation append to
the corresponding entry in `docs/LOGS/log_sweep.md`:

```markdown
### Results

**Best run**: `<run_id>` (<metric_name>: <value>)
- <parameter configuration>

**Parameter impact** (by mean metric, descending):
| Parameter | Value | Mean | Std |
|-----------|-------|------|-----|
| ...       | ...   | ...  | ... |

**Findings**:
- <key findings in bullet points>

**Next steps**:
- <recommended follow-ups>
```

If early stopping assessment or resource usage data is available, append those sections too.

## Error handling

- If wandb API connection fails, suggest checking `wandb login` status
- If the sweep has no completed runs yet, report status and suggest waiting
- If runs crashed, extract error messages from run logs when possible

## Rules

- Retrieve entity name from `wandb.Api().default_entity`
- Infer the optimization metric from the sweep config — do not hardcode metric names
- Local `wandb/` directory run data may also be used supplementarily
- Round numbers to 4 significant digits
- Exclude skipped runs (runtime ≈ 0s) from analysis
- Present results in conversation first, then append to logs after user confirmation
