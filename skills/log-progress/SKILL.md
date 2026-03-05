# log-progress

セッション終了時に呼び出し、会話内容に基づいてドキュメントを更新する。

## 手順

1. 会話を分析し、進捗・発見・解決済み課題を特定する
2. 以下のファイルを適切に更新する:
   - `docs/TODO.md` — 完了した項目に `[x]` を付ける。新たに発生したタスクを追加する
   - `docs/LOGS/log_*.md` — 該当するトピックのログに結果・発見を追記する（末尾に append）
   - `docs/ISSUES.md` — 新たに発見した課題を追加する。解決した課題は項目ごと削除する
   - `docs/PLAN.md` — 設計判断が変わった場合のみ更新する

## 参考文献の処理

ログに文献を引用した場合、以下を必ず行う:

1. **本文中**: インラインキーをクリッカブルリンクにする
   - 例: `[[Tsujita2008]](../REFERENCES/MAIN.md#Tsujita2008)`
   - パスはログファイルからの相対パス（`docs/LOGS/` 配下なら `../REFERENCES/MAIN.md#Key`）

2. **セクション末尾**: `#### 参考文献` セクションを追加し、引用した文献を短縮形で列挙する
   ```markdown
   #### 参考文献
   - [[Tsujita2008]](../REFERENCES/MAIN.md#Tsujita2008) — discount γ=0.99 がバックスイングを抑制
   ```

3. **REFERENCES/MAIN.md の更新**: `docs/REFERENCES/MAIN.md` を読み、引用キーのエントリが存在するか確認する
   - 存在しない場合 → 適切なカテゴリに `<a id="Key"></a>**[Key]** Authors, "Title", Venue, Year.` 形式で追加
   - 存在する場合 → 追加不要

引用キーの命名規則: `[著者姓Year]` または `[略称Year]`。詳細は `docs/REFERENCES/STYLE.md` を参照。

## ルール

- LOGS は **append-only**。過去の記録は編集しない
- ISSUES は解決済み項目を **削除** する（アーカイブしない）
- 各ファイルの既存フォーマットを維持する
- 日付は ISO 形式 (YYYY-MM-DD) を使用する
- 変更がない場合はファイルを触らない
