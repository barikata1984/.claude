# wrap-up-session

セッション終了時の定型処理。ドキュメント更新 → コミット → プッシュを一括実行する。「終わり」「おしまい」「セッション終了」「wrap up」「まとめて」といったリクエストや、作業の区切りで使用する。セッションの最後に呼ぶべきスキルなので、ユーザーが作業完了を示唆したら積極的に提案すること。

## 手順

1. `.claude/skills/log-progress/SKILL.md` の手順に従い、ドキュメントを更新する
2. ドキュメント更新が完了したら、`.claude/skills/commit-and-push/SKILL.md` の手順に従い、変更をコミット・プッシュする

## ルール

- 各ステップは必ず順番に実行する（log-progress → commit-and-push）
- log-progress で変更がなかった場合でも、セッション中に未コミットの変更があれば commit-and-push を実行する
- コミット対象がない場合は、その旨を通知して終了する

## コンテキスト

- ドキュメント更新ロジック: `.claude/skills/log-progress/SKILL.md` を参照
- コミット・プッシュロジック: `.claude/skills/commit-and-push/SKILL.md` を参照
