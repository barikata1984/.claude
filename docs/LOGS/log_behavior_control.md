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
