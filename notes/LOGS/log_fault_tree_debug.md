# Log: fault-tree-debug

## 2026-06-04: fault-tree-debug SKILL.md の empirical prompt tuning

### 対象と動機
`skills/fault-tree-debug/SKILL.md`（Fault Tree Analysis によるデバッグ手法）の指示品質を empirical-prompt-tuning で検証・改善。

### シナリオ
- A（中央値）: stale-closure — イベント駆動プロセッサで config 更新が handler に反映されない（test_case_7）
- B（edge）: silent-data-corruption — パイプラインで float64→float32 ダウンキャストが 0.4% の数値ずれを生む（test_case_6）

両シナリオともユーザーが誤った仮説を提示する設計（A: event_bus が原因、B: aggregator が原因）。

### 露呈した問題と対策

**問題 1: Phase 2 の「コードを読むな」が実践不可能**

元の指示 "Do this BEFORE reading any source code related to the bug" は、Read ツールでファイルを開くと全体が表示される現実と矛盾。Iter 2 で厳格化（"do NOT read function bodies"）したところ、シナリオ B の実行者が Read でファイルを開いた時点で指示違反を自覚し精度 100%→90% に低下（失敗が可視化された）。

対策: 指示の意図を「物理的にコードを見ない」から「見えてもロジック分析は後回しにする」に切り替え。"Build hypotheses from structure, not from code logic ... if the tool shows more than that, ignore function bodies and logic for now"。Iter 3 でシナリオ B が 100% に回復。

残存: 「見えても無視する」は実行者の認知的規律に依存。ツール側の制約でありこれ以上は skill で対処不能。

**問題 2: ユーザー仮説の扱いが未定義**

全 iter で「ユーザーが提示した仮説をどう扱うか SKILL.md に記載がない」と裁量補完が報告された。結果的に全実行者が適切に処理したが記述に穴があった。

対策: Phase 2 に "If the user suggests a likely cause, include it as a hypothesis — but treat it the same as any other" を追記。Iter 4 で裁量補完から消滅。

### メトリクス推移

| iter | A 精度 | A steps | B 精度 | B steps |
|---|---|---|---|---|
| 1（ベースライン） | 100% | 13 | 100% | 21 |
| 2（厳格化） | 100% | 10 | 90% | 25 |
| 3（認知的規律へ切替） | 100% | 14 | 100% | 18 |
| 4（ユーザー仮説追記） | 100% | 14 | 100% | 24 |

### 収束判定
質的指標（不明瞭点 0 件 × 2 連続、精度 100% × 3 連続）は完全収束。steps/duration のばらつきは subagent の探索深度のランダム性に起因し skill の問題ではない。実質収束として停止。SKILL.md への変更は計 3 箇所（Phase 2 の読み方ガイド書き換え + ユーザー仮説の扱い追記）。

