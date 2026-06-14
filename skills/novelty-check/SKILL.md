---
name: novelty-check
description: "Verify the novelty of a research idea or proposal by searching for the nearest prior work and writing a differential analysis log with a distinct/incremental/duplicate verdict. Also verifies that named baselines actually exist. Use this skill whenever a research candidate, seed, or proposal needs novelty verification against existing literature, when the user asks 'has this been done before', 'is this novel', 'check prior art', or when research-theme-proposal Phase 4 dispatches per-candidate novelty checks."
---

# Novelty Check Skill

研究候補 1 件に対し、最近接の先行研究を**積極的に探しに行き**、差分分析ログと
verdict を返す skill。reference-verify（実在確認）の上位互換ではなく相補:
reference-verify は「挙げた論文が実在するか」、本 skill は「挙げて**いない**
論文が存在しないか」を検証する。

## 原則

自己評価は信用しない。novelty の主張は「探したが見つからなかった」という
**検索の失敗の記録**によってのみ支持される。したがって本 skill の成果物は
verdict ではなく**検索ログ**であり、verdict はその要約にすぎない。

## 入力

- 候補概要（research-theme-proposal Phase 3 の 1 ページ概要）または提案書のパス
- 出力先パス（既定: `output/proposals/novelty/{proposal_id}-{slug}.md`）

## Workflow

### Step 1: クエリ展開

候補の中核主張から検索クエリを **3 系統以上**展開する:

1. **直接系**: 中核主張のキーワードそのまま（同義語・略語展開込み。
   literature-survey の Keyword Construction 規約を流用）
2. **構造系**: 手法と対象を入れ替えた一般形（「X を Y に適用」なら
   「X application」「Y with learned methods」等）
3. **隣接系**: cross-domain 候補なら移植元分野での類似適用、
   enabler 候補なら同じ enabler を使う他タスクの研究

### Step 2: 検索実行

literature-survey の `references/search_sources.md` のカスケードに従う:
Semantic Scholar MCP → OpenAlex script → arXiv API → WebSearch。
**直近 6 ヶ月の arXiv を必ず含める**（採録前の競合が最大のリスク）。

各系統で上位ヒットを確認し、**最近接 5–10 本**を確定する。

### Step 3: 差分分析

最近接の各論文について:

- 1 行で「何をやったか」
- 候補との差分を **problem / method / evaluation** の 3 レベルで判定
  （どのレベルで違うかを明示。「なんとなく違う」は不可）

### Step 4: Baseline 実在確認

候補が baseline として挙げる手法それぞれについて:

- 論文の実在を確認（reference-verify の Step 1 手順を inline 実行。
  6 本以上なら reference-verify skill を起動）
- 公開実装の有無と repo URL

### Step 5: Verdict

| verdict | 基準 |
|---|---|
| **distinct** | 最近接論文との差分が problem または method レベルで実質的 |
| **incremental** | 差分は evaluation レベルのみ、または method の表現替え。差分を明確化できれば再提出可 |
| **duplicate** | 中核主張と同一の研究が存在する（即落選） |

判定に迷う場合は incremental に倒す（false negative の方が安い）。

## 出力形式

```markdown
# Novelty Log: {proposal_id} <title>

## Queries executed
| 系統 | Query | Source | Hits reviewed |
|---|---|---|---|

## Nearest prior work (N=5–10)
| # | Paper (year, venue) | 1-line | Diff level | Diff summary |
|---|---|---|---|---|

## Baselines verified
| Baseline | Exists | Impl. | Note |
|---|---|---|---|

## Verdict: distinct / incremental / duplicate
**根拠** (2-3 文): ...
**カバーできていない検索角度** (red-team A1 への引き継ぎ): ...
```

「カバーできていない角度」の自己申告は必須。red-team の A1 攻撃はここから
始まるため、空欄は red-team の攻撃失敗を偽装する行為とみなされる。

## 環境フォールバック

MCP 不通時は OpenAlex / arXiv API / WebSearch のみで実行し、ログ冒頭に
縮退内容を記録する。検索系統を 3 未満しか実行できなかった場合、verdict は
distinct を出せない（最大 incremental）。
