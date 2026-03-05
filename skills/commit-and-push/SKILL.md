# commit-and-push

`/commit` と `/push` を順に実行する統合コマンド。セッション中の変更または git 差分をコミットし、リモートにプッシュする。コミットしてプッシュしたい、変更を反映したい、といったリクエストで使用する。

## 使い方

```
/commit-and-push    → コミット + プッシュを順に実行
/commit             → コミットのみ（プッシュしない）
/push               → プッシュのみ（コミット済みの変更を対象）
```

## 手順

1. `.claude/skills/commit/SKILL.md` の手順に従い、変更をコミットする
2. コミットが成功した場合、`.claude/skills/push/SKILL.md` の手順に従い、リモートにプッシュする
3. 最終結果として `git status` と `git log --oneline -5` を表示する

## コンテキスト

- コミットのロジック: `.claude/skills/commit/SKILL.md` を参照
- プッシュのロジック: `.claude/skills/push/SKILL.md` を参照
