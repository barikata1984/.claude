# sweep

Sweep 実験管理の統合エントリポイント。引数またはコンテキストに応じてサブスキルを呼び分ける。

## 使い方

```
/sweep              → コンテキストから自動判定
/sweep plan         → 実験計画の立案（/sweep-plan）
/sweep config       → sweep config YAML の生成（/sweep-config）
/sweep run          → sweep エージェントを tmux で起動（/sweep-run）
/sweep monitor      → GPU リソースモニタリング開始（/sweep-monitor）
/sweep analyze      → sweep 結果の分析（/sweep-analyze）
/sweep full         → plan → config → run + monitor → analyze を順に実行
```

## 自動判定ロジック

引数なしで呼ばれた場合、以下の優先順で判定する:

1. 会話中に sweep 結果や sweep ID への言及がある → **analyze**
2. sweep が実行中（tmux セッションが存在） → **monitor** の状況確認を提示
3. 会話中に `/sweep-plan` の結果（パラメータ選定済み）がある → **config**
4. 上記いずれでもない → **plan** から開始

## full モード

`/sweep full` が指定された場合、以下を順に実行する:

1. `/sweep-plan` — 目的の明確化とパラメータ選定
2. `/sweep-config` — YAML 生成と検証
3. `/sweep-run` — GPU 状況表示 → ユーザー判断 → tmux でエージェント起動
4. `/sweep-monitor` — リソースモニタリング開始（並行）
5. （sweep 完了後に再度呼ばれた場合）`/sweep-analyze` — 結果分析 + モニタリングデータ集計

各フェーズの間でユーザーの承認を得てから次に進む。

## 共通コンテキスト

全サブスキルで共通する参照先:

- **プロジェクト構成**: `src/training/config.py`, `src/models/configs/multi_modal_config.py`
- **wandb ユーティリティ**: `src/training/wandb_utils.py`
- **既存 sweep config**: `configs/sweep_*.yaml`
- **実験ログ**: `docs/LOGS/log_sweep.md`
- **GPU モニタリングデータ**: `docs/LOGS/gpu_monitor_*.csv`
- **戦略ドキュメント**: `docs/archive/wandb_sweep_unified_strategy.md`
