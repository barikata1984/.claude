# sweep-analyze

wandb API を使って sweep 結果を取得・分析し、知見を抽出する。

## 入力

以下のいずれかで sweep を特定する:

- **sweep ID**: wandb の sweep ID（例: `abc123de`）
- **sweep 名**: `log_sweep.md` のエントリ名
- **プロジェクト指定**: `--project phys-prop-aware` 等（デフォルト: `phys-prop-aware`）

不足情報はユーザーに質問する。

## 手順

### 1. データ取得

wandb API を使って sweep のメタデータと run 結果を取得する:

```python
import wandb
api = wandb.Api()
sweep = api.sweep(f"<entity>/<project>/<sweep_id>")
runs = sweep.runs
```

各 run から以下を収集する:
- config（ハイパーパラメータ）
- summary metrics（最終値: val/prior_loss, validation_loss 等）
- history（学習曲線: step ごとの loss 推移）
- state（finished / crashed / running）

### 2. 基本分析

以下の分析を実施し、結果を提示する:

#### a) ベストモデルの特定
- メトリック（val/prior_loss or validation_loss）でソートし、上位 N 件を表示
- 各 run のパラメータと最終メトリックの表

#### b) パラメータ別の影響分析
- 各探索パラメータについて、値ごとの平均メトリックを集計
- どのパラメータが性能に最も影響するかを特定
- 可能なら交互作用（2パラメータの組み合わせ効果）も確認

#### c) 学習曲線の概観
- 収束速度の比較（early stopping した step 数の分布）
- 発散・失敗した run の有無

#### d) ステータスサマリ
- 完了 / 実行中 / 失敗の run 数
- 失敗した run のエラーパターン（あれば）

#### e) Early stopping 設定の妥当性評価
- **停止ステップの分布**: パラメータ条件別の平均・範囲。極端に早い停止や上限到達が多い場合は設定見直しを提案
- **patience 消費パターン**: best_step と stopped_step の差分を分析。patience を常に使い切っている場合は不足、大幅に余っている場合は過剰
- **`min_delta_relative` の実効性**: 閾値（SMA × min_delta_relative）と val loss の典型的な揺らぎ幅を比較。閾値が揺らぎより極端に小さい場合は実質無効
- **`min_steps` の妥当性**: min_steps 時点の SMA と最終 SMA を比較。min_steps 以前に明確な発散がある run が多い場合は値を下げることを提案

### 3. 洞察の抽出

分析結果から以下を導出する:

- **最良パラメータ構成**: 推奨するハイパーパラメータの組み合わせ
- **次のステップ提案**: さらなる探索が必要か、探索範囲の絞り込みが可能か
- **予想外の発見**: 仮説に反する結果や興味深いパターン

### 4. 記録

結果を `docs/LOGS/log_sweep.md` の該当エントリの `### 結果` セクションに追記する:

```markdown
### 結果

**ベスト run**: `<run_id>` (val/prior_loss: <value>)
- <パラメータ構成>

**パラメータ影響度** (平均メトリック降順):
| Parameter | Value | Mean Loss | Std |
|-----------|-------|-----------|-----|
| ...       | ...   | ...       | ... |

**知見**:
- <箇条書きで主要な発見>

**Early stopping 評価**:
- 停止ステップ: 平均 <value>K (範囲 <min>K–<max>K)
- patience 消費: <分析結果>
- min_delta_relative 実効性: <分析結果>
- 推奨変更: <変更提案 or 「現行設定で妥当」>

**次のステップ**:
- <推奨するフォローアップ>
```

## ルール

- wandb API アクセスは `wandb login` 済みを前提とする
- entity 名は `wandb.Api().default_entity` から取得する
- ローカルの `wandb/` ディレクトリの run データも補助的に使用してよい
- 数値は有効桁 4 桁で丸める
- 分析結果はまず会話上で提示し、ユーザーの確認後にログに追記する
- skipped run（runtime ≈ 0s、unified sweep の pruning による）は分析から除外する
