# sweep-monitor

Periodically record GPU resource usage during sweep execution. Accumulate data for establishing future automated GPU assignment criteria.

## Purpose

- Record actual GPU utilization and memory consumption for each model × batch size × GPU combination during sweeps
- Accumulate this data to enable quantitative decisions about whether "this model configuration can share a GPU" in the future

## Procedure

### 1. Start monitoring

Start background recording in a tmux session:

```bash
tmux new-session -d -s "sweep-monitor" \
  "nvidia-smi --query-gpu=timestamp,index,name,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw \
   --format=csv,nounits -l 30 \
   >> docs/LOGS/gpu_monitor_<sweep_id>_<date>.csv"
```

- Sampling interval: 30 seconds (`-l 30`)
- Output: `docs/LOGS/gpu_monitor_<sweep_id>_<YYYYMMDD>.csv`

### 2. Stop monitoring

Terminate the tmux session after sweep completion or via `/sweep-monitor stop`:

```bash
tmux kill-session -t sweep-monitor
```

### 3. Data analysis

Read the recorded CSV and aggregate/present the following:

#### a) Per-GPU summary
| GPU | Util% (mean/max/p95) | Memory (mean/max) | Power (mean) |
|-----|----------------------|--------------------|--------------|
| 0   | 45% / 98% / 92%     | 8.2G / 12.1G       | 180W         |

#### b) Time-series patterns
- Util% range during steady-state training
- Presence and depth of valleys (GPU idle) during batch loading
- Memory usage stability (any signs of leaks)

#### c) Parallelization feasibility assessment
Per GPU:
- **util p95 < 50% AND memory max < 50%**: Possible to co-locate 2 agents on the same GPU
- **util p95 > 80%**: Compute saturated, sharing not possible
- **memory max > 70%**: Insufficient memory headroom, sharing not possible

### 4. Record

Append analysis results to the corresponding entry in `docs/LOGS/log_sweep.md`:

```markdown
### Resource usage
- Monitoring period: <start> – <end>
- Data: `docs/LOGS/gpu_monitor_<id>_<date>.csv`

| GPU | Util% (mean/p95) | Memory (mean/max) | Co-location feasible |
|-----|-------------------|--------------------|----------------------|
| ... | ...               | ...                | ...                  |
```

## Rules

- Monitoring can also be used for non-sweep training (standalone `train.py` runs)
- Do not overwrite CSV files; keep them unique by sweep_id + date
- If a monitoring session (`sweep-monitor`) already exists, warn and do not launch another
- Present analysis results in conversation first, then append to logs after user confirmation
