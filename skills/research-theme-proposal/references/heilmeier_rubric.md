# Heilmeier Rubric (theme granularity)

DARPA の Heilmeier Catechism をテーマ提案粒度に適合させた質問群と、リーダー
（採点者）用ルーブリック。Phase 4 Rubric 層と Phase 5 の採点表で使用する。

## 8 問（テーマ粒度への適合）

| # | 原 Catechism | テーマ粒度での読み替え |
|---|---|---|
| H1 | What are you trying to do? No jargon | 非専門家に 3 文で説明できるか |
| H2 | How is it done today, limits? | survey の thesis / progress に接地した現状記述か |
| H3 | What is new, why successful? | **why now を必須化**: 「なぜ昨年でなく今か」に enabler の具体名で答える |
| H4 | Who cares? | 学術コミュニティ（どの venue の誰）と応用側の両方 |
| H5 | Risks? | Expected failure modes と整合しているか |
| H6 | Cost? | Data / compute budget と Readiness の New development 項目から見積もる |
| H7 | How long? | フル計画ではなく **de-risking までの期間**のみ答える |
| H8 | Mid-term / final exams? | mid-term = de-risking 実験 + kill criterion。final = 想定 venue の採録水準で何を示すか |

## 採点軸（各 1–5、アンカー付き）

| 軸 | 1 | 3 | 5 |
|---|---|---|---|
| **Novelty** | novelty-check で incremental 判定、差分が表現レベル | 差分は実質的だが先行研究の自然な次ステップ | distinct 判定かつ gap inventory の why-not-yet に新しい解を与える |
| **Why-now** | enabler が挙げられない / 汎用論（「LLM が進歩したから」） | enabler はあるが当該 gap への必然性が弱い | 具体的 enabler（手法名・データセット名）と gap の結合が一意 |
| **Interest** | 解けても誰の行動も変わらない | 当該サブ分野内では引用される | thesis レベルの緊張に触れ、隣接分野にも波及 |
| **Feasibility** | Readiness の過半が New development、または research-context の機材と不整合 | Adaptable 中心、改造工数が支配的 | Available + Adaptable で de-risk まで到達可能 |
| **Plan rigor** | baseline 不在 / 試行数・指標が未定 | baseline はあるが比較設計が甘い（条件不一致等） | 実在 baseline・統計的に意味のある試行数・実機評価コストまで見積もり済み |
| **Kill sharpness** | 非数値 / 事実上撤退不能な基準 | 数値だが閾値の根拠が薄い | 数値 + 閾値根拠（baseline 性能等）+ 検知時期が明確 |

## 合否基準

- **通過**: 全軸 3 以上 **かつ** Novelty・Feasibility・Kill sharpness のいずれか 2 軸が 4 以上
- **差し戻し**: いずれかの軸が 2 以下 → 当該軸の改善指示を 1-2 文で明記して返す
  （「もっと良くして」は禁止。何をどう直せば何点になるかを書く）
- **落選**: 改訂 2 回後も通過基準未達、または novelty_verdict が duplicate

## 採点表フォーマット（提案書 Rubric Scores 節に転記）

```markdown
| Axis | Score | Evidence (1 文) |
|------|-------|------------------|
| Novelty | 4 | novelty log P1: 最近接 3 本との差分が手法レベル |
| Why-now | ... | ... |
| Interest | ... | ... |
| Feasibility | ... | ... |
| Plan rigor | ... | ... |
| Kill sharpness | ... | ... |
| **Verdict** | PASS / REVISE / REJECT | iteration N/2 |
```

## 採点者への注意

- 採点は**証拠列必須**。証拠列に novelty log / survey / research-context の
  参照を書けない採点は無効（自己評価バイアスの抑制）
- ideator 本人・red-teamer は採点しない。採点はリーダーのみ
- 全候補に同じ順序で軸を適用する（候補間のハロー効果を避けるため、
  候補単位でなく**軸単位**で横断採点するのが望ましい）
