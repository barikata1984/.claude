---
name: fault-tree-debug
description: "MANDATORY debugging methodology. You MUST use this skill for ANY bug investigation, test failure, error diagnosis, or troubleshooting task — even if you think you can handle it without a skill. This skill provides the Fault Tree Analysis (FTA) framework that prevents the #1 AI debugging failure: jumping to one hypothesis without considering alternatives. Trigger on: NaN, crash, test failure, wrong output, assertion error, flaky test, regression, performance issue, memory leak, divergence, oscillation, timeout, data corruption, silent error, shape mismatch, type error — any symptom the user wants investigated. Also trigger on phrases like: debug, find the root cause, why is this failing, investigate, what's wrong, look into this error, this doesn't work, something is broken, fix this bug, 調べて, 原因, バグ, エラー, 落ちる, 動かない, おかしい, 壊れた. If the user describes a symptom and asks you to find the cause, USE THIS SKILL."
---

# Fault Tree Debug

Systematic debugging via Fault Tree Analysis. The core discipline:
**enumerate all plausible causes before investigating any of them.**

You (like all AI agents) tend to latch onto the first plausible hypothesis. This
skill counteracts that by forcing structured enumeration, prediction-driven
investigation, and explicit elimination of alternatives before declaring a root cause.

## Phase 0: Triage

Not every bug needs a full fault tree. Quick-check first:
1. Does the linter / type checker catch it?
2. Does `git log --oneline -10` reveal an obvious culprit?
3. Is the error message self-explanatory with a single unambiguous cause?

If yes, fix and move on. Full FTA is for cases where the cause isn't obvious.

## Phase 1: Top Event

State the failure precisely — **what** is observed, **when** it occurs, and
**reproducibility**. Write it down before proceeding.

## Phase 2: Build the Fault Tree

**Do this BEFORE reading any source code related to the bug.** Reading code first
anchors you to whatever you see first.

Walk through each cause category and ask "could this produce the top event?"
Write a one-line hypothesis for each plausible category. For excluded categories,
state why in one line.

| # | Category | Ask yourself |
|---|----------|-------------|
| 1 | **Logic error** | Wrong condition, algorithm, off-by-one? |
| 2 | **State corruption** | Stale/uninitialized/shared mutable state? |
| 3 | **Race condition** | Concurrent access or timing dependency? |
| 4 | **Configuration** | Wrong env var, config value, feature flag? |
| 5 | **Dependency** | Library version, API change, external service? |
| 6 | **Data** | Unexpected input, schema mismatch, encoding? |
| 7 | **Environment** | OS, runtime version, container difference? |
| 8 | **Resource exhaustion** | Memory, disk, connections, file descriptors? |

For each plausible hypothesis, note whether sub-causes combine as OR (any one
suffices) or AND (multiple must co-occur). Rank the hypotheses: single-cause
explanations first, then multi-factor combinations.

## Phase 3: Investigation Plan

Rank hypotheses by: (1) probability, (2) verification cost (cheap checks first),
(3) information value (checks that eliminate multiple branches at once).

Create a numbered investigation order.

## Phase 4: Investigate

For **each** step:

1. **Predict**: State what you expect if the hypothesis is true vs false —
   before looking at any evidence. This prevents post-hoc rationalization.
2. **Observe**: Do the minimum action that distinguishes true from false.
   See `references/investigation_map.md` for concrete actions per category.
3. **Update all branches**: Evidence from one investigation often eliminates
   or strengthens other branches. Record cross-branch implications.

Guard against tunnel vision: if 3-4 steps on one branch don't converge, move
to the next branch. When you find supporting evidence, ask yourself what would
*contradict* it and whether any alternative explanations remain.

## Phase 5: Converge

Declare root cause **only** when all four conditions hold:

| Condition | Meaning |
|-----------|---------|
| **Reproduction** | You can reliably trigger the failure |
| **Isolation** | Specific code/config identified |
| **Mechanism** | You can explain *how* it produces the symptoms |
| **Exclusion** | Alternatives ruled out by evidence, not assumption |

If the bug has multiple contributing causes (AND-gate), report all of them
and their interaction.

## Avoid

- Declaring the cause before investigating alternatives
- Announcing root cause after checking only one branch
- Making speculative fixes without understanding the mechanism
- Treating error messages as root causes (they describe symptoms)
- Reading code before building the tree

## Report

1. **Top event** / **Root cause** / **Mechanism** (how cause → symptoms)
2. **Key evidence** that confirmed the cause
3. **Fix** and why it works
4. **Eliminated hypotheses** with the evidence that ruled each out
