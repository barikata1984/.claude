# sweep-run

Sweep エージェントを tmux セッションで起動する。GPU 状況を表示し、ユーザーの判断に基づいて並列数・GPU 割当を決定する。

全パスは `catkin_ws/src/osx_bilateral/` からの相対。

## 入力

以下のいずれかで sweep を特定する:

- **sweep ID**: `wandb sweep` の出力から得た ID（例: `entity/project/abc123de`）
- **sweep config**: 未登録の YAML パス → `wandb sweep` で登録してから agent を起動する

## 手順

### 1. GPU 状況の表示

`nvidia-smi` を実行し、以下をユーザーに提示する:

```
GPU  Name           Util%  Memory         Status
  0  RTX 3090       12%    1.2G / 24.0G   空き
  1  RTX 3090       97%   20.1G / 24.0G   使用中
  2  RTX 3090        0%    0.4G / 24.0G   空き
```

- Util > 80% または Memory 使用 > 80% の GPU は「使用中」と表示する
- それ以外は「空き」と表示する

### 2. ユーザーに判断を委ねる

以下をユーザーに質問する:

- **何並列で起動するか**（空き GPU 数をデフォルト値として提案）
- **どの GPU に割り当てるか**（空き GPU の番号をデフォルトとして提案）

### 3. tmux セッションの起動

ユーザーの指定に基づき、各エージェントを個別の tmux セッションで起動する:

```bash
# セッション命名: <sweep名>-<sweep_id短縮>-<agent番号>
tmux new-session -d -s "<name>-<id>-0" \
  "cd catkin_ws/src/osx_bilateral && CUDA_VISIBLE_DEVICES=<gpu> wandb agent <sweep_id>"

tmux new-session -d -s "<name>-<id>-1" \
  "cd catkin_ws/src/osx_bilateral && CUDA_VISIBLE_DEVICES=<gpu> wandb agent <sweep_id>"
```

### 4. 起動確認

起動後に以下を表示する:

```
起動完了:
  sweep: <sweep名> (<sweep_id>)
  sessions:
    - <session_name_0> → GPU 0
    - <session_name_1> → GPU 2

確認コマンド:
  tmux ls                          # セッション一覧
  tmux attach -t <session_name>    # セッションに接続
  wandb sweep cancel <sweep_id>    # sweep 中止
```

## ルール

- GPU 割当はユーザーが決定する。自動判定しない
- 各 agent は `CUDA_VISIBLE_DEVICES` で 1 GPU に固定する
- sweep ID が未指定の場合、`configs/sweep_*.yaml` の一覧を提示して選択させる
- 既に同名の tmux セッションが存在する場合は警告する
- `wandb sweep` の登録と `wandb agent` の起動は分けて実行し、sweep ID を明示する
