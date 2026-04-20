# Skills 汎用化ログ

## 2026-03-19: スキル定義の調査と修正開始

### 調査対象
- commit, push, commit-and-push, log-progress, wrap-up-session

### 発見した問題

1. **commit/push に `ros-o` がハードコード** — 特定プロジェクトのメインブランチ名が埋め込まれており、汎用スキルとして不適切
2. **log-progress にファイルパスがハードコード** — `docs/TODO.md`, `docs/LOGS/`, `docs/ISSUES.md`, `docs/PLAN.md` が固定。フォークプロジェクト等で成立しない
3. **log-progress の参照処理ルール** — `.claude/rules/references.md` は研究プロジェクト固有
4. **ユーザーレベル CLAUDE.md にプロジェクト固有の内容が混在** — 検証コマンド、コンテナ環境、参照先、注意事項が osx_ose_for_learning_manipulation 固有

### 実施した修正
- commit/SKILL.md: `ros-o` への警告ルールを削除
- push/SKILL.md: `ros-o` への特別処理（警告・確認・force push 禁止）を削除

### 議論と方針決定
- ブランチ保護は必要なプロジェクトでプロジェクトレベルの CLAUDE.md に個別定義する
- log-progress は役割定義をスキルに残しつつ、パス解決は CLAUDE.md に委ねる方針に
- ユーザーレベル CLAUDE.md を汎用化し、スクラッチプロジェクトの標準ドキュメント構成を明記する

### 追加修正
- log-progress/SKILL.md: パスのハードコードを除去。CLAUDE.md からのパス解決 + ファイルが存在しなければスキップする設計に変更。参照処理は `.claude/rules/references.md` が存在する場合のみ適用に緩和
- CLAUDE.md: プロジェクト固有の内容（コマンド、コーディング規約の一部、注意事項、コンテナ環境、参照先）を `~/_CLAUDE.md` に退避。汎用的な内容のみ残し、「標準ドキュメント構成」セクションを新設
- wrap-up-session/SKILL.md: 確認の結果、変更不要

### 残作業
- `~/_CLAUDE.md` の内容を対象プロジェクトの CLAUDE.md に配置する（対象プロジェクトでの作業時に実施）

---

## 2026-04-20: 知識ソース明示ルールの策定と request-source スキル実装

### 背景

Isaac Sim ロープシミュレーションのデバッグ中、内部知識のみで API 挙動を断言し誤った説明をした。
その原因の内省と、再発防止のための構造的対策を議論・実装した。

### 内省の結論

- 「パターンマッチが発火した瞬間に確信に変わり、検証ステップが消えた」
- CLAUDE.md のルールは「外部から課された制約」であり、内側から自然に発火しない
- ルールの想起が能動的に必要な構造では、高速なパターンマッチに負ける

### 実装内容

**CLAUDE.md への追記（`~/.claude/CLAUDE.md`）:**
- 知識ソース明示ルール: 全回答末尾に `[知識ソース]` ブロック（内部知識／外部知識／観測事実 の3分類）を水平バーで分離して付与
- WebSearch/WebFetch 必須トリガー: A〜F の6カテゴリ（API仕様・エラー診断・推論マーカー・数値根拠・環境依存・学術工学情報）に該当する場合は判断なしに即実行

**request-source スキル（`~/.claude/skills/request-source/SKILL.md`）:**
- `/request-source この回答` または `/request-source 直前の回答` で知識ソースブロックを生成
- 発火タイミングはスキル内では定義せず、CLAUDE.md のルールに委ねる

### 調査で判明した構造的限界

- CLAUDE.md はセッション開始時のコンテキストに入るが、hooks のような確実な自動発火はない
- `Stop` フックはレスポンステキストを検査できないため、ブロック有無の機械的チェックは不可能
- スキルは tool call として実行され「編纂中の回答への末尾追記」は構造的に不可能
- 結論: CLAUDE.md ルール（自発的遵守）＋ユーザーの明示呼び出し（`/request-source`）の組み合わせが現時点の最善

### 用語の整理

- 「未検証」「WebSearch/WebFetch 未実施」という表現を廃止
- 「内部知識」（学習データ由来）と「外部知識」（このセッションでの WebSearch/WebFetch 結果）に統一
