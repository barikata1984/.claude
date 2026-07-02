---
name: implement
description: Ergonomic entry point for implementing a non-trivial feature or task. Delegates to the plan-to-implement skill, which triages the work into single-agent vs parallel-team execution and, for team execution, negotiates a frozen interface contract before coding. Use this skill whenever the user says "implement X", "build X", "add feature X", "/implement", or otherwise asks to build something that may decompose into parts. Do NOT use for a one-line edit, a bug fix in a known spot, or pure investigation.
---

# implement

Thin entry point. When invoked, follow `~/.claude/skills/plan-to-implement/SKILL.md` and execute the task through it.

This skill exists so the user can trigger the plan-to-implement flow with a single short invocation. It adds no logic of its own — all triage, negotiation, and build behavior is defined in plan-to-implement.
