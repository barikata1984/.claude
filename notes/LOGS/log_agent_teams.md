# Agent Teams 設定ログ

## 2026-06-04: ルールファイル作成と検証

### 背景

Agent Teams 機能（`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`）が有効化済みだったが、TeamCreate ツールが使われず Agent の並列 spawn で代用されていた。TeamCreate を適切な場面で使うためのルールファイルを作成した。

### 実施内容

1. **事前調査**
   - TeamCreate / TaskCreate / SendMessage / TeamDelete のスキーマを取得・照合
   - 公式ドキュメント（code.claude.com）で Agent Teams のベストプラクティスを確認
   - `~/.claude/rules/*.md` に配置する方針を確定（既存パターンと一致、teammates は project CLAUDE.md を自動読み込み）

2. **ルールファイル作成**: `~/.claude/rules/agent-teams.md`
   - When to Use: 3 件以上の独立タスク、依存関係あり、異なる役割の協調
   - When NOT to Use: 単発調査、2 件以下、会話的やりとり
   - Standard Workflow: TeamCreate → TaskCreate → Agent(team_name) → TaskUpdate(owner) → SendMessage → shutdown → TeamDelete
   - Best Practices: チーム 3–5 人、タスク最大 5–6 件/人、name 参照、idle 正常

3. **empirical-prompt-tuning 検証**
   - シナリオ A（中央値）: 4 モジュール並列移行 → TeamCreate 使用すべき
   - シナリオ B（edge）: 2 件バグ修正 → TeamCreate 不要
   - シナリオ C（hold-out）: 依存関係パイプライン（調査→設計→並列実装→テスト）→ TeamCreate + blockedBy/blocks
   - 4 イテレーション + hold-out、全シナリオ精度 100%

4. **修正 2 件**
   - Iter 2: 「5–6 タスク」→「最大 5–6 件を目安. 少なければ 1 人 1 件でも良い」（タスク粒度の曖昧さ解消）
   - Iter 3: `shutdown_request` → `message: {type: "shutdown_request"}` 明示（送信形式の曖昧さ低減）

### 残存事項

- Agent spawn vs メインセッション直接対処の使い分け: rules ファイルのスコープ外（TeamCreate 判断が目的）として対処不要と判断
- 実運用での効果観察が未実施
