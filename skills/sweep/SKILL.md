# sweep

Unified entry point for sweep experiment management. Routes to sub-skills based on arguments or context.

## Usage

```
/sweep              → Auto-detect from context
/sweep plan         → Plan the experiment (/sweep-plan)
/sweep config       → Generate sweep config YAML (/sweep-config)
/sweep run          → Launch sweep agents in tmux (/sweep-run)
/sweep monitor      → Start GPU resource monitoring (/sweep-monitor)
/sweep analyze      → Analyze sweep results (/sweep-analyze)
/sweep full         → Run plan → config → run + monitor → analyze in sequence
```

## Auto-detection logic

When called without arguments, determine the sub-skill in the following priority order:

1. Conversation mentions sweep results or a sweep ID → **analyze**
2. A sweep is running (tmux sessions exist) → present **monitor** status check
3. Conversation contains `/sweep-plan` results (parameters already selected) → **config**
4. None of the above → start with **plan**

## Full mode

When `/sweep full` is specified, execute the following in sequence:

1. `/sweep-plan` — Clarify objectives and select parameters
2. `/sweep-config` — Generate and validate YAML
3. `/sweep-run` — Display GPU status → user decides → launch agents in tmux
4. `/sweep-monitor` — Start resource monitoring (in parallel)
5. (When called again after sweep completion) `/sweep-analyze` — Analyze results + aggregate monitoring data

Obtain user approval between each phase before proceeding to the next.

## Shared context

References common to all sub-skills:

- **Project config**: `src/training/config.py`, `src/models/configs/multi_modal_config.py`
- **wandb utilities**: `src/training/wandb_utils.py`
- **Existing sweep configs**: `configs/sweep_*.yaml`
- **Experiment logs**: `docs/LOGS/log_sweep.md`
- **GPU monitoring data**: `docs/LOGS/gpu_monitor_*.csv`
- **Strategy document**: `docs/archive/wandb_sweep_unified_strategy.md`
