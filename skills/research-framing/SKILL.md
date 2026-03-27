---
name: research-framing
description: >
  Use this skill whenever the user needs to establish, clarify, or articulate the
  core direction and positioning of something new — a research paper, a business
  proposal, an investor pitch, or any situation where a new idea needs to be framed
  convincingly for an audience. This skill MUST be used — do not attempt to handle
  these tasks with general conversation alone.

  Trigger on any of the following, even if the user does not say "framing":
  - Wants to define or sharpen a take-home message, core message, or main claim
  - Wants to write or refine a contribution statement or list of contributions
  - Wants to position their work against prior art, competitors, or existing solutions
  - Wants to build a logical structure that moves from "why this matters" to
    "what is missing" to "what we do about it" (CARS: Territory, Niche, Occupation)
  - Says things like "what is my paper about", "how do I frame this", "what should I
    claim", "what is the novelty", "how do I differentiate", "what gap does this fill",
    "how do I pitch this", "what problem does this solve"
  - Is starting a new research project or business initiative and exploring directions
  - Has results or a product but has not yet articulated what they mean or why they matter
  - Needs to explain to stakeholders, investors, or reviewers why something is worth doing

  Default mode is academic paper (RA-L). For other contexts (business, pitch, etc.),
  the user can specify the audience and the skill adapts accordingly.
  Produces research_framing_output.md. Delegates literature survey to /literature-survey.
allowed-tools: Read, Write, WebSearch
user-invocable: true
---

# Research Framing: 研究・提案の方向づけ

## このスキルの目的

research_framing_output.mdを生成することで、研究・提案の方向づけを完了させる。
文献調査を`/literature-survey`スキルに委譲しながら、3つのステージを対話形式で進め、
最終成果物として `research_framing_output.md` を生成する。

**完了条件**: 以下の3アイテムが確定し、相互に整合していること。
- Take-home message（1文）
- Contribution statement（3〜5文）
- 研究ポジショニング（CARS 3ムーブの骨格）

---

## ステップ0: 起動時の確認

既存の `research_framing_output.md` が存在する場合は内容を読み込み、
どのステージまで完了しているかをユーザーに伝える。完了済みステージはスキップ可能。

次に、以下の1問だけを尋ねる。

> 「研究テーマや技術的アプローチはすでに固まっていますか？
> （例：実験が進行中、使う手法は決まっている、など）
> それとも、これから方向性を探索したい段階ですか？」

回答に応じて**モードB**または**モードA**に進む。

---

## モードB: テーマ確定済み（実験が進行中のプロジェクト向け）

### B-1: 研究の現状をヒアリングする

以下の質問を**1つずつ**行う。前の回答を受けて次の質問を調整する。
3問は「手法・結果・意義」の3軸を引き出すために設計されており、
take-home messageに必要な素材がこの3軸から構成されるためである。

1. 「研究テーマと使っている手法を簡単に説明してください。」
2. 「実験で得られた（または得られる見込みの）最も重要な結果は何ですか？」
3. 「この研究がなければ、ロボティクスの実践者はどんな問題に直面し続けますか？」

3つの回答を受けて、Take-home message の候補を **2〜3案**提示する。
複数案を提示するのは、研究者が「自分が言いたいこと」を外から見ると
意外と言語化できていないことが多いためで、候補を見て「これは違う」と
言える状態にすることが言語化の助けになるからである。

```
候補1: [手法] により [問題] を解決し、[定量結果] を達成した。
候補2: [観察/発見] を利用することで、[タスク] において [改善] が可能であることを示す。
候補3: （回答内容に応じた別フォーミュラ）
```

「最も近いものはどれですか？修正点があれば教えてください。」
修正を受けてA1（Take-home message）を確定し、「A1が完了しました」と宣言する。

### B-2: 文献調査を実行する（A1確定後）

A1が確定したら、ユーザーに以下を伝える。

> 「A1が確定しました。次に、研究ポジショニング（A3）を構築するために
> `/literature-survey` スキルで関連先行研究を調べます。
> スコープと調査深度は `/literature-survey` スキルのPhase 1で確認します。
> 調査結果は `docs/SURVEYS/` に保存されます。進めてよいですか？」

承認を得たら、以下の情報を会話上に明示してから `/literature-survey` スキルを起動する。

> 「文献調査のスコープ:
> - トピック: [A1のtake-home messageから抽出したキーワード（英語）]
> - 深度: focused（隣接分野は含めない）
> - seed: 不要（研究の方向性は確定済み）
> - 目的: research-framing CARS骨格の構築
> `/literature-survey` を開始してください。」

