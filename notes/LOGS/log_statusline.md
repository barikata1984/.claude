# Statusline 設定ログ

## 2026-06-29: statusline-command.sh 復元と表示修正

### 問題

`~/.claude/statusline-command.sh` がファイルではなく空ディレクトリになっており、ステータスラインが表示されなくなっていた。

### 原因調査

全ブランチを確認したが、`.gitignore` で除外されていたためどこにもコミットされていなかった。
もう一台のマシンからリモートにプッシュしてもらい、`git pull` で復元した。

### 修正内容

1. **Line 1: `📊 XX%` の重複表示を削除** — コンテキスト使用率が二重に出ていた
2. **Line 1: 区切りを `│` から `@` スタイルに変更**
3. **Line 1: 作業ディレクトリ名 `📁 dirname` を末尾に追加**
4. **Line 2: コスト表示を Line 3 から Line 2 に統合** — 3行表示から2行表示に削減
5. **`✏️` 後のダブルスペースを修正**

### 発見: ステータスラインの配布制約

ステータスラインはプラグイン/マーケットプレイスの共有対象外。
`settings.json` の `statusline` キー + スクリプトファイル (`statusline-command.sh`) の両方が必要なため、ドットファイルリポジトリでの配布が唯一の手段。

### git 管理への追加

`.gitignore` から `statusline-command.sh` を削除し、git 追跡対象に変更した。
以後は他マシンとの同期が `git pull` で可能になった。

## 2026-07-05: effort.level 表示の追加

`statusline-command.sh` に、ステータスライン JSON 入力の `effort.level` を表示する処理を追加した。

- モデル名の直後に `w/ {effort}` を表示（`effort.level` が存在しない場合は省略）
- Line 1 の項目順序を並べ替え: `🤖 {model} w/ {effort} ✏️ +N/-N of 📁 {dirname} @ 🔀 {branch}`（従来はブランチがディレクトリ名より先で、両方に `@` 区切りを使用していた）
