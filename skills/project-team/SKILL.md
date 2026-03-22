---
name: project-team
description: "Manage a robot learning research project with a team of 3 AI agents (Research, Engineer, Analyst). Orchestrates project phases (1-8), generates tasks from phase templates, dispatches agents, runs external verification, and tracks state across sessions. Use when the user says /project-team, project team, start project, next task, check in, phase status, or wants to manage a multi-phase research or startup project with agent collaboration."
---

# Project Team

Task queue manager for multi-phase robot learning projects.
You orchestrate 3 agents (Research, Engineer, Analyst) across 8 project phases,
persisting state between sessions so work can resume at any point.

## Usage

```
/project-team              → Check in: read state, show remaining tasks, propose next action
/project-team phase <N>    → Move to Phase N and generate tasks
/project-team status       → Show current phase, task queue, and loop counts
/project-team init         → Initialize a new project (set mode and create state file)
```

## Core Loop

Every invocation follows this sequence:

```
1. READ state file
2. ROUTE by command (init / phase / status / default check-in)
3. PRESENT options to user
4. DISPATCH agent or record human task completion
5. RECEIVE agent report
6. VERIFY (external tools if applicable)
7. UPDATE state file
8. PROPOSE next action
```

## Step 1: Read State

Read the project state file. The default location is `docs/LOGS/log_project_team.md`.
If it does not exist, prompt the user to run `/project-team init`.

Parse the following from the state file header:

- **Mode**: `academic` or `startup`
- **Current phase**: 0–8
- **Loop counts**: (A)N (B)N (C)N (D)N

Then parse the task queue table for the current phase (if it exists).

## Step 2: Route

### `/project-team init`

1. Ask the user: academic or startup mode?
2. Ask for a one-line project description
3. Create the state file with this template:

```markdown
# Project State

- Mode: [academic | startup]
- Current phase: 0
- Loop counts: (A)0 (B)0 (C)0 (D)0
- Description: [one-line project description]

## History

| Date | Phase | Event |
| ---- | ----- | ----- |
| YYYY-MM-DD | 0 | Project initialized |
```

4. Tell the user: "Phase 0 (Ideation) is a human task. Define the problem you want to solve, then run `/project-team phase 1` to begin."

### `/project-team status`

Display:
- Current mode and phase
- Loop counts
- Task queue summary (N done / M total, next task)
- Blockers (any task with status = blocked)

### `/project-team phase <N>`

1. Validate the transition against `references/phase_transitions.md`
   - Check completion condition of current phase
   - Check approval gates (phases 2→3, 5→6, 7→8)
2. If valid, update state file: set current phase to N
3. Generate tasks (see Step 3 below)
4. If invalid, explain why and suggest what needs to happen first

### Default check-in (`/project-team`)

1. If task queue exists and has pending tasks → present them and ask which to work on
2. If task queue exists and all tasks are done → evaluate phase completion (see Step 6)
3. If no task queue → generate tasks for the current phase (see Step 3)

## Step 3: Generate Tasks

When entering a new phase that has a definition file:

1. Read the phase definition file from `phases/phase<N>-*.md`
2. Read deliverables from the previous phase (files listed in the last completed task queue)
3. Apply mode-specific rules (academic vs startup sections in the phase file)
4. Generate a task queue table:

```markdown
## Phase N Task Queue

| ID | Task | Agent | Mode | Dependencies | Status | Completed |
| -- | ---- | ----- | ---- | ------------ | ------ | --------- |
| N.1 | [task description] | [Research/Engineer/Analyst/(human)] | [execute/critique] | - | pending | |
| N.2 | ... | ... | ... | N.1 | pending | |
```

5. Present the generated tasks to the user for approval
6. On approval, write the task queue to the state file
7. On rejection, ask what to change and regenerate

**Phases without definition files** (0, 4, 8):
- Phase 0: Human-only. No tasks to generate
- Phase 4: Delegate to `/sweep run` if applicable. Otherwise, inform the user this is a human/compute phase
- Phase 8: Delegate to `/commit-and-push` if applicable. Otherwise, inform the user this is a human decision

## Step 4: Dispatch Agent

When the user selects a task:

