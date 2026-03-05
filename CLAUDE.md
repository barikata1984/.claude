# Inertia-Conditioned Robot Manipulation Learning

## ワークフロー

- 3ステップ以上のタスクは Plan Mode から開始せよ
- 調査・分析タスクはサブエージェントに委譲し、メインコンテキストを保護せよ
- 実装完了を自己宣言するな。テスト実行・差分確認・ログ確認で動作を実証せよ
- バグ報告を受けたらまずログ・エラー・テストから自力調査せよ。質問は調査後に
- 修正指摘を受けたら MEMORY.md に教訓を記録せよ
- セッション終了時は /log-progress で進捗を記録せよ

## コマンド

### 検証（コンテナ起動後に順番に実行）

```bash
python scripts/sanity_check.py
python scripts/test_foundation.py
python scripts/test_tasks.py
python scripts/train.py --max-iterations 2 --num-envs 2 --save-interval 1
```

### 学習

```bash
python scripts/train.py --task hammer --ablation-condition grid-8 --max-iterations 1000
python scripts/train.py --task hammer --device cuda --num-envs 256 --max-iterations 5000
```

### 評価

```bash
python scripts/eval.py --checkpoint results/<run>/model_1000.pt --num-episodes 100
python scripts/eval.py --checkpoint results/<run>/model_1000.pt --save-video --video-episodes 3
python scripts/eval.py --checkpoint results/<run>/model_1000.pt --generalization --density-patterns all
```

### WandB Sweep

```bash
wandb sweep configs/sweep_hammer.yaml
wandb agent <sweep-id>
```

## コーディング規約

- **Formatter**: `ruff format`
- **Linter**: `ruff check`
- **Type hints**: Python 3.10+ annotations required
- **Line length**: 100 characters
- **Import order**: stdlib → third-party → local (enforced by ruff isort)
- **Docstrings**: Google style, only for non-obvious functions
- Gymnasium `gymnasium.Env` interface for CPU prototyping
- Mass grids: always shape `(N, N, N)`, float32
- `np.random.Generator`（legacy `np.random` 禁止）
- Config: Python dataclasses + tyro CLI. YAML files for reference/sweep configs
- MJCF で inertial properties はランタイム上書き可能に設計

## Git Workflow

- **Commit format**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`)
- **Main branch**: `main`

## 注意事項（知らないと間違うもの）

- **MJCF はランタイムで慣性パラメータを上書きする設計**。XML 内の `<inertial>` はデフォルト値。環境リセット時に `model.body_mass` / `model.body_inertia` を書き換え → `mj_setConst()` で派生量を再計算。
- **ハンマーは剛体取り付け**。freejoint + weld ではなく、グリッパーボディに `MjSpec.attach()` で直接接続。
- **`train_args.json`** が各 run の results/ に保存される。eval.py はこれを読み込んでモデル構成を完全復元する。

## コンテナ環境

- Python venv: `/opt/venv/bin/python`
- MuJoCo Menagerie: `/opt/mujoco_menagerie/`
- editable install 済み: `pip install --no-deps -e /workspace`

## 参照先

- 研究計画・仮説・ablation 条件: docs/PLAN.md
- 進捗チェックリスト: docs/TODO.md
- 実験記録: docs/LOGS/README.md（インデックス）→ docs/LOGS/（トピック別ログ）
- 未解決の技術課題: docs/ISSUES.md
- ドキュメントガイド: docs/README.md
- 報酬設計リファレンス: configs/hammer_swing.yaml
- 参考文献マスタ: docs/REFERENCES/MAIN.md（引用規約: docs/REFERENCES/STYLE.md）
