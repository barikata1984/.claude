# literature-survey スキル v2 改善ログ

## 2026-03-22: 類似スキルとの比較分析・改修実施

### 背景

公開されている Claude Code スキルおよび LLM ベースの文献調査ツールと比較し、
literature-survey スキルの改善点を特定した。

### 調査した主な類似ツール

- agent-research-skills (lingzhi227) — 31 composable skills、Semantic Scholar/arXiv/OpenAlex/CrossRef の API スクリプト同梱
- research30 (shandley) — 直近30日の文献を5データベースから並列検索、スコアリング・重複排除あり
- FastMCP literature-review — PRISMA methodology、最も方法論的に厳密
- ARIS (wanshuiyin) — DBLP/CrossRef から実 BibTeX を取得（LLM 生成禁止）
- OpenScholar — 45M 論文からの RAG、GPT-4o を上回る引用精度
- PaperQA2 — agentic RAG、retraction check 付き

### 特定した改善候補と対応

| # | 改善内容 | 対応 |
|---|----------|------|
| 1 | Semantic Scholar / OpenAlex API スクリプト同梱 | 実施 — `scripts/` に2本追加 (stdlib only) |
| 2 | 重複排除ルールの明示 | 実施 — Deduplication セクション新設 |
| 3 | Phase 2→3 間に Human-in-the-loop チェックポイント | 実施 — Phase 2.5 新設 |
| 4 | 論文スコアリング基準の明示 | 実施 — 被引用数 > venue tier > recency |
| 5 | limit フィールドの LLM 推測禁止ルール強化 | 実施 — 明示的な禁止ルール追加 |
| 6 | BibTeX 出力の追加 | 不要 — references.bib は既にフックで MAIN.md から自動生成 |

### 変更ファイル

- `skills/literature-survey/scripts/search_semantic_scholar.py` (新規)
- `skills/literature-survey/scripts/search_openalex.py` (新規)
- `skills/literature-survey/SKILL.md` (Phase 2 改修, Phase 2.5 新設, dedup, limit ルール, checklist 更新)
- `skills/literature-survey/references/report_template.md` (Search Review Checkpoint セクション追加)

### 検証結果

- 両スクリプト: Python コンパイル OK
- OpenAlex API テスト: 正常 (JSON 返却確認)
- Semantic Scholar API テスト: レート制限後リトライで正常動作確認
