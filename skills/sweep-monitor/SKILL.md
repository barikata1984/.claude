# sweep-monitor

Sweep 実行中の GPU リソース使用状況を定期記録する。将来の自動 GPU 割当基準の策定に使うデータを蓄積する。

全パスは `catkin_ws/src/osx_bilateral/` からの相対。

## 目的

- sweep 中のモデル × バッチサイズ × GPU の組み合わせごとに、実際の GPU 利用率とメモリ消費を記録する
- このデータを蓄積し、将来「このモデル構成なら GPU を共有できるか」を定量的に判断できるようにする

## 手順

### 1. モニタリング開始

tmux セッションでバックグラウンド記録を開始する:

```bash
tmux new-session -d -s "sweep-monitor" \
  "nvidia-smi --query-gpu=timestamp,index,name,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw \
   --format=csv,nounits -l 30 \
   >> docs/LOGS/gpu_monitor_<sweep_id>_<date>.csv"
```

- サンプリング間隔: 30 秒（`-l 30`）
- 出力先: `docs/LOGS/gpu_monitor_<sweep_id>_<YYYYMMDD>.csv`

### 2. モニタリング停止

sweep 完了後、または `/sweep-monitor stop` で tmux セッションを終了する:

```bash
tmux kill-session -t sweep-monitor
```

### 3. データ分析

記録された CSV を読み込み、以下を集計・提示する:

#### a) GPU 別サマリ
| GPU | Util% (mean/max/p95) | Memory (mean/max) | Power (mean) |
|-----|----------------------|--------------------|--------------|
| 0   | 45% / 98% / 92%     | 8.2G / 12.1G       | 180W         |

#### b) 時系列パターン
- 訓練中の定常状態における util% の範囲
- バッチ読み込み時の谷（GPU idle）の有無と深さ
- メモリ使用量の安定性（リークの兆候がないか）

#### c) 並列化可能性の評価
GPU ごとに以下を判定:
- **util p95 < 50% かつ memory max < 50%**: 同 GPU に 2 agent 載せられる可能性あり
- **util p95 > 80%**: compute 飽和、共有不可
- **memory max > 70%**: メモリ余裕なし、共有不可

### 4. 記録

分析結果を `docs/LOGS/log_sweep.md` の該当エントリに追記する:

```markdown
### リソース使用状況
- モニタリング期間: <開始> 〜 <終了>
- データ: `docs/LOGS/gpu_monitor_<id>_<date>.csv`

| GPU | Util% (mean/p95) | Memory (mean/max) | 並列化可否 |
|-----|-------------------|--------------------|------------|
| ... | ...               | ...                | ...        |
```

## ルール

- モニタリングは sweep 以外の訓練（単発 `train.py` 実行）にも使用可能
- CSV ファイルは上書きせず、sweep_id + 日付で一意にする
- 既にモニタリングセッション (`sweep-monitor`) が存在する場合は警告し、追加起動しない
- 分析結果はまず会話上で提示し、ユーザー確認後にログに追記する
