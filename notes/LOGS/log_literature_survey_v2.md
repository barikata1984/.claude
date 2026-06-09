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

## 2026-04-06: クレデンシャル隔離 + OA アクセスパイプライン + MCP サーバー化

### 背景

`pass` (GPG) + `~/.zshenv` 方式では (1) シェル起動のたびに GPG パスフレーズ入力が必要、
(2) `S2_API_KEY` がエージェントの環境変数に平文露出、という問題があった。
組織内でスキルを共有するにあたり、ゼロベースでクレデンシャル管理のベストプラクティスを構成した。

### エビデンス調査

4つの一次情報源から原則を抽出:

| ID | 情報源 | 種別 |
|----|--------|------|
| E1 | Anthropic "Securely deploying AI agents" | 公式セキュリティガイド |
| E2 | Errico et al. arXiv:2511.20920 "Securing the MCP" | 学術論文 |
| E3 | OWASP Top 10 for LLM 2025 — LLM07 | 業界標準 |
| E4 | OWASP AI Agent Security Cheat Sheet | 実装ガイド |

導出した原則: P1 クレデンシャル外部化、P2 セキュリティ境界分離、P3 仲介者パターン、P4 最小権限。
「MCP サーバーがベスト」と断言した文献は存在しない。MCP は確立された原則を
Claude Code で実現する自然な機構として位置づけた（推論であることを明記）。

成果物: `docs/bestpractice_credential_isolation.md`

### 論文アクセスルートの調査

arXiv, Unpaywall, S2 openAccessPdf, OpenAlex, CORE, 出版社 API, PMC, Google Scholar を調査。
Robotics/ML 分野では arXiv (85-95%) + Unpaywall でほぼカバー可能。
Cookie ベースの academic-fetch はペイウォール論文の最終フォールバックに格下げ。

### academic-search MCP サーバーの実装

S2 検索 + OA URL 解決を単一の MCP サーバーで提供。MCP の「1ドメイン=1サーバー」
原則に従い、S2 API キーとレートリミッターを共有する2ツールを統合。

| ツール | 機能 |
|--------|------|
| `search_semantic_scholar` | S2 検索（openAccessPdf フィールド追加） |
| `resolve_oa_url` | Unpaywall → S2 OA → arXiv PDF のカスケード解決 |

構成:
- `~/.claude/mcp/academic-search/start.sh` — `pass` → 環境変数注入 → `exec uv run`
- `~/.claude/mcp/academic-search/server.py` — FastMCP, 2 tools, async レートリミット
- `claude mcp add --scope user` で登録（`mcp.json` ではなく `~/.claude.json`）

### 変更ファイル

| ファイル | 操作 |
|---------|------|
| `mcp/academic-search/start.sh` | 新規 |
| `mcp/academic-search/server.py` | 新規 |
| `skills/literature-survey/SKILL.md` | MCP ツール参照 + OA パイプライン追加 + Phase 4 更新 |
| `~/.zshenv` | `S2_API_KEY` の export 削除 |
| `scripts/search_semantic_scholar.py` | deprecated コメント追加 |
| `docs/bestpractice_credential_isolation.md` | 新規 |

### 検証結果

- MCP サーバー: Connected（academic-search, academic-fetch 両方）
- `search_semantic_scholar`: 検索成功、`openAccessPdf` フィールド含む
- `resolve_oa_url`: arXiv PDF フォールバック動作確認、Unpaywall は email 未登録のためスキップ
- クレデンシャル隔離: VSCode 再起動後 `echo $S2_API_KEY` が空であることを確認

### 未着手・検討中

(なし — 以下のセッションで対応済み)

---

## 2026-04-06: Phase 3a/3b 分割実装

### 実施内容

