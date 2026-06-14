# Proposal Template

`output/proposals/P{N}-{slug}.md` の必須形式. YAML frontmatter とセクション見出しは
`.claude/hooks/check_proposal.py` の検証対象なので**一字一句変えない**こと.

```markdown
---
proposal_id: P1
title: "<English title>"
mechanism: enabler-driven   # enabler-driven | cross-domain-transfer | benchmark-definition | assumption-busting
survey_slug: <survey_slug>
gap_refs: ["gap-3", "matrix-empty:tactile×long-horizon"]   # gap inventory 内の ID
status: screened            # draft | screened | accepted | rejected (検証は screened のみ)
iteration: 1                # 改訂回数（最大 2）
novelty_log: output/proposals/novelty/P1-<slug>.md
novelty_verdict: distinct   # distinct | incremental | duplicate
baselines_verified: true    # reference-verify / novelty-check による実在確認済みか
citations_total: 9
citations_recent_18mo: 4
kill_criterion_quantified: true
human_approved: false       # 人間チェックポイント通過前は必ず false
---

# P1: <Title>

## Heilmeier Answers

<!-- references/heilmeier_rubric.md の 8 問にテーマ粒度で回答。各 2-5 文 -->

### H1. What are you trying to do? (no jargon)
### H2. How is it done today, and what are the limits?
### H3. What is new, and why now (not last year)?
### H4. Who cares? What difference does it make?
### H5. What are the risks?
### H6. Resource estimate
### H7. How long will the first de-risking take?
### H8. What are the mid-term and final exams?

## Gap Grounding

<!-- survey のどの gap / 空セル / 横断 limitation に根差すか。
     survey への wikilink と gap_refs の対応を明記。推測でなく survey 根拠で -->

## Approach Sketch

<!-- 手法の完全な仕様ではなく「議論の土台」。読者の「で、何がしたいの?」を防ぐ。
     確定済みの設計と未確定の設計を区別して書く。全 5 フィールド必須
     (機械チェック対象) -->

- **構成要素と動作原理**: <要素ごとに 2-4 文。数式・指標は概観レベルでよいが、
  「それをどうやってコスト関数化 / 評価指標化 / 学習目的化するのか」に答えること。
  名前を挙げるだけの要素 (例: 「ガウス測度を使う」) は不可>
- **要素間の依存関係**: <各要素は独立に検証可能か。どの要素が落ちると全体が
  崩れるか。循環依存 (要素 A の成立が要素 B の成果物を前提とし、B が A を前提と
  する等) がないことを明示>
- **統合方針**: <要素を対象課題に対してどう組み合わせるか 2-3 文。
  offline / online、設計則 / 適応則などのスコープを明示>
- **対抗系統と比較方針**: <survey の concept matrix クラスタ単位で対抗手法系統を
  列挙し、比較対象に含める / 含めないを理由付きで明記。含める場合は比較設計を
  一言で。系統の見落としは red-team A3 の攻撃対象>
- **未確定事項**: <de-risk 以降に確定する設計点。人間と議論したい論点を明示>

## Required Components & Readiness

<!-- literature-survey の seed_format.md と同形式。
     ただし Status 判定は research-context.md と突き合わせること:
     ラボに機材・スキルが無い要素は論文上 Available でも Adaptable 以下に落とす -->

| Component | Status | Detail (paper / lab capability mapping) |
|-----------|--------|------------------------------------------|
| ... | Available / Adaptable / New development required | ... |

## Mini Experiment Plan

<!-- スケジュールではなく feasibility の証拠。全フィールド必須 -->

- **Task & embodiment**: <タスクと、research-context.md のどの機材で実施するか>
- **Sim / Real**: <選択と理由。real なら評価コストの見積もりも>
- **Baselines**:

| Baseline | Public impl. | Verified | Why this baseline |
|----------|--------------|----------|-------------------|
| <実在手法名> | <repo URL or none> | yes/no | ... |

- **Metrics & trials**: <指標と試行数。実機なら統計的に意味のある最小試行数>
- **Data / compute budget**: <デモ本数 or データ量、GPU 構成 × 日数>
- **De-risking experiment (first 2–4 weeks)**: <仮説を最安で潰す実験>
- **Kill criterion**: <数値で。例: 「de-risk 実験で成功率が baseline +5pt 未満なら撤退」>
- **Expected failure modes**: <2-3 個と、それぞれの早期検知方法>

## Red-team Record

<!-- redteam_protocol.md の攻撃と応答の要約。攻撃が無かった項目も「未攻撃」と明記 -->

| Attack | Verdict | Resolution |
|--------|---------|------------|
| ... | survived / revised / conceded | ... |

## Rubric Scores

<!-- heilmeier_rubric.md の採点表をそのまま転記。リーダー（採点者）が記入 -->

## References

<!-- 全引用。reference-verify 通過済みであること。8 本以上、うち直近 18 ヶ月 3 本以上 -->
```

## 記述ルール

- 提案書は self-contained にする(survey を読まずに判断できる程度に Gap Grounding
  で文脈を与える). ただし詳細は wikilink で survey / 深読みノートへ飛ばす
- 数値・手法名・引用は novelty ログまたは survey に根拠があるもののみ.
  根拠のない"一般に知られている"系の主張で Heilmeier に答えない
- kill criterion の禁止表現:"十分な性能が出なければ""有望でなければ"等の
  非数値表現. hook が `kill_criterion_quantified: true` と本文の整合を見る
