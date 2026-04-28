# Section-by-Section Question Bank

Full question sets for each section of the interactive design mode. Use 2–3 questions per section
depending on how much the user has already shared. Skip questions the user has already answered.

---

## Section 1: Research Motivation

**Goal**: Establish why this problem matters, to whom, and why now.

**Questions:**

Q1-a (jargon-free summary — ask before Q1-b and Q1-c; skip only if the user already gave a jargon-free description unprompted):
> "この研究で解こうとしている問題を、専門知識のない人（家族や学部1年生など）に説明するつもりで1〜2文で書いてみてください。専門用語は使わないで。"
>
> (English: "Describe the problem you're trying to solve in 1–2 sentences, as if explaining to someone
> outside your field. No jargon.")

This is the Heilmeier diagnostic. If the user can't do it, that's important information — it means the
problem framing needs more work before anything else.

If the user answers Q1-a with method names, architectures, or field-specific terms (e.g., "RL + IL の統合" instead of a problem statement a layperson could follow), note this and ask again with a concrete example: "まだ専門用語なしの説明ができていないので、もう一度試してみてください。例えば『〇〇が難しいせいで、ロボットは新しい場所で転んでしまう』のような感じで。"

Q1-b (stakes):
> "この問題が解決されると、誰の何が具体的に変わりますか？できれば数値や具体例を使って。"
>
> (English: "If this problem were solved, what would concretely change for whom? Numbers or examples
> preferred.")

Q1-c (timing):
> "なぜ今この問題に取り組むのですか？1年前では早すぎて、1年後では遅すぎる、という理由はありますか？"
>
> (English: "Why is now the right time? What makes this problem tractable today that wasn't before?")

**What good answers look like:**
- Problem stated in plain language without loss of meaning
- Specific stakeholder identified (not "the research community" — who exactly?)
- Clear connection to recent technical enablers (new datasets, compute, methods)

**Common issues:**
- "It's an interesting problem" — not a motivation, ask for impact
- "Everyone in the field knows this is important" — that's not an argument, that's an appeal to
  authority; push for a concrete reason

---

## Section 2: Current State & Gaps

**Goal**: Show what exists and precisely where it falls short.

**Questions:**

Q2-a (existing methods):
> "現在この問題に最もよくアプローチしている手法を2〜3つ挙げてください。できれば論文名・著者名も。"
>
> (English: "Name 2–3 methods that currently best address this problem. Paper names and authors if
> possible.")

Q2-b (specific limitations):
> "それらの手法の限界を、できるだけ具体的に教えてください。どのベンチマーク・設定で、どのくらい失敗しますか？"
>
> (English: "What are the specific limitations of those methods? On which benchmarks or conditions do
> they fail, and by how much?")

Q2-c (your gap):
> "あなたが解こうとしている問題に既存手法を適用すると、どこで詰まりますか？"
>
> (English: "If you tried to apply existing methods directly to your problem, where exactly would they
> break down?")

**What good answers look like:**
- Specific paper names and years cited (not "existing methods")
- Quantitative limitations ("achieves 60% success on task X but requires 10 hours of training")
- Clear mapping: existing method → specific failure mode → proposed solution

**Common issues:**
- Vague: "existing methods are not good enough" — push for specifics
- Missing baseline knowledge: if the user can't name the top methods, they need more literature review
  before writing the proposal

---

## Section 3: Contribution Type

**Goal**: Clarify what *kind* of contribution this is — ML research has multiple valid types.

**Questions:**

Q3-a (contribution type — ask first):
> "この研究の主な貢献は次のどれに当たりますか？複数でもOKです：
> (A) 新しいアルゴリズム・手法の提案
> (B) 既存ベンチマークでの性能改善
> (C) 新しい問題設定・タスクの定義
> (D) 新しいデータセット・ベンチマークの作成
> (E) 効率化（同等性能でより少ない計算・データ）
> (F) 理論的解析・説明
> (G) その他"
>
> (English: "What type of contribution is this primarily? A) New algorithm/method, B) Performance
> improvement on existing benchmarks, C) New problem formulation/task, D) New dataset/benchmark,
> E) Efficiency (same performance, less compute/data), F) Theoretical analysis, G) Other")

Q3-b (novelty claim):
> "先行研究と比べて、何が根本的に新しいですか？一文で言い切ってみてください。"
>
> (English: "What is fundamentally new compared to prior work? Try to state it in one sentence.")

**Why this matters**: The contribution type determines what the evaluation plan needs to demonstrate.
A method paper needs ablations. A benchmark paper needs diverse evaluations. An efficiency paper needs
compute comparisons. Getting this clear early shapes everything else.

**What good answers look like:**
- Unambiguous primary contribution type
- Novelty claim that an expert could evaluate (not "we combine X and Y in a novel way")

**Common issues:**
- "We improve over existing methods" — that's a result, not a contribution type; is the novelty
  the algorithm, the problem framing, or the insight?
- Multiple contribution types claimed equally — usually one is primary; help the user identify it

---

## Section 4: Proposed Approach

**Goal**: Describe the core idea and explain why it should work.

**Questions:**

Q4-a (core idea):
> "提案手法のコアアイデアを2〜3文で教えてください。まず直感的な説明から始めて、必要なら技術的な詳細に進みましょう。"
>
> (English: "Describe the core idea in 2–3 sentences. Start with the intuition, then add technical
> detail if needed.")

Q4-b (why it works):
> "なぜそれがうまくいくと思いますか？理論的な根拠、予備実験の結果、または類似手法の成功事例があれば教えてください。"
>
> (English: "Why do you believe this will work? Theoretical reasoning, preliminary experiments, or
> analogous successes in related work?")

Q4-c (comparison to baselines):
> "既存の最良手法と比べて、何が根本的に違いますか？どのコンポーネントが新しいですか？"
>
> (English: "What's fundamentally different from the best existing method? Which component is novel?")

**What good answers look like:**
- Intuitive explanation that a graduate student in an adjacent subfield could follow
- At least one reason to believe the approach will work (not just "we'll try it and see")
- Clear delineation of what's borrowed from prior work vs. what's new

**Common issues:**
- "We use a transformer" — architecture choice alone is not a contribution; what's different about
  how it's used or trained?
- "The idea is novel, trust me" — push for the specific insight

---

## Section 5: Evaluation Plan

**Goal**: Define how the hypothesis will be tested, before doing any experiments.

**Questions:**

Q5-a (benchmarks):
> "どのベンチマーク・データセットで評価しますか？具体名を挙げてください。複数使う場合、それぞれを選んだ理由は？"
>
> (English: "Which benchmarks or datasets will you evaluate on? Please name them. If multiple, why
> each one?")

Q5-b (baselines):
> "比較するベースライン手法を3つ以上挙げてください。それぞれを選んだ理由も。"
>
> (English: "Name at least 3 baseline methods you'll compare against, and why each one is included.")

Q5-c (metrics and targets):
> "主要な評価指標は何ですか？数値目標はありますか？（例：Push-T で成功率90%以上）"
>
> (English: "What are your primary evaluation metrics? Any numerical targets?
> e.g., '≥90% success on Push-T'")

Q5-d (ablations — especially for method papers):
> "提案手法のどのコンポーネントが効いているかを確認するためのアブレーション計画はありますか？"
>
> (English: "What's your ablation plan — how will you isolate the contribution of each component?")

**What good answers look like:**
- Specific benchmark names (not "standard benchmarks")
- Baselines include the strongest competing method, not just easy ones
- Metrics match the contribution type (accuracy for performance claims, FLOPs for efficiency claims)
- Ablation design removes one component at a time against a clear control

**Common issues:**
- "We'll evaluate on several benchmarks" — which ones? Why?
- Baselines chosen because they're easy to beat — push for the most competitive baselines
- No ablation plan — for a method paper this is a significant gap

**Benchmark saturation warning**: If the proposed benchmark is near-saturated (year-over-year
improvements within noise), ask: "What will you do if the improvement is within the evaluation noise?
Is there a more discriminating benchmark or task?"

---

## Section 6: Timeline & Milestones

**Goal**: Break the research into realistic phases with intermediate checkpoints.

**Questions:**

Q6-a (overall duration):
> "この研究にどれくらいの期間を想定していますか？（卒論、修士論文、論文投稿、など）"
>
> (English: "What's the overall time horizon? Thesis, conference submission, etc.?")

Q6-b (phases):
> "大まかに分けると、どんなフェーズになりますか？各フェーズの目標は？"
>
> (English: "What are the rough phases of the work? What does each phase accomplish?")

Q6-c (intermediate checkpoints):
> "各フェーズの終わりに、「次に進む価値があるか」を判断するための中間検証は何ですか？"
>
> (English: "At the end of each phase, what intermediate result would tell you it's worth continuing?")

**What good answers look like:**
- Phases that build on each other logically (proof-of-concept → prototype → full evaluation)
- Each phase has a concrete exit criterion, not just "complete the implementation"
- Realistic time estimates (compare with similar past projects)

**Common issues:**
- All experiments and analysis compressed into the last month — flag this
- No intermediate checkpoints — the proposal assumes everything works until the end
- Underestimating implementation time (infrastructure, debugging, data prep often take 2–3× longer
  than expected)

**Template for a single phase:**
```
Phase N: [Name] (Weeks X–Y)
- What will be done
- Intermediate checkpoint: [specific measurable condition]
- If checkpoint fails: [what this means and what to try next]
```

---

## Section 7: Risks & Alternatives

**Goal**: Identify realistic failure scenarios and credible responses to each.

**Questions:**

Q7-a (main failure scenarios):
> "この研究が想定通りに進まない最大のリスクは何ですか？技術的な失敗シナリオを2〜3つ挙げてください。"
>
> (English: "What are the 2–3 biggest technical risks? What could go wrong with the core approach?")

Q7-b (fallback plans):
> "それぞれのリスクに対して、代替案はありますか？"
>
> (English: "For each risk, what's the fallback plan?")

Q7-c (negative results):
> "提案手法が既存手法に勝てなかった場合、この研究はどう着地しますか？"
>
> (English: "If your method doesn't beat existing approaches, how does the project land? Is there
> still a publishable story?")

**What good answers look like:**
- Specific, technically grounded risks (not "it might not work")
- Fallback plans that are realistic, not just "we'll figure it out"
- A negative result scenario that still yields a publishable contribution

**Risk table template:**
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [scenario] | Low/Med/High | Low/Med/High | [specific action] |

**ML-specific risks to probe for if not mentioned:**
- Benchmark saturation: "What if the chosen benchmark is already saturated and your gains are within
  noise?"
- Silent training failures: "How will you verify that training is working as expected beyond just
  watching the loss curve?"
- Compute cost overrun: "What if training takes 10× longer than expected?"
- Data pipeline bugs: "How will you sanity-check the data before committing to a large training run?"

---

## Sections 8–9: Robot Learning (activate if applicable)

### Section 8: Sim-to-Real Strategy

Q8-a:
> "学習はシミュレーションで行いますか？使用するシミュレーション環境は何ですか？"

Q8-b:
> "Sim-to-Realギャップにどう対処しますか？（ドメインランダマイゼーション、real2sim2real、オンライン適応、など）"

Q8-c:
> "実機実験に移行する前に、方策が転送可能かどうかをどう検証しますか？"

### Section 9: Hardware & Safety

Q9-a:
> "使用するロボットプラットフォームは何ですか？主な制約（自由度、センサ、オンボード計算量、コスト）は？"

Q9-b:
> "タスクは準静的（低リスク）ですか、動的（ハードウェア損傷リスクあり）ですか？"

Q9-c:
> "実機実験での安全対策は何ですか？（ケージ、非常停止、実験監視体制など）"

Q9-d:
> "実機の使用時間へのアクセスはどうなっていますか？（研究室所有、共有設備、外部機関）"