1. Check dependencies — all dependent tasks must be `done`
2. If the task agent is `(human)`, ask the user to confirm completion and provide deliverables
3. If the task agent is an AI agent, launch it using the Agent tool:

```
Agent(
  subagent_type: "general-purpose",
  prompt: [constructed from task description + phase context + agent definition reference]
)
```

**Prompt construction** for agent dispatch:

```
You are the [Agent Name] Agent. Follow the instructions in agents/pt-[agent].md.

## Task
Phase: [N]
Mode: [execute | critique]
Task: [task description from the queue]

## Context
[Relevant deliverables from previous tasks/phases]
[Mode: academic | startup]

## Output
Report your results following references/handoff_protocol.md.
```

## Step 5: Process Agent Report

After the agent returns:

1. Parse the report for Status (complete / partial / blocked) and Mode (execute / critique)
2. If critique mode, also parse Verdict (PASS / REVISE / BLOCK)

### Status handling

| Status | Action |
| ------ | ------ |
| `complete` | Mark task as `done` with today's date |
| `partial` | Keep task as `in-progress`, present issues to user |
| `blocked` | Mark task as `blocked`, escalate to user immediately |

### Critique verdict handling

| Verdict | Action |
| ------- | ------ |
| `PASS` | Mark critique task as `done` |
| `REVISE` | Create a revision task for the original agent (Loop D if in Phase 7) |
| `BLOCK` | Escalate to user. If in Phase 7, propose Loop C (regression to Phase 3 or 4) |

## Step 6: External Verification

After Engineer execute-mode tasks in Phase 3 and Phase 7 Round 1:

1. Run verification commands and capture output:

```bash
python -m pytest tests/ -v 2>&1 | tail -20
ruff check . 2>&1 | tail -10
ruff format --check . 2>&1 | tail -10
pyright 2>&1 | tail -10  # only if pyright is installed
```

2. Record results in the state file under the task
3. If any check fails:
   - In Phase 3: keep task as `in-progress`, ask the agent to fix
   - In Phase 7 Round 1: auto-set REVISE status, create fix task

## Step 7: Update State File

After each task completion or status change:

1. Update the task row in the state file (status + completion date)
2. If a new task was generated (revision, re-review), append it to the task queue
3. If a loop was triggered, increment the loop counter and log it in History

### Phase completion check

When all tasks in a phase are `done`:

1. Read completion conditions from `references/phase_transitions.md`
2. Check approval gates
3. If conditions met, propose advancing to the next phase
4. Log the phase completion in History

### Loop detection

Read `references/phase_transitions.md` for loop definitions.
When a loop is triggered:

1. Increment the relevant loop counter (A/B/C/D)
2. Check against escalation thresholds (A>3, B>2, C>1)
3. If threshold exceeded, warn the user and propose escalation action
4. Log the loop in History

## Step 8: Propose Next Action

After updating state, always end by proposing the next action:

- If there are remaining tasks with met dependencies → suggest the next task
- If all tasks are done → suggest phase transition
- If blocked → summarize blockers and ask for guidance
- If the session is getting long → suggest wrapping up with `/wrap-up-session`

## Existing Skill Delegation

| Situation | Delegate to |
| --------- | ----------- |
| Phase 1 needs 30+ paper survey | `/literature-survey` |
| Phase 4 hyperparameter sweep | `/sweep run` |
| Phase 5 sweep result analysis | `/sweep analyze` |
| Phase 3-5 bug encountered | `/fault-tree-debug` |
| Phase 6 citation verification | `/reference-verify` |
| Phase completion milestone | `/commit` |
| Phase 8 publication/release | `/commit-and-push` |
| Session end | `/wrap-up-session` |

## Rules

- Never auto-advance past an approval gate. Always ask the user
- Never skip external verification after Engineer tasks
- Never let an agent self-review (same agent critiquing its own output)
- Follow the cross-critique dispatch in `references/handoff_protocol.md`
- Keep task granularity at 1 task = 1 agent invocation
- Log every phase transition and loop in the History table
- If uncertain about phase transition validity, check `references/phase_transitions.md`
- State file is the single source of truth — always read before acting, always write after acting
