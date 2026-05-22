# Log: 挙動制御フレームワーク

## 2026-05-04: scope expansion 抑制と CLAUDE.md 剪定

### 問題診断

ユーザーから挙動の指摘：「A という質問に答える際、Claude が B/C
という関連話題を勝手に提示し、自分の希望（B について話したい等）まで
表明する」型の scope expansion。加えて「過度な迎合（sycophancy）」も
抑制したいが、まずは前者から対処する方針。

文献調査の結果（WebSearch / WebFetch）：

- **Excessive Agency** (OWASP LLM06:2025) — ツール権限の脆弱性なので、
  この現象を直接記述する用語ではない（誤用注意）
- **Verbosity Compensation** (arXiv:2411.07858) — 不確実性下での冗長応答。
  scope 拡張とは別概念
- **Sycophancy** (arXiv:2310.13548, Anthropic) — ユーザー見解への迎合
- **Verbosity Bias** (arXiv:2310.10076, Saito et al.) — preference labeling
  でのバイアス
- **Show and Tell** (arXiv:2511.13972) — directive 介入で 56% 削減、
  directive + 例示で 70% 削減を実証

「scope expansion」を直接命名する標準用語は存在せず、Anthropic の
[claude-personal-guidance](https://www.anthropic.com/research/claude-personal-guidance)
が報告する sycophancy の親戚として扱える。`anthropics/claude-code` issue
[#27147](https://github.com/anthropics/claude-code/issues/27147) が
「Claude が research answer の後に勝手に write アクションを取る」現象を
記述しており、最も直接的な関連 issue。

### 対策の階層（layered defense）

1. **CLAUDE.md directive**（予防、~56% 効果）
2. **Stop hook**（決定論的検査、100% 効果だがパターンマッチ精度依存）
3. **将来オプション**：UserPromptSubmit hook、subagent systemPrompt override 等

### CLAUDE.md 剪定（153 → 124 行、-29 行）

- 旧 L17-29「モデル・effort・context の使い分け」を削除
  - 内容はユーザー手打ちコマンドの説明で Claude 向け instruction でない
  - 一旦 `docs/model_usage_cheatsheet.md` に分離後、ユーザー判断で削除
- 「セッション終了時は /log-progress」削除（`/wrap-up-session` で代替）
- 「回答の根拠となるソース明示」削除（知識ソース明示ルールと重複）
- WebSearch/WebFetch 必須トリガーの A-F 列挙（32 行）を 6 箇条のキーワード並列に圧縮
- 機密情報の取扱いから「deny rules で自動ブロック済み」の状態記述行を削除
  （settings.json で deterministic に強制されているため）

### CLAUDE.md 追加

- 新規 `## 応答スコープ規約` セクション（ワークフロー直後、3 箇条）
  - 質問・依頼で明示されていないサブセクション（「なぜ」「結論」「推奨」
    「次のステップ」「要点」「まとめ」「補足」「例」「比較」「方針」等）の
    自動付加を禁止
  - 真に曖昧な場合のみ明確化質問を 1 つ・1 行で返す
  - 不確実性は範囲拡張ではなく知識ソースブロックでの明示で扱う
- 既存 `## 日本語スタイル規約` 冒頭に「日本語応答を出力する直前に英単語を
  点検し、固有名詞・コード片・数式・skill 構造ラベルでなければ和訳せよ」
  directive を追加

### Stop hook 実装

- 新規 `~/.claude/hooks/stop-scope-check.sh`（block mode）
  - `^#{2,}\s+.*(なぜ|結論|推奨|次のステップ|要点|まとめ|補足|例|比較|方針)`
    にマッチする見出しを検出
  - 検出時は `{"decision": "block", "reason": "..."}` を出力して再生成を強制
  - `stop_hook_active=true` 時は無限ループ防止のためパススルー
  - 違反ログは `~/.claude/hooks/scope-violation.log` に記録
- 既存 `~/.claude/hooks/stop-taxonomy-check.sh` を warn-only から block へ昇格
  - `stop_hook_active` チェックを追加
  - 検出時のログ記録を維持しつつ block JSON を出力
- `settings.json` の Stop 配列に scope-check を並列登録（同一 entry に追加）

### 設計判断：分離 vs 統合

scope-check と taxonomy-check は別スクリプトとして分離。理由：
- 検出対象が直交（taxonomy ハルシネーション vs 未要求サブセクション）
- 既存 taxonomy-check の試運用観察（ログ蓄積）を撹乱しない
- ログを分離（`taxonomy-warn.log` / `scope-violation.log`）して個別に偽陽性率
  評価が可能
- 重複する transcript parsing logic（~40 行の jq pipeline）はコピペ容認、
  3 つ目の hook が必要になった時点で共通関数に抽出（YAGNI）

---

## 2026-05-22 和文タイポgrafィ正規化フック実装 + 応答制御の concise スタイル移行

### 和文タイポグラフィ正規化フック（新規実装）

英文・和文混在の技術文書で、半角約物スタイル（理工系スタイル）を `.md` 生成時に
自動適用するフックを実装。設計判断は以下。

**二層構成**：判断を要する規則（ダッシュ使い分け・和欧境界スペースの語彙的例外）は
プロンプト（`rules/japanese_style.md`）、機械判定できる規則（全角約物→半角）は
決定論的フックに分離。フックはチャット応答には効かず Write/Edit したファイルのみ対象。

**変換規約（全角約物のみ変換・ASCII 不可侵）**：
- `。`→`. ` / `、`→`, ` / `！`→`! ` / `？`→`? ` / `：`→`: `
- `「」『』`→`"" ''`、`（）`→`()`、`〜`・`・` は温存
- ASCII の `.` `,` は触らないため小数 `3.14`・略語 `e.g.`・URL・コードは自動保護
- ダッシュ: em dash 禁止は生成時、en dash は範囲・複合語限定。フックは検出して警告のみ
- 数字スペース: 直後が漢字かな=詰める / ラテン文字=空ける / `%`・`°`=詰める（生成時規則）

**実装手段の確定経緯**：当初 markdown-it-py の AST で変換を計画したが、実測で
(1) インライントークンが元ソースの文字位置を持たない (map=None)、(2) render() が
HTML を返し Markdown に戻せない、ことが判明。AST 経由を断念し**正規表現マスク方式**に
変更。保護対象（フロントマター・フェンス/インラインコード・数式・LaTeX・リンク/URL）を
順にマスク→残りを変換→復元。

**成果物**：
- `~/.claude/hooks/format_ja_typography.py`（マスク方式エンジン、フェイルセーフ・冪等）
- `~/.claude/hooks/test_format_ja_typography.py`（24 ケース + 冪等性 + 警告検出、全通過）
- `~/.claude/hooks/format-ja-typography.sh`（`.md` のみ・`~/.claude/**` 除外・
  opt-out マーカー `<!-- no-ja-typography -->` 対応）
- `settings.json` PostToolUse に登録（ユーザーが手動登録、フック登録は分類器がブロック）
- `rules/japanese_style.md` に「タイポグラフィ（半角約物スタイル）」節を追記

**適用範囲**：global（全 .md）。PostToolUse は編集したファイルにのみ発火するため、
触らないノートは無傷。LaTeX ソースは opt-out マーカーで除外。

### 応答制御：scope-check 路線から concise 出力スタイルへ移行

**検証で判明した事実**：
- 「1-3 文 / preamble 禁止」という固定の組み込み既定は**存在しない**（公式 Claude Code
  ベストプラクティス全文を確認）。Opus 4.7 は複雑性に応じて応答長を調整し固定既定を
  持たない設計（Anthropic 公式プロンプトガイドで確認）。以前「組み込み既定」と呼んだ
  のは非公式ミラー由来の誤りで撤回。
- 公式は「冗長削減はプロンプトで明示せよ、否定形より肯定例が有効」と明記。
- Claude Code には**出力スタイル**機能あり（`~/.claude/output-styles/*.md`、
  システムプロンプトに直接追記、`/config` で選択）。CLAUDE.md（ユーザーメッセージとして
  注入）より、振る舞い定義にはこちらが設計上適切。ブラウザの `<userStyle>` は browser-only。

**真因の特定**：本セッション中の冗長な応答（未要求の太字疑似見出しの濫用・反復）の真因は
規則の不在ではなく、既存「応答スコープ規約」をエージェント側が遵守しない**遵守不全**。
規則は自己強制しないため、重複する新規則を足しても効果は限定的（セッション中に実演された）。

**方針転換の経緯**：
1. 「応答密度規約」新節の追加を検討 → 組み込み既定・既存スコープ規約と重複し不要と判断
2. 応答スコープ規約に反復禁止 1 行を追加 → 一旦実施
3. ブラウザ版 concise スタイル文面の存在を受け、出力スタイル機能での実装に方針変更
4. concise 単体の効果を純粋に観察するため、**独自二条項（スコープ制約・反復禁止）を
   応答スコープ規約から削除**し、concise 出力スタイルのみで運用開始

**成果物**：
- `~/.claude/output-styles/concise.md`（ブラウザ concise 文面から、Claude Code に無い
  UI 条項を削除。`keep-coding-instructions: true`）
- `CLAUDE.md` 応答スコープ規約から独自二 bullet を削除（残り 2 bullet）

**有効化**：`/config` → Output style → Concise を選択（次セッションから反映）。

### 設計判断：長さ上限フックの見送り

反復抑制の手段として (1) プロンプト規則 (2) 長さ上限 Stop フック (3) ユーザーの即時指摘、
の三段を検討。長さ閾値は恣意的で試行錯誤コストが高いため、まずプロンプト/スタイル単体で
運用し、効果不足なら閾値フックを追加する段階導入を選択。情報密度 = 情報量/文量のうち
分子（情報量）と「言い換え反復」は semantic で機械判定不可、分母（文量）のみ決定論的に
制約可能、という分析に基づく。
