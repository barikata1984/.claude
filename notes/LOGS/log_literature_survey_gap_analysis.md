# literature-survey スキル: ベストプラクティス乖離分析と改善案

**日付**: 2026-04-06
**入力**: `survey_paper_best_practices.md` (Kitchenham, Webster & Watson, Shaw, Boloni, PRISMA)

## 参照文献

| 文献 | 概要 |
|------|------|
| Kitchenham (2004) | SLR の標準的手順書。PICOC, レビュープロトコル, 品質評価 |
| Webster & Watson (2002) | 概念中心アプローチ、概念マトリクスの提唱 |
| Shaw (2003) | ICSE 2002 全投稿分析。問い・結果・検証の三軸モデル |
| Boloni (2008) | サーベイ論文の実践的執筆アドバイス |
| PRISMA 声明 | 体系的レビューの報告基準 |

## 乖離分析

### 充足している項目

- 複数データベース検索 (Semantic Scholar, OpenAlex, arXiv, WebSearch)
- Snowballing (前方・後方引用追跡)
- 検索プロセスの文書化 (Search Log)
- データ抽出の体系化 (thesis/core/diff/limit 4軸アノテーション)
- 定性的統合 (Phase 5: thesis→foundation→progress→gap)
- 概念中心（著者中心でない）組織化
- 未解決課題と将来展望 (Gap + Seed)
- レビュープロトコル (Phase 2-7 のワークフロー)

### 重大な乖離 TOP 5

| 優先度 | 乖離項目 | 影響 |
|--------|----------|------|
| 1 | 横断的比較表の欠如 | 論文間の体系的比較ができない |
| 2 | RQ / 包含・除外基準の不在 | スコープが曖昧、検索の一貫性低下 |
| 3 | 用語整理セクションの欠如 | 異表記による検索漏れ・読者混乱 |
| 4 | 定量的トレンド分析の欠如 | 動向の主張に客観的裏付けがない |
| 5 | サーベイ自体の限界記述の欠如 | 学術論文としての信頼性要件不足 |

### その他の乖離

- Abstract セクションの欠如
- Conclusion セクションの欠如
- 概念マトリクスの欠如
- 引用時の著者名本文記載 (Boloni 推奨) と現行 `[Key]` 形式の差異
- 個別論文の品質評価（エビデンスレベル）の欠如
- 出版バイアスへの明示的対処の欠如
- 分類体系の網羅性・相互排他性の検証手順の欠如

## 改善案

### A. 低コスト改善（Phase 追加なし）

| ID | 内容 | コスト影響 |
|----|------|-----------|
| A1 | Phase 1 強化: RQ 策定 + 包含/除外基準の事前定義 | ほぼなし。下流の検索・分析精度向上 |
| A2 | Phase 2 強化: RQ から同義語・Boolean 検索文字列を構築 | 中立。検索精度向上で再検索削減 |
| A3 | テンプレート拡充: Abstract, Terminology, Comparison Table, Threats to Validity, Conclusion | Phase 7 のトークン微増のみ |

### B. 中コスト改善（Phase 5 拡充）

| ID | 内容 | コスト影響 |
|----|------|-----------|
| B1 | 定量的トレンド分析 (年別論文数, 手法分布, 実験環境内訳) | Phase 3 のメタデータから集計。中程度 |
| B2 | 概念マトリクス (概念 × 論文の対応表) | Phase 3 の annotations から再構成。中程度 |

### C. 高コスト改善（簡略化版で対応）

| ID | 内容 | 対応方針 |
|----|------|----------|
| C1 | 多段階スクリーニング (PRISMA) | 1段階を維持し、Phase 2.5 で包含/除外基準を明示適用 |
| C2 | 個別品質評価チェックリスト | 比較表にエビデンスレベル列を追加する形で簡略化 |
| C3 | 出版バイアス対処 | 検索戦略にプレプリント包含を明記 + Search Log で記録 |

### D. 対応不要

