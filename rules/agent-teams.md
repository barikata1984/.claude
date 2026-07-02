# Agent Teams Rules

## When to Use TeamCreate

以下のいずれかに該当するとき, Agent ツールの単発 spawn ではなく TeamCreate でチームを構成する:

- ユーザーが「チーム」「並列で」「分担して」等の協調作業を示唆した
- 独立した 3 件以上のタスクがあり, 並列実行で明確に速くなる
- タスク間に依存関係があり, blockedBy / blocks による順序制御が必要
- 実装 + テスト + レビューなど異なる役割の協調が必要

## When NOT to Use

- 単発の調査・検索・検証 → Agent (subagent) で十分
- 2 件以下の独立タスク → Agent の並列 spawn で十分
- 会話的なやりとり・簡単な質問への回答

## Standard Workflow

1. **TeamCreate**: チーム作成 (`team_name`, `description`)
2. **TaskCreate**: 作業を分割してタスク登録. 依存関係は `addBlockedBy` / `addBlocks` で設定
3. **Agent**: `team_name` と `name` を指定してメンバーを spawn. `subagent_type` はタスクに応じて選択:
   - 実装・編集が必要 → `general-purpose` (デフォルト)
   - 読み取り専用の調査 → `Explore`
   - 設計・計画 → `Plan`
4. **TaskUpdate**: タスクの `owner` を設定して割り当て
5. **SendMessage**: メンバーへの指示・フィードバック (名前で宛先指定)
6. **完了後**: SendMessage で `message: {type: "shutdown_request"}` を各メンバーに送信 → TeamDelete でクリーンアップ

## Subagent Reporting

Agent ツールでサブエージェントを spawn するときは, プロンプトに「完了時に SendMessage で報告せよ」という指示を含める. 後から催促するのは無駄なラウンドトリップになる.

## Best Practices

- チーム規模は 3–5 人から開始する. 不必要に大きくしない
- 各メンバーに割り当てるタスクは最大 5–6 件を目安とする. タスク総数が少なければ 1 人 1 件でも良い
- spawn 時のプロンプトにタスク固有のコンテキストを十分含める
- メンバーは名前 (`name`) で参照する. `agentId` は使わない
- メンバーが idle になるのは正常. エラーではない
- タスク完了後は TaskList で次の未割り当てタスクを確認する
- メンバーからのメッセージは自動配信される. inbox の手動チェックは不要

## Progress Management with Workflow

複数エージェントの進捗管理には Workflow ツールを使う:

- `phase(title)` で作業フェーズを宣言し, 進捗表示をグループ化する
- `log(message)` で要所ごとに進捗メッセージを出す
- `meta.phases` にフェーズ一覧を事前定義し, `/workflows` で進捗を可視化する
- `pipeline()` / `parallel()` 内の `agent()` には `phase` オプションを明示して, 正しいグループに帰属させる

### TeamCreate との使い分け

| 状況 | 選択 |
|---|---|
| 制御フローが決定的 (ループ, 条件分岐, fan-out → 集約) | Workflow |
| タスク間の依存が動的に変わる, 人間のフィードバックを挟む | TeamCreate + TaskCreate |
| 単発の並列実行 (2–3 件) | Agent の並列 spawn |
