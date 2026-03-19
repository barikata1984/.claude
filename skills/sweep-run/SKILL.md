---
name: sweep-run
description: sweep-run
---

# sweep-run

Launch sweep agents in tmux sessions with optional GPU monitoring. Handles sweep registration,
GPU assignment, agent launch, and resource monitoring in one flow.

## Input

Identify the sweep using one of the following:

- **sweep ID**: ID obtained from `wandb sweep` output (e.g., `entity/project/abc123de`)
- **sweep config YAML**: Path to an unregistered YAML → register with `wandb sweep` first
- **auto-detect**: If neither is provided, list `configs/sweep_*.yaml` and let the user choose

When coming from `/sweep config`, the just-generated YAML path should already be in context.

## Procedure

### 1. Register sweep (if needed)

If the user provides a YAML path instead of a sweep ID:

```bash
wandb sweep <config_path>
```

Capture the sweep ID from the output and confirm it with the user before proceeding.

### 2. Display GPU status

Run `nvidia-smi` and present a summary:

```
GPU  Name           Util%  Memory         Status
  0  RTX 3090       12%    1.2G / 24.0G   Available
  1  RTX 3090       97%   20.1G / 24.0G   In use
  2  RTX 3090        0%    0.4G / 24.0G   Available
```

- Util > 80% or Memory usage > 80% → "In use"
- Otherwise → "Available"

### 3. Defer to user judgment

Ask the user:

- **How many parallel agents** (propose available GPU count as default)
- **Which GPUs to assign** (propose available GPU numbers as default)

### 4. Launch tmux sessions

Launch each agent in a separate tmux session. Infer the working directory from the
project root (where `wandb sweep` should be run from):

```bash
tmux new-session -d -s "<sweep_name>-<short_id>-<N>" \
  "cd <project_root> && CUDA_VISIBLE_DEVICES=<gpu> wandb agent <sweep_id>"
```

### 5. Start GPU monitoring

Start background GPU resource recording alongside the sweep agents:

```bash
tmux new-session -d -s "sweep-monitor-<short_id>" \
  "nvidia-smi --query-gpu=timestamp,index,name,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw \
   --format=csv,nounits -l 30 \
   >> docs/LOGS/gpu_monitor_<sweep_id>_<date>.csv"
```

If a monitoring session already exists, warn and skip.

The monitoring data is consumed by `/sweep analyze` for resource usage analysis.

### 6. Launch confirmation

Display after launch:

```
Launch complete:
  sweep: <sweep_name> (<sweep_id>)
  agents:
    - <session_name_0> → GPU 0
    - <session_name_1> → GPU 2
  monitoring: sweep-monitor-<short_id> → docs/LOGS/gpu_monitor_<id>_<date>.csv

Management commands:
  tmux ls                          # List sessions
  tmux attach -t <session_name>    # Attach to session
  wandb sweep cancel <sweep_id>    # Cancel sweep

When the sweep finishes:
  /sweep analyze                   # Analyze results (also stops monitoring)
```

## Error handling

- If `wandb sweep` fails (not logged in, invalid YAML, etc.), show the error and suggest fixes
- If all GPUs are in use, inform the user and ask whether to wait or proceed anyway
- If a tmux session with the same name already exists, warn and ask before overwriting

## Rules

- GPU assignment is decided by the user — do not auto-assign
- Each agent is pinned to 1 GPU via `CUDA_VISIBLE_DEVICES`
- Infer the project working directory from existing sweep configs or the project root
- Do not overwrite monitoring CSV files; keep them unique by sweep_id + date