| 項目 | 理由 |
|------|------|
| 評価者間信頼性 (Cohen's Kappa) | AI 単独実行のため該当なし |
| メタ分析 | ロボット工学で実験条件の多様性が大きく適用限定的 |
| 独自の図の作成 | Claude Code では困難。テキストベース表・樹形図で代替 |

## コンテクスト・実行時間の分析

### 参照文献（エージェントスキル設計）

| ID | 文献 | 種別 |
|---|---|---|
| R1 | Anthropic, "Custom slash commands" (https://code.claude.com/docs/en/skills) | 公式ドキュメント |
| R2 | Anthropic Engineering, "Effective context engineering for AI agents" (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 公式ブログ |
| R3 | Larsen, "Building an internal agent: Progressive disclosure and handling large files" (https://lethain.com/agents-large-files/) | 実践者ブログ |
| R4 | Lin et al., "Stop Wasting Your Tokens" (arXiv:2510.26585) | arXiv プレプリント |
| R5 | Bandara et al., "A Practical Guide for Production-Grade Agentic AI Workflows" (arXiv:2512.08769) | arXiv プレプリント |
| R6 | Speakeasy, "Reducing MCP token usage by 100x" (https://www.speakeasy.com/blog/how-we-reduced-token-usage-by-100x-dynamic-toolsets-v2) | エンジニアリングブログ |
| R7 | Epsilla, "The 3 Essential Sub-Agent Patterns" (https://www.epsilla.com/blogs/2026-03-14-ai-sub-agent-patterns) | エンジニアリングブログ |

### 現行スキルの構造分析

SKILL.md: 458 行（推奨上限 500 の 92%）、references/ 2 ファイル 269 行、計 727 行。

セクション別行数:

| セクション | 行数 | 割合 |
|---|---|---|
| Frontmatter + Language Rule | 29 | 6% |
| Phase 1: Scope Definition | 9 | 2% |
| Phase 2: Search Strategy | 27 | 6% |
| **Search Execution (API/ツール詳細)** | **65** | **14%** |
| Deduplication | 14 | 3% |
| Phase 2.5: Search Review Checkpoint | 44 | 10% |
| **Phase 3a: OA Paper Analysis** | **48** | **10%** |
| Phase 3b: Paywall Paper Analysis | 43 | 9% |
| Phase 4: DOI Resolution | 36 | 8% |
| **Phase 5: Survey-Level Synthesis** | **55** | **12%** |
| Phase 6: Reference Verification | 18 | 4% |
| Phase 7: Output Generation | 15 | 3% |
| Reference Processing + Quality Checklist | 29 | 6% |

### 実行時トークンコスト推定

| Phase | 入力 | 出力 | 主因 |
|---|---|---|---|
| 1 (Scope) | 低 | 低 | ユーザー対話のみ |
| 2 (Search) | **高** | 中 | 複数サブエージェント、WebSearch/API 多数 |
| 2.5 (Checkpoint) | 低 | 中 | 集計表示 |
| **3a/3b (Analysis)** | **極めて高** | **高** | **最大ボトルネック: 30-60 本の論文全文 fetch + 4 軸アノテーション** |
| 4 (DOI Resolution) | 中 | 低 | 論文ごと逐次 API（LLM 推論不要） |
| 5 (Synthesis) | 高 | 高 | 全アノテーション読み込み + 横断分析 |
| 6 (Verification) | 中 | 低 | reference-verify スキル呼び出し |
| 7 (Output) | 中 | **極めて高** | 最終レポート全文一括生成 |

### 設計原則と現行スキルの適合度

文献から抽出した原則と現行スキルの対応:

| # | 原則 | 出典 | 現行 | 問題度 |
|---|---|---|---|---|
| P1 | SKILL.md は 500 行以下。参照資料は references/ に分離 | R1 | 458 行で余裕なし | **高** |
| P2 | サブエージェントは凝縮した要約 (750-2,000 tokens) を返す | R2, R7 | Phase 3 の戻り値に圧縮指示なし | **高** |
| P3 | 決定論的操作は LLM を介さずスクリプト実行 | R5 | Phase 4 を LLM が逐次実行 | **中** |
| P4 | 冗長なツール出力をフィルタリング | R4 | 論文全文が圧縮なく流入 | **高** |
| P5 | 長時間タスクではコンテキスト圧縮 | R2 | 圧縮タイミングの言及なし | **中** |
| P6 | 最小限から始め、失敗に基づいて追加 | R2 | Phase 5 の書き方指示が詳細すぎる | **低** |

### P2/P4/P5 の統合理解：コンテクスト流入制御

P2, P4, P5 は同一原則「メインコンテキストへの情報流入量の制御」を異なるレイヤーで適用したもの:

```
論文全文 (数万トークン)
  → [P4] ツール出力フィルタ: サブエージェント内で全文を消費、必要部分のみ保持
  → [P2] サブエージェント境界: 構造化 JSON (数百トークン/論文) のみ返却
  → [P5] セッション圧縮: Phase 完了後、次 Phase に必要な情報だけ残す
```

P4 と P2 は一体設計すべき。提案 2 がこの両方をカバーする。
P5 は蓄積への安全弁。30-60 本分の JSON も総量は大きいため、Phase 5 前に
カテゴリ別集約サマリに圧縮するタイミングを設けるかが設計判断点。

## 実装計画

### Step 1: SKILL.md のリファクタリング（コスト削減）

改善案の追加よりも先に行う。SKILL.md の行数を削減し、追加の余裕を確保する。

| 変更 | 対象 | 行数変化 | 根拠 |
|------|------|----------|------|
| 1a. Search Execution を `references/search_sources.md` に分離 | Phase 2 | **-60** | P1 |
| 1b. Phase 5 の詳細指示を `references/synthesis_guide.md` に分離 | Phase 5 | **-20** | P1, P6 |
| 1c. Quality Checklist を `references/quality_checklist.md` に分離 | 末尾 | **-20** | P1 |
| 1d. Phase 4 の API 手順を削除（スクリプト化による置換） | Phase 4 | **-30** | P3 |
| **小計** | | **-130** | |

分離後の SKILL.md: 約 328 行。追加可能な行数: 約 170 行。

### Step 2: コンテクスト流入制御の実装（P2/P4/P5 統合）

| 変更 | 内容 | 行数変化 |
|------|------|----------|
| 2a. Phase 3 のサブエージェント出力仕様を定義 | バッチサイズ (5-10 本)、戻り値を構造化 JSON に限定、論文全文は内部消費 | +15 |
| 2b. Phase 5 前のコンテクスト圧縮ポイントを明記 | Phase 3 完了→Phase 5 の間に集約ステップを挿入 | +5 |
| 2c. Phase 7 を分割生成に変更 | セクション単位で追記する指示 | +5 |
| **小計** | | **+25** |

### Step 3: 乖離分析の改善案を追加

Step 1-2 後の SKILL.md: 約 353 行。残り約 147 行を使って追加。

| 変更 | 対応する乖離 | 追加先 | 行数変化 |
|------|-------------|--------|----------|
| 3a. RQ 策定 + 包含/除外基準 | 乖離 #2 | Phase 1 (SKILL.md) | +15 |
| 3b. キーワード体系化 | その他 | Phase 2 (SKILL.md) | +10 |
| 3c. 出版バイアス明記 | C3 | Phase 2 (SKILL.md) | +3 |
| 3d. Phase 2.5 で包含/除外基準を適用 | C1 | Phase 2.5 (SKILL.md) | +5 |
| 3e. 定量的トレンド分析 | 乖離 #4 | Phase 5 (SKILL.md) | +8 |
| 3f. 概念マトリクス | その他 | Phase 5 (SKILL.md) | +5 |
| **小計 (SKILL.md)** | | | **+46** |

| 変更 | 対応する乖離 | 追加先 | 行数変化 |
|------|-------------|--------|----------|
| 3g. Abstract | その他 | report_template.md | +10 |
| 3h. Terminology & Background | 乖離 #3 | report_template.md | +15 |
| 3i. Comparison Table | 乖離 #1 | report_template.md | +20 |
| 3j. 定量的トレンド分析テンプレート | 乖離 #4 | report_template.md | +15 |
| 3k. 概念マトリクステンプレート | その他 | report_template.md | +10 |
| 3l. Threats to Validity | 乖離 #5 | report_template.md | +10 |
| 3m. Conclusion | その他 | report_template.md | +8 |
| 3n. エビデンスレベル列 | C2 | report_template.md (比較表内) | +3 |
| **小計 (report_template.md)** | | | **+91** |

### Step 4: スクリプト新設

| ファイル | 内容 |
|----------|------|
| `scripts/resolve_dois.py` | JSON 入力 → DBLP/Crossref API → DOI 解決 → JSON 出力 |

### 最終見積もり

| ファイル | 現行 | 変更後 | 変化 |
|----------|------|--------|------|
| SKILL.md | 458 | ~399 | -59 |
| references/report_template.md | 172 | ~263 | +91 |
| references/search_sources.md | 0 (新規) | ~65 | +65 |
| references/synthesis_guide.md | 0 (新規) | ~25 | +25 |
| references/quality_checklist.md | 0 (新規) | ~25 | +25 |
| references/seed_format.md | 97 | 97 | 0 |
| scripts/resolve_dois.py | 0 (新規) | ~150 | +150 |

SKILL.md は推奨上限 500 行の約 80% に収まり、
乖離分析 TOP 5 すべてとその他の主要項目をカバーする。

## 実装結果

### Step 1: SKILL.md リファクタリング

SKILL.md から参照資料を分離し、行数を 458 → 334 に削減。

| 変更 | 内容 | 行数変化 |
|------|------|----------|
| 1a | Search Execution → `references/search_sources.md` (82行) | -60 |
| 1b | Phase 5 詳細指示 → `references/synthesis_guide.md` (67行) | -20 |
| 1c | Quality Checklist → `references/quality_checklist.md` (28行) | -20 |
| 1d | Phase 4 API 手順 → `scripts/resolve_dois.py` 参照に置換 | -24 |

### Step 2: コンテクスト流入制御 (P2/P4/P5 統合)

| 変更 | 内容 | 行数変化 |
|------|------|----------|
| 2a | Phase 3 サブエージェント出力仕様: 構造化 JSON のみ返却 | +45 |
| 2b | Phase 3→5 間に Context Consolidation セクション追加 | +12 |
| 2c | Phase 7 を 3 段階の分割生成に変更 | +3 |

### Step 3: 乖離分析の改善追加

SKILL.md:

| 変更 | 内容 |
|------|------|
| 3a | Phase 1 → Research Design に改名。RQ 策定 + 包含/除外基準追加 |
| 3b | Phase 2 に Keyword Construction セクション追加 |
| 3c | Tier 1 に出版バイアス対策（プレプリント包含）明記 |
| 3d | Phase 2.5 で包含/除外基準の適用を明示 |
| 3e | Phase 5 に Quantitative Trends 追加 |
| 3f | Phase 5 に Concept Matrix 追加 |

report_template.md:

| 変更 | 内容 |
|------|------|
| 3g | Abstract セクション（4文構造） |
| 3h | Terminology and Background セクション（用語バリエーション表） |
| 3i | Comparison Table（横断比較表 + エビデンスレベル列） |
| 3j | Quantitative Trends テンプレート（年別/手法別/実験設定別） |
| 3k | Concept Matrix テンプレート |
| 3l | Threats to Validity セクション |
| 3m | Conclusion セクション（RQ 回答 + 実務示唆） |

quality_checklist.md: Research Design チェック項目、新セクション対応項目を追加。

### Step 4: スクリプト新設

| スクリプト | 機能 | 検証結果 |
|-----------|------|---------|
| `scripts/resolve_dois.py` | arXiv ID → DBLP/Crossref → publisher DOI 解決 | arXiv 1808.00177 → IJRR DOI `10.1177/0278364919887447` を正しく解決 |
| `scripts/extract_sections.py` | ar5iv HTML → キーセクション抽出 (Abstract, Introduction, Conclusion, Limitations, Future Work, Tables, Figure captions) | h2/h3 両パターンの論文で正常動作確認 |

### extract_sections.py による Phase 3 改訂

Phase 3 の最大ボトルネックであった「全論文の全文を LLM に投入」を改善。

変更前: サブエージェントが全文を fetch → 読解 → アノテーション生成
変更後: スクリプトがキーセクションを抽出 → サブエージェントは抽出済みテキストのみ受領

| 項目 | 変更前 | 変更後 |
|------|--------|--------|
| サブエージェント入力/論文 | 全文 (10,000-15,000 tokens) | 抽出セクション (2,000-5,000 tokens) |
| バッチサイズ | 5-10 本 | 15-20 本 |
| サブエージェント数 (50本) | 5-10 個 | 3-4 個 |
| 推定トークン削減率 | — | 約 70-80% |

設計原則: P3 (決定論的操作はスクリプトで) と P4 (冗長出力のフィルタリング)
を Phase 3 の最大コストポイントに適用。

### 最終状態

| ファイル | 改善前 | 改善後 |
|----------|--------|--------|
| SKILL.md | 458 | 429 (推奨上限の 86%) |
| references/report_template.md | 172 | 275 |
| references/search_sources.md | (新規) | 82 |
| references/synthesis_guide.md | (新規) | 67 |
| references/quality_checklist.md | (新規) | 47 |
| references/seed_format.md | 97 | 97 (変更なし) |
| scripts/resolve_dois.py | (新規) | 240 |
| scripts/extract_sections.py | (新規) | 400 |

乖離分析 TOP 5 すべてカバー、コンテクスト流入制御実装済み、Phase 3 の
トークン消費を推定 70-80% 削減。

### 未着手

- テストケースでの実行評価（別セッションで実施予定）

### 実装順序

1. **Step 1** (リファクタリング) → 2. **Step 2** (流入制御) → 3. **Step 4** (スクリプト) → 4. **Step 3** (改善追加)

Step 1-2 を先に行う理由: 行数削減と流入制御設計が Step 3 の追加内容の形態を制約するため。