- SKILL.md の Phase 3 を Phase 3a (OA 先行処理) + Phase 3b (ペイウォール出版社グループ単位) に分割
- OA 解決セクションに Phase 3a/3b の用途注記を追加
- Quality Checklist に Phase 3a/3b チェック項目を追加
- report_template.md の Limit Field Coverage テーブルを "Paywall (fetched in 3b)" / "Paywall (skipped)" に分割

### 設計判断

- **Cookie 自動読み込み (旧 Issue #1) は不要と判断**: Phase 3b の時点でユーザーは出版社リストを認識済みなので、意図的に `save-cookies.sh` を実行できる。Phase 3a/3b 分割単体で UX は十分改善される
- **Phase 3b は出版社グループ単位のループ**: 出版社ごとに Cookie エクスポート → 当該出版社の全論文を `fetch_with_auth` で一括処理。出版社単位で skip も可能
- `pass insert api/unpaywall-email` は実施済み（Unpaywall カスケード有効化）

### 変更ファイル

| ファイル | 変更 |
|----------|------|
| `skills/literature-survey/SKILL.md` | Phase 3 → 3a/3b 分割、OA 注記、Quality Checklist |
| `skills/literature-survey/references/report_template.md` | Limit Field Coverage テーブル |
| `docs/TODO.md` | Phase 3a/3b 完了、Unpaywall 完了、Cookie 自動読み込み削除 |
| `docs/ISSUES.md` | 全イシュー解決済みでクリア |

---

## 2026-04-07: ISSUES レビュー + SKILL.md 改善

literature-survey 実行後に記録された ISSUES 5件（#1 均一密度未検証、#2 並列制御、
#3 コンテキスト予算、#4 DOI 検証遅延、#5 Paywall 判断）の Fix 適用状況を検証し、
未適用の Fix を精査・適用した。

ISSUES.md に「Fix (SKILL.md)」と記載されていたが、実際に SKILL.md に反映されていたのは
Issue #5 のチェックポイント部分のみ（部分適用）。他は全て未適用だった。

### Issue 別対応

| Issue | 対応 |
| ----- | ---- |
| #1 均一密度未検証 | ユーザーが ISSUES.md から削除（プロジェクト側イシュー） |
| #2 並列制御 | Phase 3a は自然に 2-4 並列に収まるため制限不要と判断。Phase 2 のみ対象。SKILL.md 適用は保留 |
| #3 コンテキスト予算 | 根本解決不可（API 不在）。Fix を「コンテキスト保護設計」に書き直し: サブエージェント返却要約化 + 中間ファイル書き出し必須化 + Phase 5 ファイル読み直し |
| #4 DOI 検証遅延 | Phase 2 での即時検証は不可能（DOI が揃わない）。Fix を Phase 4 解決結果検証 + Phase 6 漏れ防止に書き直し。さらにユーザーが「Phase 6 の失敗モード調査が先決」と判断し、次のアクションに変更 |
| #5 Paywall 判断 | OA カバレッジ分析 + 3段階推奨生成（Skip all / Selective fetch / Full fetch）を SKILL.md Phase 3a Step 3 に適用 → Issue 解消・削除 |

### SKILL.md 適用内容

1. **Subagent Model Policy** 新設 — 全サブエージェントにミドルクラスモデル（現 Sonnet 4.6）を指定。将来のモデルラインナップ変更にも対応するため抽象表現を採用
2. **Phase 3a Step 3** 改修 — 「Report paywall papers」→「OA coverage analysis and paywall processing recommendation」に名称変更。カバレッジ分析テーブル + 3段階推奨 + Publisher Priority 列を追加

### 変更ファイル一覧

| ファイル | 変更 |
| -------- | ---- |
| `skills/literature-survey/SKILL.md` | Subagent Model Policy 新設、Phase 3a Step 3 改修 |
| `docs/ISSUES.md` | #1 削除、#3/#4 Fix 書き直し、#5 適用済み→削除、ラベル「対策案 (未実装)」に統一 |
| `docs/TODO.md` | スキル改善タスク更新 |
