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

## 2026-03-22: Semantic Scholar API キー対応・指数バックオフ実装

### レート制限調査

Semantic Scholar API のレート制限を調査:
- 認証なし: 5,000 req / 5分を全匿名ユーザーで**共有** → 429 が頻発
- 認証あり: `/paper/search` は **1 req/sec** 保証
- 公式ドキュメントで指数バックオフが **mandatory** と記載

### 実施内容

1. **指数バックオフ実装** — `search_semantic_scholar.py` のリトライを固定3秒から
   指数バックオフ+ジッター (2s→4s→8s→16s→32s, max 60s, 最大5回) に変更
2. **API キー対応** — `--api-key` オプションと `S2_API_KEY` 環境変数の読取を追加。
   認証時は `x-api-key` ヘッダーで送信
3. **API キー保管** — `pass` (GPG暗号化) に保存し、`~/.zshenv` で環境変数に展開。
   dotfiles が git 管理下のため平文保存は不可

### API キー保管方式の検討

| 方法 | 採用 | 理由 |
|------|------|------|
| `~/.zshenv` に直接 export | 不可 | dotfiles が git 管理下 |
| `pass` (GPG) + `~/.zshenv` | **採用** | 暗号化 at rest、git に平文なし |
| `.env` ファイル | 不可 | `~/.claude/` が git 管理下 + Claude Code の自動読込リスク |
| `settings.json` の env | 不可 | git-tracked |

### 検証結果

- API キーあり: 429 なしで即座に結果返却（連続呼び出しも OK）
- API キーなし: 指数バックオフで 2-3回リトライ後に成功
