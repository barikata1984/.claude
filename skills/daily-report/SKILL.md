---
name: daily-report
description: "Generate a structured daily work report. Extracts the day's work from docs/LOGS/ logs, docs/TODO.md, and git log, then saves it as a structured report for management in docs/REPORTS/. Invoke with /daily-report or /daily-report YYYY-MM-DD. Also trigger for requests like daily report, work summary, progress report, today's work summary."
---

# daily-report

Extract the day's work from docs/ and git log, and generate a report for management.

## Arguments

- No arguments → targets today (JST)
- `YYYY-MM-DD` → targets the specified date

## Procedure

### 1. Determine target date and extract git log

The server runs in PST (UTC-8). The offset from JST (UTC+9) is 17 hours.

PST range for target date `YYYY-MM-DD` (JST):
- Start: `YYYY-MM-(DD-1)T07:00:00` PST
- End: `YYYY-MM-DDT07:00:00` PST

Retrieve git log from both the osx_bilateral submodule and the parent repository:

```bash
# osx_bilateral
cd catkin_ws/src/osx_bilateral
git log --since="<start>" --until="<end>" --format="%h %ai %s"

# Parent repository
cd /root/osx-ur
git log --since="<start>" --until="<end>" --format="%h %ai %s"
```

### 2. Read sources

Read the following files:

- `docs/TODO.md` — completed `[x]` and pending `[ ]` items
- `docs/ISSUES.md` — newly registered and resolved issues
- `docs/LOGS/log_*.md` — sections appended on the target date (identify via git diff or date headers)
- `docs/PLAN.md` — if there were design changes

Cross-reference git log commit messages with log content to determine the scope of work for the target date.

### 3. Topic integration (most important)

Multiple entries about the same theme (investigation 1 → investigation 2, analysis → fix, etc.)
should be **consolidated into a single topic centered on the conclusion**. Keep the background
to the minimum necessary for understanding the conclusion.

Integration rules:
- When investigation/analysis/implementation for the same theme spans multiple steps, state the
  final conclusion first, then briefly reference preceding steps as reasons leading to that conclusion
- Include specific numerical data (loss values, test results, statistical tests)
- List changed files in table format
- Include "investigated but decided not to change" as well (valuable as a record of decisions)

### 4. Report structure

```markdown
# Work Report — YYYY-MM-DD

## 1. [Topic name]

### Conclusion / Summary
(Conclusion first. 1-3 sentences)

### Background
(Context leading to the conclusion. Only if necessary)

### Changes
(File change table, test results)

## 2. [Next topic]
...

## References

(Only if citations are used in this report)

- [[Key]](../REFERENCES/MAIN.md#Key) — Brief summary of why cited

---

**Commits today**: N (osx_bilateral) + M (parent repository)
**Final test status**: X passed, Y skipped
```

Granularity per topic:
- Large investigation + implementation → 3 sections: Conclusion / Background / Changes
- Small fix → 1 section: Summary only
- Design/planning → Summary + Design details

### 5. Save

Output to: `docs/REPORTS/YYYY-MM-DD.md`

Create the directory if it does not exist. If a file with the same name already exists, confirm with the user.

## Reference processing

Follow the citation conventions in `.claude/rules/references.md`.

## Rules

- Language is Japanese (fixed)
- Conclusion first. The manager should grasp the key point from the first sentence
- Avoid verbose background explanations; focus on decisions and results
- Include specific numbers ("improved by 3-5%" not "improved")
- Always include test results
- Do not include work not recorded in logs (do not speculate)
