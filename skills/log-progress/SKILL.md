---
name: log-progress
description: Write session minutes (セッション議事録) to notes/LOGS/YYYY-MM-DD_<topic>.md — a causal-order History of what happened and why, plus a one-line Decisions list — then sync the thin state indexes TODO.md, ISSUES.md, and the DECISIONS.md decision ledger. The main agent writes the minutes directly from full conversation context; a subagent lint-checks the result. Also used as a sub-step by /wrap-up-session. Use this skill whenever the user wants to record session progress, capture findings or decisions before stopping, update project docs from conversation, or says things like "log progress", "update docs", "update notes", "record what we did", "議事録", "進捗記録", "ログ更新", "記録して", "TODO を更新", "ノート更新". Do NOT trigger if the user also wants to commit and push — suggest /wrap-up-session instead.
---

# log-progress

Write session minutes: a per-session record of what happened and why. The reader is you or the user weeks later. The failure mode this skill exists to prevent is a record of outcomes whose reasoning cannot be reconstructed — 「なんでそうなった？」に答えられないログ.

**The main agent writes the minutes directly.** You are the only party holding the full conversation. Any summarize-then-delegate step loses context that can never be recovered. Delegation happens only after writing, as a lint pass (step 6).

## Output layout

| File | Role |
|---|---|
| `<base>/LOGS/YYYY-MM-DD_<topic>.md` | Session minutes — the primary record, one per session |
| `<base>/TODO.md` | State index: open tasks, 1–2 lines each + minutes link |
| `<base>/ISSUES.md` | State index: open issues, same format. Delete resolved entries |
| `<base>/DECISIONS.md` | Decision ledger: every decision as one line + minutes link. Superseded decisions get their line updated, never deleted |

`<base>` resolution: `notes/` if it exists → `docs/` (legacy) → project CLAUDE.md's designation → create `notes/`.

Out of scope — do not touch:
- Legacy topic logs (`<base>/LOGS/log_*.md`): frozen. Never append, never edit.
- Skill-owned ledgers (`log_sweep.md`, `gpu_monitor_*.csv`, `literature-survey.md`, etc.): maintained by their own skills.
- `PLAN.md`: deprecated. Leave as-is.

## Minutes template

Body in Japanese; code identifiers, commands, and paths verbatim. All five sections required; where nothing applies write `None` — an explicit `None` distinguishes "nothing happened" from "forgot to write".

```markdown
# YYYY-MM-DD <topic>

## Topic
主題と目的を 1–3 行。何のセッションで、何を達成しようとしたか

## History
因果順の散文。問題 → 原因の仮説 → 検証 (何をしたら何がわかったか) → 原因の確定 →
対処案の比較 (却下理由はここで生まれる) → 判断、の順で書く。
失敗した試みも成功と同じ流れの中に置く。数値・パス・出力などの証拠は流れの中に埋める。
並列な項目 (競合する仮説群、対処の候補案など) は導入する箇所で箇条書きにして
同列であることを示し、その後の散文で 1 つずつ解決する。
段落は作業の単位 (仮説の検証 / 原因の特定 / 案の比較と判断 / 実装と検証 など) で切る —
段落頭だけ拾い読みすれば作業の骨格が追える状態を保つ。短い作業同士の 1 段落への結合は可

## Decisions
- <採用案> / 却下: <案名> — <ユーザー確認済み | エージェント判断>

## Changes
- 変更ファイル・コミット・成果物

## Open Items
- 未解決・次の作業 (→ TODO/ISSUES へ反映)
```

**Why History is causal-order:** the reader must meet each conclusion only after the evidence that produced it. Writing the decision first (「案 B を採用した。根拠は…」) forces the reader to hold an unexplained conclusion while back-filling its justification — the exact reading failure this template replaces. A decision appears in History as the last link of its chain: what was tried, what that showed, which options were compared, why the losers lost, then the judgment.

**Why Decisions is one line each:** the reasons live in History, inside their causal chain. The Decisions list exists for scanning and grep (「この案は検討済みか？」) — it names the adopted option, the rejected alternatives, and the approval mark (ユーザー確認済み / エージェント判断). Repeating rationale here would fork the record into two places that can drift.

## Procedure

1. **Resolve `<base>` and target file.** Date via `date +%F`; topic slug short kebab-case English. If this session already wrote a minutes file, revise that same file — one session, one document; never fragment it with "continued" sections. If a different session claimed today's date+topic, suffix `-2`, `-3`.
2. **Write the minutes** per the template, directly from conversation memory.
3. **Sync TODO.md** — check off completed `[x]`, add new open tasks (1–2 lines + minutes link). Create the file if missing.
4. **Sync ISSUES.md** — add new issues (same format), delete resolved ones entirely. Create if missing.
5. **Sync DECISIONS.md** — one line per new decision: `- YYYY-MM-DD <same text as the minutes Decisions line> ([議事録](LOGS/…))`. Create if missing. When a decision supersedes an earlier one, update the old line in place and link the new minutes.
6. **Lint pass (background by default).** Spawn a subagent (`model: "sonnet"`) with the minutes path, the DECISIONS.md path, and the template above. It reads and reports — it does not edit. Leave it in the background (the Agent default; do not pass `run_in_background: false`): steps 2–5 are already written and saved, so the lint is a non-blocking check, not a gate. Go straight to the step 7 report and stay responsive; when the subagent returns, apply the legitimate findings and report the fixes as a follow-up. **Wrap-up exception:** when log-progress runs inside an end-of-session flow (e.g. /wrap-up-session, whose next step commits these same files), run the lint synchronously instead — there its fixes must land before the commit, so the result is needed to continue the turn rather than a responsiveness cost. Violations to hunt: missing sections; empty sections lacking `None`; History stating a decision before the evidence that produced it (conclusion-first); parallel alternatives (hypotheses, candidate options) buried inline in prose instead of enumerated as a bullet list at their introduction; a single paragraph spanning multiple units of work (e.g., a decision and its implementation packed together — long ones deserve their own paragraphs); failed attempts without failure reasons; claims without evidence (numbers, paths, outputs); Decisions lines carrying rationale (belongs in History) or missing the approval mark; minutes Decisions lines not matching their DECISIONS.md counterparts; broken relative links; malformed dates. Fix legitimate findings yourself.
7. **Report** to the user: minutes path, sections with content vs `None`, index changes (TODO/ISSUES/DECISIONS). Deliver this immediately without waiting on the lint; report the lint findings and any fixes in a follow-up once the background subagent returns. (In the wrap-up flow the lint is synchronous, so its findings join this same report.)

## Lifecycle

Minutes are revisable while their session is alive — repeat invocations rework the same file into one coherent document. Once the session ends, the file is frozen: later sessions write their own minutes and never edit past ones. The state indexes (TODO/ISSUES/DECISIONS) are living documents, always edited in place.
