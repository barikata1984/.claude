---
name: plan-to-implement
description: Triage an implementation task into single-agent vs parallel-team execution, and for team execution, negotiate a frozen interface contract before any code is written. Use this skill whenever the user asks to implement, build, or add a non-trivial feature that might decompose into several parts — especially when they say "implement X", "build X", "add X", or invoke /implement. The skill decides whether the work is better done by one agent (coupled or exploratory work) or by a team of function-owning agents that agree on interfaces first (breadth work with nameable seams). Do NOT use for a one-line edit, a bug fix in a known spot, or pure investigation — those need no decomposition.
---

# plan-to-implement

Decide **how** to implement a task before implementing it: one agent, or a team of function-owning agents that agree on their interfaces first. The point is not raw speed. It is to move the burden of keeping interfaces consistent off the operator and onto a planning phase, so that a task which outgrows a single person's attention can still be built coherently.

This skill covers Stage 1 (the minimal working version). It runs the triage, and — for team execution — the interface negotiation and the parallel build. It does not yet do large-N recursive splitting or mid-implementation re-negotiation.

## The triage gate

Answer two questions about the task. Both are decided during the Explore phase below, not guessed up front.

1. **Breadth or depth?**
   - **Breadth** = many largely independent pieces (several endpoints, several modules, several call-sites). Leans **team**.
   - **Depth** = one tightly-coupled thing whose parts share state and evolve together. Leans **single**.
2. **Can you name the seams right now?** A seam is the contract between two pieces, stated concretely enough that two agents could build opposite sides without talking: a function signature, an API/endpoint shape, a data schema, a module's public interface.
   - If you can write each seam as one line such that the pieces would fit on first integration → seams are nameable.
   - If the honest answer is "I'll discover the boundary while coding" → seams are **not** nameable. The task is still exploratory.

**Decision:** Go **team** only when the work is breadth **and** the seams are nameable. Otherwise go **single**. Non-nameable seams are not a failure — they mean the task is in its exploratory phase, where one agent holding the whole context is the right tool.

## Flow

### Phase 0 — Explore (always)

Spawn an **Explore** subagent (read-only agent type; its read-only property comes from tool restriction, so it holds even under auto mode) to investigate the task and codebase. It should return:
- What the task requires and what already exists.
- The language / framework / conventions in use, so the frozen-contract artifact form (below) follows from the codebase rather than a guess.
- A proposed decomposition into functional components (F1, F2, …), or the finding that the work does not cleanly decompose.

The Explore result is a **proposal**. The orchestrator (you) owns the final decomposition and may revise the component list before proceeding.

Using the Explore result, answer the two triage questions and decide single vs team. Two shortcuts:
- If Explore reports the work **does not cleanly decompose**, that is by definition depth + non-nameable seams → go **single** (Phase 1a) without further deliberation.
- If there is genuinely **nothing to explore** (e.g. a greenfield task with no existing code to read), record that as the Explore finding and proceed straight to the triage questions.

### Phase 1a — Single-agent path

If the triage says **single**: dispatch one `general-purpose` subagent (or do it inline for small work) with the whole task in one context. No contract, no team. Done after it returns.

### Phase 1b — Team path: negotiate a frozen contract

If the triage says **team**, create a team (follow `~/.claude/rules/agent-teams.md` for the mechanics) with:
- One **function-owner** agent per functional component (F1, F2, …).
- One **interface agent** acting as a hub.

Then run this negotiation loop. It is **function-driven**: interfaces exist to connect functions, not the reverse.

0. **Setup (not a round):** each function-owner declares its I/O demands — what it needs as input and what it will produce as output, in its own terms.
1. **The interface agent reconciles** the declared demands into a concrete contract proposal (function signatures / schemas / endpoint shapes). It has **arbitration authority**: when two demands conflict, it surfaces the conflict and forces a tradeoff decision rather than silently picking one.
2. **Each function-owner reviews** the proposal and returns OK or a specific objection.

One **round** = one reconcile→review cycle (steps 1–2). The initial declaration is setup, not a round. Repeat the cycle until all function-owners return OK, bounded to **3 rounds** (exactly three reconcile→review cycles).

The hub's arbitration decision is **final within its round**. When a function-owner objects, the hub first **classifies the objection** before it consumes a round:
- **A new technical fact** (a real constraint the proposal violates, e.g. "a sync trait blocks the async runtime"): legitimate — the hub re-reconciles and this consumes a round.
- **A preference that contradicts a fixed requirement** (the owner pushes a design the user's spec rules out, e.g. a file trailer when the spec mandates a header line): the hub **overrides it immediately** and the owner must comply — this does **not** consume the bound. Convergence is then judged on the post-override state of the current cycle; an override does not require a fresh cycle or a re-announcement of the unchanged proposal.

A persistent *technical* objection consumes rounds and, if unresolved after the 3-round bound, triggers the not-converged fallback below. The loop never deadlocks: a standoff simply reaches the bound and falls back.

**Termination:**
- **Converged** (all OK): freeze the contract as a concrete artifact **written to a file** — stub files, type/interface declarations, or a schema, placed at a path in the repo (or a scratch path if the repo location is not yet decided). Announce that path to every function-owner. This artifact is a deliverable in its own right, and it is what Phase 2 agents read.
- **Not converged after 3 rounds:** never freeze over the conflict. Choose the fallback by the conflict's **source**, not by assuming the decomposition is at fault:
  - **Structural** — the seam itself is drawn wrong, or owners cannot agree on boundaries: **re-decompose** and retry once. The retry re-enters Phase 1b with a fresh 3-round bound; if it also fails to converge, escalate to the user rather than re-decomposing a second time.
  - **Hard-requirement tension** — the requirements themselves conflict, so no decomposition resolves it (e.g. bounded memory vs. an exact whole-dataset header): **escalate to the user** with the specific tradeoff and options.
  - **Irreconcilable but low-stakes** — no principled resolution and it does not warrant the user's time: **drop to the single-agent path** and let one agent make the call in context.

Communication in this phase is via team messaging routed **through the interface hub** (function-owners negotiate with the hub, not pairwise), to keep coordination cost linear in the number of components.

### Phase 2 — Parallel implementation

With the contract frozen, each function-owner implements its component **by reading the frozen artifact file** (at the path announced in Phase 1b), in parallel. No messaging in this phase: the contract is fixed. If a function-owner finds the frozen contract genuinely cannot be implemented, stop and report it — that is a signal the negotiation was too shallow, not a cue to renegotiate ad hoc (mid-implementation renegotiation is a later stage, not part of this one).

## Rules

- **Explore before deciding.** Never pick single vs team without the Explore result. Guessing the decomposition is the main failure mode.
- **Read-only exploration uses the Explore agent type**, not `permissionMode: plan` (which is ignored under auto mode).
- **The contract is frozen before Phase 2 begins.** Phase 2 agents read it; they do not message each other.
- **Non-convergence is an outcome, not an error to suppress.** Fall back or escalate; never freeze over an unresolved conflict.
- **Interface work serves the functions.** The interface agent reconciles and arbitrates; it does not dictate the design.
- **Scope:** this is Stage 1. If the component count is large enough that hub negotiation itself becomes unwieldy, say so and stop — recursive meta-splitting is out of scope here.
