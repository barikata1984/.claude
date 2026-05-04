---
name: daily-report
description: "Generate a structured daily work report. Extracts the day's work from notes/LOGS/ logs, notes/TODO.md, and git log (or docs/* for legacy projects), then saves it as a structured report for management in notes/REPORTS/ (or docs/REPORTS/ for legacy). Invoke with /daily-report or /daily-report YYYY-MM-DD. Also trigger for requests like daily report, work summary, progress report, today's work summary."
---

# daily-report

Extract the day's work from `<base>/` and git log, and generate a report for management.

**`<base>` resolution**: `notes/` (default) if it exists in the project, else `docs/` (legacy) if it exists, else `notes/` (newly created). See CLAUDE.md「標準ドキュメント構成」for the full rule.

## Arguments

- No arguments → targets today (JST)
- `YYYY-MM-DD` → targets the specified date

## Procedure

### 1. Determine target date and extract git log

Compute the JST day boundaries using the system's timezone, then query git log with
those boundaries. This avoids hardcoding timezone offsets.

```bash
# Target date in JST (default: today)
TARGET="${1:-$(TZ=Asia/Tokyo date +%Y-%m-%d)}"
START=$(TZ=Asia/Tokyo date -d "$TARGET 00:00" -u +%Y-%m-%dT%H:%M:%SZ)
END=$(TZ=Asia/Tokyo date -d "$TARGET +1 day 00:00" -u +%Y-%m-%dT%H:%M:%SZ)

# Current repository
git log --since="$START" --until="$END" --format="%h %ai %s"

# Submodules (if any)
git submodule foreach --quiet \
  "git log --since='$START' --until='$END' --format='%h %ai %s' 2>/dev/null"
```

This automatically handles month/year boundaries and works regardless of the
server's system timezone.

### 2. Collect sources

Git log is the only required source — it always exists and provides an objective
record of work. The <base>/ files enrich the report but are not prerequisites.

**Required**:
- `git log` + `git diff` for each commit (from Step 1)

**Optional** (use if present, skip silently if not):
- `<base>/TODO.md` — completed `[x]` and pending `[ ]` items
- `<base>/ISSUES.md` — newly registered and resolved issues
- `<base>/LOGS/log_*.md` — sections appended on the target date (identify via git diff or date headers)
- `<base>/PLAN.md` — if there were design changes

If no git commits exist for the target date, do not generate a report — inform
the user that no work was recorded and ask them to verify the date.

Cross-reference git log commit messages with available <base>/ content to determine
the scope of work for the target date. When <base>/ files are unavailable, infer
topic structure from commit messages and diffs.

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

**Commits today**: N (list repositories if multiple)
**Final test status**: X passed, Y skipped (if available in logs)
```

Granularity per topic:
- Large investigation + implementation → 3 sections: Conclusion / Background / Changes
- Small fix → 1 section: Summary only
- Design/planning → Summary + Design details

### 5. Save

Output to: `<base>/REPORTS/YYYY-MM-DD.md`

Create the directory if it does not exist. If a file with the same name already exists, confirm with the user.

## Reference processing

Follow the citation conventions in `.claude/rules/references.md`.

## Rules

- Language: match the user's prompt language (Japanese if invoked in Japanese, English if in English)
- Conclusion first. The manager should grasp the key point from the first sentence
- Avoid verbose background explanations; focus on decisions and results
- Include specific numbers ("improved by 3-5%" not "improved")
- Include test results if recorded in <base>/LOGS/ or commit messages. Do not run tests just for the report
- Do not include work not recorded in logs (do not speculate)
