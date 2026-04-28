## Claude's initial response

Great — using foundation model representations to improve sample efficiency in offline RL is a promising direction. Before we structure anything, let me ask a few focused questions so I understand what's already clear in your mind and what still needs to be worked out.

**First, a quick Heilmeier-test question (Section 1 — Research Motivation):**

> Describe the problem you're trying to solve in 1–2 sentences, as if explaining it to someone outside your field — a friend who doesn't know what reinforcement learning is. No jargon.

This is less of a test and more of a diagnostic: if the plain-language framing comes easily, your motivation is solid. If it's hard, that's where we should spend time first.

---

**Second, on contribution type (Section 3) — this needs clarification:**

Looking at your idea, it could land in several different places. Which of these best describes what you're going for?

> (A) A new algorithm/method — you're proposing a specific way to extract or adapt foundation model representations for offline RL  
> (B) A performance improvement — you're primarily showing that existing ideas work better with foundation model features on standard benchmarks  
> (C) An efficiency contribution — same final performance as the state of the art, but requiring significantly less offline data  
> (E) A combination of A and C — a new method *whose primary claim* is data efficiency  

This matters a lot because it determines what your evaluation needs to prove. An efficiency claim (C or E) needs a very different experimental design than a method novelty claim (A) — you'd need to show sample efficiency curves, not just final performance numbers.

---

**Third, directly on the evaluation gap you mentioned (Section 5 — Evaluation Plan):**

You said you haven't figured out the evaluation plan yet. Let's start here rather than leave it to the end:

> 1. Which offline RL benchmarks are you considering? (e.g., D4RL, Calvin, something domain-specific?) If you're not sure yet, that's fine — just tell me what problem domain you're targeting.
> 2. How do you intend to measure "sample efficiency"? A few options:
>    - Plot final policy performance as a function of dataset size (the most common approach)
>    - Fix a performance threshold and measure how little data is needed to reach it
>    - Compare against an online RL baseline to frame the offline efficiency gain
> 3. What would a "win" look like concretely — e.g., "match the performance of [baseline] using 10× less data"?

You don't need to have all of this figured out now, but your advisor will almost certainly ask these questions in the first five minutes of your meeting. Let's get ahead of them.

---

Take these one at a time — start with whichever feels most natural, and we'll build from there.

---

## Simulated user answer

So for the plain-language version: "I want to train AI agents to make good decisions using only pre-collected data, but normally you need a huge amount of that data. I think we can reuse knowledge from large pretrained models to need much less data." For the contribution type, I think it's mostly E — same performance but less data — though I do have a specific idea for how to use the representations so maybe also A. For evaluation, I was thinking D4RL as the benchmark, but I'm not sure which metrics to use beyond return. I haven't thought about baselines much yet.

---

## Claude's follow-up

Your plain-language summary is actually quite good — that's exactly the kind of framing that will help your advisor follow the argument. Let me reflect back what I heard and then push on the specifics:

**What I understood:**
You want to show that a foundation model's pretrained representations can serve as a richer feature space for offline RL, reducing the amount of offline data needed to reach good policy performance — and you have a specific method idea for how to use those representations (not just plug-and-play). The primary contribution is efficiency (E), with a secondary claim of novelty in the representation-use mechanism (A). Is that right?

If yes, here's why clarifying the A vs. E split matters: an E-only paper has a clean, testable thesis ("same return, less data") but may feel incremental. An A+E paper is harder to write but more defensible if the method itself is novel. Your advisor will likely ask: "What's the insight? Why does using foundation model representations help specifically with data efficiency, rather than just helping in general?" — you should have a one-sentence answer ready.

---

**Now let's sharpen the evaluation plan (Section 5), since you've identified D4RL:**

D4RL is a reasonable starting point, but I want to push on three things:

**1. Which D4RL tasks and data splits?**
D4RL has multiple domains (Gym locomotion, AntMaze, kitchen, Adroit) and data quality splits (random, medium, medium-replay, expert). Sample efficiency claims play out very differently across these. The kitchen and Adroit tasks are generally harder and lower-data regimes — more interesting for an efficiency claim. Which are you targeting, and why?

**2. Your baseline set — this is currently empty and it's the biggest gap.**

For an efficiency + method paper, you need at least three types of baselines:
- A strong offline RL baseline *without* foundation model features (e.g., IQL, TD3+BC, or DT depending on your approach) — this isolates the effect of the representation
- An offline RL baseline *with* a simpler representation (e.g., random network features, or a smaller supervised model) — this isolates the effect of using a *foundation* model specifically, versus any pretrained model
- An oracle or data-efficiency upper bound (e.g., the same offline RL algorithm trained on the full dataset) — this frames the efficiency gain

Without these three, you can't cleanly argue that the foundation model representation is what's doing the work.

**3. Metrics beyond return:**

For an efficiency claim, normalized return alone is not enough. You should also plan to report:
- **Learning curves vs. dataset fraction** — your main efficiency narrative
- **Performance at multiple data budgets** (e.g., 1%, 5%, 10%, 50%, 100% of the dataset) — gives your advisor a picture of where the method shines
- Optionally: **compute cost of the representation extraction step** — if your advisor asks "is this just better because foundation models are bigger?", you'll want an answer

---

**One question before we move on to Section 4 (your proposed method):**

> What foundation model are you thinking of using, and what part of it do you plan to use as the representation — raw embeddings, fine-tuned features, something else? The answer shapes what "your method" actually is.

Once I understand that, we can draft a one-sentence novelty claim and then check whether the evaluation plan you've sketched actually tests that specific claim.

---

[知識ソース]
内部知識：
- D4RL benchmark structure (domains, data quality splits)
- Standard offline RL baselines: IQL, TD3+BC, Decision Transformer
- Evaluation methodology for sample efficiency claims in offline RL (learning curves vs. dataset fraction)
- Heilmeier Catechism framing for research motivation
- Contribution type taxonomy as defined in the research-proposal skill

外部知識：
- なし

観測事実：
- Skill files read at /home/ak/.claude/skills/research-proposal/SKILL.md and /home/ak/.claude/skills/research-proposal/references/sections.md
- Session setup confirmed: mode = interactive design, language = English, subfield = ML (robot learning module NOT activated)
- User's stated gap: evaluation plan not yet developed
- Output saved to /home/ak/.claude/skills/research-proposal-workspace/iteration-1/eval-2-offline-rl-english/with_skill/outputs/response.md
