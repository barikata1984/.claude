# Handoff Protocol

Standardized format for agent outputs that enables structured handoff between agents
and between agents and SKILL.md (the task queue manager).

## Report Format

Every agent must produce a report in the following format upon task completion.
SKILL.md parses this output to update the task queue and determine next actions.

```markdown
## [Agent Name] Report
**Phase**: [current phase number]
**Mode**: [execute | critique]
**Status**: [complete | partial | blocked]

### Results
[Detailed findings, implementation summary, or review output]

### External Verification (Engineer only)
| Check | Result | Details |
| ----- | ------ | ------- |
| pytest | PASS/FAIL | [test count, failures] |
| ruff check | PASS/FAIL | [warning count] |
| ruff format | PASS/FAIL | [files changed] |
| pyright | PASS/FAIL/SKIP | [error count] |

### Statistical Summary (Analyst analysis tasks only)
| Comparison | Test | p-value | Effect Size | 95% CI | Verdict |
| ---------- | ---- | ------- | ----------- | ------ | ------- |

### Files Created/Modified
| File | Operation | Description |
| ---- | --------- | ----------- |

### Handoff Notes
- [Items to pass to the next agent or phase]

### Issues & Concerns
- [Problems found, escalation items for the lead]
```

## Field Definitions

### Status

| Value | Meaning | SKILL.md action |
| ----- | ------- | --------------- |
| `complete` | Task finished successfully, all checks passed | Mark task as done, proceed to next |
| `partial` | Task partially done — fixable issues remain | Keep task open, present issues to user |
| `blocked` | Cannot proceed — needs human decision or external dependency | Escalate to user immediately |

### Mode

| Value | Meaning |
| ----- | ------- |
| `execute` | Agent performed its primary function (survey, implement, analyze) |
| `critique` | Agent reviewed another agent's output |

## Critique Mode Output

When an agent operates in critique mode, the Results section must contain:

1. **Verdict**: `PASS` / `REVISE` / `BLOCK`
2. **Specific findings**: Each issue with concrete evidence (line numbers, statistical values, citations)
3. **Suggested fixes**: Actionable recommendations, not vague feedback

Critique verdicts map to SKILL.md actions:

| Verdict | Meaning | SKILL.md action |
| ------- | ------- | --------------- |
| `PASS` | No issues found | Mark critique task as done |
| `REVISE` | Issues found, fixable by the original agent | Create revision task for the original agent |
| `BLOCK` | Fundamental issues requiring phase-level rework | Escalate to user, propose phase regression |

## Cross-Critique Dispatch

Which agent critiques which — self-review is prohibited.

| Critic | Reviews | Focus |
| ------ | ------- | ----- |
| Research | Engineer output | Code-paper consistency, citation accuracy |
| Engineer | Research output | Method section matches implementation |
| Engineer | Analyst output | Statistical code correctness (Phase 5) |
| Analyst | Research output | Claim-evidence alignment, statistical validity |
| Analyst | Engineer output | Experiment design flaws in code |

## Constraints

- An agent must **never** review its own output
- Reports must be self-contained — the next consumer should not need to re-read source files
- The Files Created/Modified table must list every file touched, not just key files
- Handoff Notes should focus on what the next agent needs to know, not what was done
