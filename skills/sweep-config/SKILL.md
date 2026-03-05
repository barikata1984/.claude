# sweep-config

Sweep 計画に基づいて wandb sweep config YAML を生成・検証する。

## 入力

以下のいずれかから sweep 設定情報を取得する:

- `/sweep-plan` の結果（会話中 or `docs/LOGS/log_sweep.md` の最新エントリ）
- ユーザーからの直接指定（パラメータ名・値のリスト）

## 手順

### 1. ベース config の検証

1. 指定されたベース config YAML を読み込む
2. `scripts/train.py` のエントリポイントと `command:` セクションの互換性を確認する
3. ベース config で `use_wandb: true` が設定されていることを確認する

### 2. YAML 生成

既存の sweep config（`configs/sweep_*.yaml`）のフォーマットに従い、以下の構成で生成する:

```yaml
# Sweep config for <目的の簡潔な説明>
# Base: <ベースconfig名>
# <探索内容の要約>
#
# Usage:
#   cd catkin_ws/src/osx_bilateral
#   wandb sweep configs/<filename>.yaml
#   wandb agent <sweep_id>

project: phys-prop-aware
name: <sweep名>
program: scripts/train.py
method: <grid/random/bayes>
metric:
  name: <メトリック名>
  goal: minimize

parameters:
  # Dataset
  trainer.dataset-path:
    value: "<dataset名>"

  # Base config
  config:
    value: <ベースconfig>

  # Fixed overrides (ベースconfigと異なる固定パラメータ)
  ...

  # === Sweep parameters ===
  <パラメータ>:
    values: [...]

command:
  - ${env}
  - python3
  - ${program}
  - ${args}
```

### 3. 検証

生成した YAML について以下を確認する:

1. **パラメータ名の整合性**: CLI 引数名（kebab-case）が `TrainingConfig` / `MultiModalConfig` のフィールド名と一致するか
   - trainer 配下: `trainer.<field-name>` (例: `trainer.batch-size`)
   - model 配下: `model.<field-name>` (例: `model.embed-dim`)
   - ネスト: `model.transformer.<field>`, `model.cvae.<field>`
2. **値の型チェック**: int/float/bool/str が正しいか
3. **組み合わせ数**: grid の場合、全パラメータの values の直積を計算して表示する
4. **metric 名**: ACT の場合は `val/prior_loss`、非 ACT の場合は `validation_loss` が適切
5. **command セクション**: ベース config を `--config` で渡す場合は command に `--config` / `configs/...` を含める

### 4. 出力

1. 生成した YAML を `configs/sweep_<name>.yaml` に書き出す
2. ユーザーに以下を提示する:
   - 生成したファイルパス
   - 実行コマンド（`wandb sweep` + `wandb agent`）
   - 想定 run 数と探索パラメータの一覧

## ルール

- 既存の sweep config のスタイル・構造に合わせる（ヘッダコメント、パラメータ順序）
- `command` セクションは既存ファイルと一貫性を保つ
- ベース config の `--config` 指定方法を既存の sweep config から推測する（`config` パラメータ vs `command` セクション内）
- パラメータ名は Python (snake_case) ではなく CLI 形式 (kebab-case) で記述する