`/literature-survey` 完了後、生成された調査レポート（`docs/SURVEYS/<topic_slug>.md`）を読み込み、
以下の2点を確認する。

- 「見落としている重要な先行研究はありますか？」
- 「調査結果を踏まえて、A1を修正したい点はありますか？」

### B-3: A2（Contribution statement）を定義する

貢献の種類を確認する（1問）。

> 「この研究の貢献は主にどれですか？（複数可）
> 1. 新しい手法・アルゴリズムの提案
> 2. 既存手法では解けなかった問題への適用・拡張
> 3. 新しい評価軸・知見・洞察の提供
> 4. その他」

回答と文献調査レポートのGapセクションを照合し、以下の構造でドラフトを生成する。
文1でGapと対応させるのは、RA-Lの査読者がcontribution statementを読む時、
「なぜこの研究が必要か」をIntroductionより先にAbstractで判断するためである。
先行研究のギャップと自分の貢献が対応していることが、
contribution statementの説得力の根拠になる。

```
文1: 問題の設定（何が課題か）← 文献調査のGapと対応させる
文2: アプローチ（何をしたか）← A1の手法部分を展開
文3: 主要な結果（何が示されたか）← A1の結果部分を展開
文4: （あれば）副次的な知見・実機での検証
文5: （あれば）先行研究との明示的な差分 ← 文献調査のGapから引用
```

「不正確な点や追加すべき貢献はありますか？」
修正を受けてA2を確定し、「A2が完了しました」と宣言する。

### B-4: A3（CARS骨格）を構築する

文献調査レポートとA1・A2を材料として、3ムーブを構築する。
文献調査レポートの各セクションと以下のCARSムーブが対応する。

| 文献調査レポートのセクション | CARSムーブ |
|---|---|
| Research Landscape Overview + Foundation + Progress | Move 1: Territory |
| Gap（構造的未解決問題） | Move 2: Niche |
| A1 + A2 | Move 3: Occupation |

**Move 1: Territory**（2〜3文）
文献調査のResearch Landscape OverviewとFoundationを要約して提示する。
「この記述に追加・修正はありますか？」

**Move 2: Niche**（1〜2文）
文献調査のGapセクションからA2の差分と最も対応するギャップを抽出して提示する。
「このギャップの記述は、あなたの研究が解決する問題を正確に表していますか？」

**Move 3: Occupation**（1〜2文）
A1・A2から自動生成し、確認のみ行う。

**CARS統合骨格**（8〜12文）を生成する。ユーザーに提示する**前に**、以下の手順でサブエージェントによるレビューを実行する。

**A3レビュー（サブエージェント経由、ユーザー提示前に実行）**

**ステップ1: レビュー入力ファイルの作成**

以下の内容を `.tmp/cars_review_input.md` に書き出す。

```markdown
# CARS骨格レビュー入力

## レビュー対象: CARS統合骨格
[生成した8〜12文の骨格をそのまま記載]

## 照合資料

### A1: Take-home message
[確定済みのA1]

### A2: Contribution statement
[確定済みのA2]

## レビュー基準（4項目すべてを評価すること）

1. **Territory→Nicheの導線**: TerritoryがNicheの前提として機能しているか。
   「A分野が重要だ」→「しかしXが未解決だ」の論理的流れになっているか。
2. **Niche→Occupationの対応**: Nicheで指摘したギャップを、Occupationが正確に埋めているか。
   別の問題を解いていないか。
3. **A1・A2との整合**: OccupationがA1・A2の内容と矛盾していないか。
   CARS骨格とcontribution statementで異なる主張をしていないか。
4. **RA-L査読者視点**: 背景知識のない査読者が「なぜこの研究が必要か」を理解できるか。

## 出力形式

`.tmp/cars_review_output.md` に以下の形式で出力すること。

### 評価結果
| 基準 | 判定 | コメント |
|------|------|---------|
| Territory→Niche | OK / NG | [具体的な指摘] |
| Niche→Occupation | OK / NG | [具体的な指摘] |
| A1・A2との整合 | OK / NG | [具体的な指摘] |
| RA-L査読者視点 | OK / NG | [具体的な指摘] |

### 修正提案
[NGがある場合のみ。骨格の該当箇所と修正案を具体的に記載。なければ「修正不要」と記載]
```

**ステップ2: サブエージェントの起動**

Taskツールを使ってサブエージェントを起動する。タスク指示は以下の通り。

```
`.tmp/cars_review_input.md` を読み、記載されているレビュー基準に従って
CARS統合骨格を評価し、結果を `.tmp/cars_review_output.md` に書き出してください。
メインの会話履歴は参照せず、このファイルの情報のみに基づいて評価してください。
```

**ステップ3: レビュー結果の反映**

