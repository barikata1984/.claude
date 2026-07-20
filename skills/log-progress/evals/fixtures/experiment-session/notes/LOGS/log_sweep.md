# log_sweep

## 2026-07-18 sweep k9x2m4p1 (lr x batch grid)

- 目的: lr {1e-3, 3e-4, 1e-4} x batch {128, 256, 512} の grid
- 設定: configs/sweep_lr_batch.yaml, 24 runs

## 2026-07-19 sweep k9x2m4p1 分析結果 (sweep-analyze 追記)

- best: lr=3e-4, batch=256, val_loss 0.412
- OOM: batch=512 の 2 runs
