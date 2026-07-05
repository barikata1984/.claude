# Hooks 運用ログ

## 2026-07-05: format-ja-typography フック削除

### 経緯

`hooks/format-ja-typography.sh` + `hooks/format_ja_typography.py`（PostToolUse フック。Markdown 保存時に全角句読点・括弧を半角に自動変換）を、`skills/japanese-tech-writing.md` の文章規範と突き合わせたところ、以下 2 点でルールが衝突していることが判明した。

- 用語定義の箇条書きで使う全角コロン（「**用語**：説明」）
- 引用に使う鉤括弧（「」『』）

フックはこれらを一律で半角/ASCII 記号に変換してしまい、規範側の意図と矛盾していた。

### 削除判断の理由

衝突 2 点の個別修正ではなくフック自体の削除に踏み切った理由は以下:

1. フックの担当範囲が本質的に狭い。em ダッシュ排除のような判断を要するルールは、当初から「生成時にプロンプト側で対応する」設計であり、機械的な字面変換で担える部分は元々限定的だった
2. blockquote（`>` 行）がマスク対象外だったため、引用文献の原文の句読点まで書き換えてしまうリスクがあった

### 実施内容

- `settings.json` の `PostToolUse` フック登録からエントリを削除
- `hooks/format-ja-typography.sh`, `hooks/format_ja_typography.py` を削除

対応する実装タスクは `notes/TODO.md`「和文タイポグラフィ正規化フック実装」（2026-05-22, 24 テスト全通過）としてチェック済みだったが、当該実装自体を撤回した形になる。