サブエージェント完了後、`.tmp/cars_review_output.md` を読み込む。
NGの有無と種類に応じて以下の3つのパスに分岐する。

---

**パスX: すべてOKの場合**

評価結果は提示しない。骨格のみユーザーに提示し、
「これはIntroduction第1〜2段落の骨格です。C2（セクション別ドラフト）で本文に発展させます。」と伝える。
`.tmp/`の両ファイルを削除し、「A3が完了しました。Research Framingが完了しました」と宣言する。

---

**パスY: 文章表現・論理構造の問題（A1/A2の内容は正しいが骨格の書き方に問題がある場合）**

該当するのは以下のようなケース:
- Territory→Nicheの接続が唐突で論理的飛躍がある
- Nicheの記述が抽象的すぎて具体的な問題が伝わらない
- Occupationの記述がA1/A2と矛盾はしないが言い回しが冗長・不明確

エージェントは以下の手順をとる。

1. レビュー結果の要約（何がNGだったか）と修正案を提示する。
2. 「修正案でよいですか？別の修正方針があれば教えてください。」と確認する。
3. ユーザーの承認または修正指示を受けて骨格を更新する。
4. 更新した骨格で再レビューを実行する（ステップ1〜2を再実行）。
5. 再レビュー結果がOKであれば、パスXと同様にユーザーに提示して確定する。
   再レビューでもNGが残った場合は、残っている問題を具体的にユーザーに提示し、
   以下の3択を示す。
   - **A. さらに修正指示を与える** → 指示に従って骨格を更新し、手順4に戻る。
   - **B. A1/A2の見直しに戻る** → パスZのA（B-3へ戻る）と同じ対応をとる。
   - **C. 現状のまま確定する** → 現在の骨格をユーザーに提示して確定する。
   ループの継続・終了はユーザーが決定する。

`.tmp/`の両ファイルを削除し、「A3が完了しました。Research Framingが完了しました」と宣言する。

---

**パスZ: A1/A2との不整合（骨格がA1/A2の内容と矛盾している場合）**

該当するのは以下のようなケース:
- OccupationがA1のtake-home messageと異なる主張をしている
- NicheがA2のcontribution statementで解くと言っている問題と食い違っている
- A2で挙げた貢献がOccupationに反映されていない

エージェントは骨格を修正**しない**。A1とA2はAtsushiが対話を通じて確定した内容であり、
その内容に起因する不整合をエージェントが勝手に解消すると、確定済みの研究の定義が
無断で変わることになる。不整合の解消方法（A1/A2を直すか、骨格の記述を直すか）は
研究者自身が判断すべき問題である。以下の手順をとる。

1. 問題を具体的にユーザーに提示する。
   例:「Occupationでは『物体の姿勢推定を改善する』と記述されていますが、
   A1のtake-home messageは『慣性特性を活用したgrasping』を主張しています。
   どちらが正しい研究の焦点ですか？」
2. 以下の2択を提示する。
   - **A. A1/A2を修正する** → B-3に戻り、A2のcontribution statementから見直す。
   - **B. CARS骨格の記述を修正する** → ユーザーの指示に従って骨格を修正し、パスYの再レビューに進む。
3. ユーザーの選択に従って対応する。

`.tmp/`の両ファイルはユーザーの選択後に削除する。

---

## モードA: テーマ探索中（新規プロジェクト向け）

### A-1: 探索の起点をヒアリングする

以下の質問を**1つずつ**行う。

1. 「興味のある研究領域・問題意識を教えてください。論文のタイトルでも、
   漠然とした課題感でも構いません。」
2. 「この領域でこれまでに読んだ論文や、気になっているアプローチはありますか？」
3. 「利用できる実験環境・データ・設備を教えてください。
   （例: UR5e実機、MuJoCo、特定のデータセット等）」

### A-2: 広域文献調査を実行する

ヒアリング結果を受けて、ユーザーに以下を伝える。

> 「方向性の探索のために `/literature-survey` スキルで広域調査を実行します。
> 調査後、見えてきたギャップをもとに研究の方向性を一緒に絞り込みます。
> `seed`（研究アイデアの提案）セクションも生成するよう指示します。進めてよいですか？」

承認を得たら、以下の情報を会話上に明示してから `/literature-survey` スキルを起動する。

> 「文献調査のスコープ:
> - トピック: [ヒアリングで得たキーワード・問題意識（英語）]
> - 深度: broad（隣接分野を含む）
> - seed: 必要（研究の方向性を探索中）
> - 制約: [A-1で得た実験環境・設備の情報]（seedの実現可能性評価に使用）
> `/literature-survey` を開始してください。」

