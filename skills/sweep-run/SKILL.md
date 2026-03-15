# sweep-run

Launch sweep agents in tmux sessions. Display GPU status and determine parallelism and GPU assignment based on user decisions.

## Input

Identify the sweep using one of the following:

- **sweep ID**: ID obtained from `wandb sweep` output (e.g., `entity/project/abc123de`)
- **sweep config**: Unregistered YAML path → register with `wandb sweep` first, then launch agents

## Procedure

### 1. Display GPU status

Run `nvidia-smi` and present the following to the user:

```
GPU  Name           Util%  Memory         Status
  0  RTX 3090       12%    1.2G / 24.0G   Available
  1  RTX 3090       97%   20.1G / 24.0G   In use
  2  RTX 3090        0%    0.4G / 24.0G   Available
```

- GPUs with Util > 80% or Memory usage > 80% are shown as "In use"
- Others are shown as "Available"

### 2. Defer to user judgment

Ask the user:

- **How many parallel agents to launch** (propose available GPU count as default)
- **Which GPUs to assign** (propose available GPU numbers as default)

### 3. Launch tmux sessions

Based on user specifications, launch each agent in a separate tmux session:

```bash
# Session naming: <sweep_name>-<short_sweep_id>-<agent_number>
tmux new-session -d -s "<name>-<id>-0" \
  "cd catkin_ws/src/osx_bilateral && CUDA_VISIBLE_DEVICES=<gpu> wandb agent <sweep_id>"

tmux new-session -d -s "<name>-<id>-1" \
  "cd catkin_ws/src/osx_bilateral && CUDA_VISIBLE_DEVICES=<gpu> wandb agent <sweep_id>"
```

### 4. Launch confirmation

Display the following after launch:

```
Launch complete:
  sweep: <sweep_name> (<sweep_id>)
  sessions:
    - <session_name_0> → GPU 0
    - <session_name_1> → GPU 2

Management commands:
  tmux ls                          # List sessions
  tmux attach -t <session_name>    # Attach to session
  wandb sweep cancel <sweep_id>    # Cancel sweep
```

## Rules

- GPU assignment is decided by the user. Do not auto-assign
- Each agent is pinned to 1 GPU via `CUDA_VISIBLE_DEVICES`
- If no sweep ID is provided, list `configs/sweep_*.yaml` and let the user choose
- Warn if a tmux session with the same name already exists
- Separate `wandb sweep` registration and `wandb agent` launch, making the sweep ID explicit