### A-3: ギャップ仮説からA1を絞り込む

`/literature-survey` 完了後、Seedセクションに含まれる研究アイデアをユーザーに提示し、
以下を確認する。

> 「この中で、あなたの興味・実験環境と最も合致するものはどれですか？
> または、これを見て別のアイデアが浮かんだ場合は教えてください。」

ユーザーの選択・反応を受けて、Take-home message の候補を2〜3案提示する。
修正を受けてA1を確定し、「A1が完了しました」と宣言する。

### A-4: A2（Contribution statement）を定義する

モードBのB-3と同じ手順で実行する。

ただしこの段階では実験結果が未確定のため、
「〜を達成することを目指す」「〜を示す予定である」という表現を使い、
その旨をドキュメントに明記する。

### A-5: A3（CARS骨格）を構築する

モードBのB-4と同じ手順で実行する（A3セルフレビューを含む）。
広域文献調査のGapとSeedがNicheとOccupationの素材として使える。

---

## Research Framing 完了: research_framing_output.md の生成

全ステージが完了したら、`research_framing_output.md` を生成する。

```markdown
# Research Framing 出力: 研究・提案の方向づけ
<!-- generated: YYYY-MM-DD -->
<!-- mode: A / B -->
<!-- status: complete / provisional（モードAの場合） -->
<!-- literature-survey-report: docs/SURVEYS/<topic_slug>.md -->

## A1: Take-home message

[確定した1文]

## A2: Contribution statement

[確定した3〜5文]

<!-- モードAの場合: ⚠️ 仮定義。B3（実験の実行と結果取得）完了後に更新すること -->

## A3: 研究ポジショニング（CARS骨格）

### Move 1: Territory
[文献調査のResearch Landscape Overview / Foundationを要約した2〜3文]

### Move 2: Niche
[文献調査のGapセクションから抽出した1〜2文]
<!-- 参照: docs/SURVEYS/<topic_slug>.md → Survey Findings → Gap -->

### Move 3: Occupation
[A1・A2から生成した1〜2文]

### CARS統合骨格（Introduction第1〜2段落の原型）
[8〜12文の骨格]

## Phase Bへの引き継ぎ情報

### B1（技術アプローチの選定）で参照すべき先行研究
<!-- docs/SURVEYS/<topic_slug>.md の Paper Catalogue から抽出 -->
[文献リスト]

### ベースライン候補（比較・アブレーション設計の起点）
<!-- A2の差分記述と文献調査のGapから抽出 -->
[候補リスト]

### 未解決の問題・検討事項
[対話中に出てきた未確定事項]
```

---

## 進行上の注意

**1ターンに1質問。** 複数の質問を一度に投げると、ユーザーは重要な問いへの回答が
薄くなるか、一部を見落とす。このスキルの質問はどれも研究・提案の方向性を決定づけるものであり、
1問ずつ丁寧に答えてもらう価値がある。

**ユーザーの発言を言い換えて確認してから次に進む。** 研究者は自分の研究を語る時、
重要なニュアンスを省略したり、複数の意味に取れる言葉を使ったりする。
「つまり〜ということですか？」と言い換えることで、エージェントの理解がずれている
場合に早期に修正できる。後のステージでのやり直しを防ぐための投資である。

**候補を先に提示してから選ばせる。** 「take-home messageを1文で書いてください」
と言われても、多くの研究者はその場で答えられない。しかし候補を見れば
「これに近いが〜が違う」と言える。白紙から書かせるのではなく、
エージェントが素材を用意してユーザーが彫刻する、という役割分担が効果的。

**`/literature-survey`の起動前に必ず承認を得る。** 文献調査は5〜30分かかる重い処理であり、
ユーザーが今すぐそれを必要としていない可能性もある。承認なしに起動すると、
ユーザーが意図しないタイミングでトークンと時間を消費することになる。

**ステージ完了時に宣言する。** 「A1が完了しました」と明示的に宣言することで、
ユーザーが今どのステージにいるかを把握しやすくなる。このスキルは複数のステージが
連続するため、進捗の可視化がユーザーの安心感につながる。

**モードAのContribution statementは仮定義であることをドキュメントに明記する。**
実験結果が出ていない段階で書いたcontribution statementは、実験後に必ず見直す必要がある。
忘れずに更新するためのリマインダーをファイルに残しておくことが重要。

**`research_framing_output.md`に`literature-survey-report`のパスを記録する。**
Research FramingとPhase Bが別セッションで実行される場合、文献調査レポートへの参照がなければ
Phase BのエージェントがPaper Catalogueを見つけられない。引き継ぎ情報として明示的に
記録しておくことで、セッションをまたいでも文脈が維持される。
