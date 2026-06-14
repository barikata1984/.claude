---
name: research-theme-proposal
description: "Use this skill — not research-proposal, not inline chat — when the user needs to FIND a research topic, not work on one they've already chosen. This is the topic-discovery skill: the user has a domain or interest area but no committed research question yet. Trigger on any of these: \"what should I work on next\", \"propose/suggest/brainstorm N research themes or directions\", \"research ideation\", 次の研究テーマを探す, テーマが決まらない, テーマ探し, 研究テーマを提案して, 新規研究テーマ, PhD/thesis topic brainstorming, gap-driven direction finding. This runs multi-phase vetting (ideation → novelty-checking → red-teaming) that inline chat cannot replicate. Do NOT trigger for: users who already have a specific topic and want execution help, literature surveys on a known topic, paper summaries, results analysis, or writing up a proposal for a decided theme."
---

# Research Theme Proposal (Orchestrator)

ロボット学習分野の新規研究テーマ提案を生成するオーケストレータ skill.
既存 skill 群(`literature-survey` / `paper-summary` / `reference-verify` /
`novelty-check`)を部品として駆動する.

設計原則(根拠は README 参照):

1. **LLM は novelty に強く feasibility に弱い** — feasibility は構造で強制する
   (Readiness Assessment × `research-context.md`, kill criterion 付きミニ実験計画)
2. **LLM の自己評価は信用しない** — 検索による反証(novelty-check)と
   別エージェントによる red-team を評価の代わりに置く
3. **発散は自由生成しない** — 生成メカニズム別の枠で多様性を構造的に強制する
4. **最終判定は人間** — 本 skill の出力は"de-risk 実験の入口まで整えた候補"であり,
   実行可否の判断は human checkpoint に委ねる

## Output Layout

```
./output/proposals/
├── INDEX.md                      ← 全候補の一覧と状態
├── P{N}-{slug}.md                ← 提案書（references/proposal_template.md 厳守）
└── novelty/
    └── P{N}-{slug}.md            ← novelty-check の差分分析ログ
./literature/                     ← literature-survey の規約に従う
```

## Language Rule

`literature-survey` と同一. 日本語入力なら本文は日本語, 構造ラベル
(gap / kill criterion / mechanism 等)は英語のまま.

## 必須入力: research-context.md

Phase 0 で project root の `research-context.md` を読む. **存在しない, または
placeholder(`<記入>`)が残っている場合は処理を中断し, 記入を求める. **
feasibility 評価はこのファイルの関数であり, 無しで生成した提案は評価不能なため.

## 実行モード

| モード | 条件 | 挙動 |
|---|---|---|
| serial | デフォルト / チーム無効 | 全フェーズを単一セッションで逐次実行. 発散はメカニズムごとに独立パスで実施 |
| team | エージェントチーム有効かつユーザーが許可 | Phase 3 を ideator で並列化, Phase 4 の novelty / red-team も並列実行. Workflow ツールがあればスクリプトで, 無ければエージェントチームで実施 (下記) |
| headless | `/goal` 起動 or 呼び出し側が batch を明示 | literature-survey を auto-execution mode で駆動. human checkpoint は"未承認"注記付きで出力に埋め込み, 停止しない |

team モードの推奨構成: ideator ×3(mechanism 別, `.claude/agents/ideator.md`)+
red-teamer ×1–2(`.claude/agents/red-teamer.md`). **リーダーは生成・攻撃を自分で
やらない**(採点と統合に徹する). メンバーは Sonnet tier.

**オーケストレーション手段**: Workflow ツールが利用可能な環境では, Phase 3-4 の
fan-out(ideation 並列 → novelty 並列 → red-team)を **Workflow スクリプトで
実行する**(本指示が Workflow 使用のオプトインに当たる). 理由: フェーズ間の
依存関係が固定的なパイプラインであり, スクリプト化により手動のチーム管理
(spawn / タスク依存設定 / shutdown / クリーンアップ)を排除できる.

- `agent()` の `agentType` に `ideator` / `novelty-checker` / `red-teamer` を指定し,
  `schema` で verdict 等の構造化出力を強制する
- novelty 層 → red-team 層の絞り込み(duplicate 即落選, incremental 差し戻し)は
  スクリプト内のフィルタで実装する(リーダー判断は不要な機械的規則のため)
- rubric 採点と統合はスクリプトの返り値を受けてリーダーが行う(従来どおり)
- Workflow ツールが無い環境ではエージェントチーム(TeamCreate)に, それも無ければ
  serial にフォールバック

## Workflow

6 フェーズ: **Context → Survey → Gap → Ideate → Screen → Writeup**

### Phase 0: Context

1. `research-context.md` を読み, placeholder 残存をチェック(残存なら中断)
2. ラボの capability summary(機材 / スキル / 計算資源 / 期間 / 戦略的関心)を
   3-5 行に要約し, 以降の全フェーズの判断基準として保持する

### Phase 1: Survey

既存 survey の再利用を最初に確認: `./literature/surveys/` に対象トピックの
survey が既にあれば再利用してよいかユーザーに確認(headless 時は鮮度 6 ヶ月以内
なら自動再利用, Methodology に注記).

新規実行時は `literature-survey` skill を以下のスコープブロックで起動する:

```
文献調査のスコープ:
- トピック: [user 指定 topic。未指定なら research-context.md の戦略的関心から導出]
- 深度: focused
- seed: 不要        ← seed 生成は本 skill の Phase 3 が担当するため必ず「不要」
- 目的: Niche 特定
```

headless 時は literature-survey の Auto-execution Mode 規約に従わせる.

### Phase 2: Gap

literature-survey の出力(`./literature/surveys/{survey_slug}.md`)から
以下を抽出して **gap inventory** を作る:

1. Survey Findings → Gap セクションの構造的ギャップ
2. Concept Matrix の空欄セル・疎な行
3. ハブ深読みノートの"議論と課題"から横断的に繰り返される limitation

各 gap entry に必須注記: **why-not-yet**(なぜ今まで埋まっていないか)と
**enabler candidates**(直近 24 ヶ月で何が変わり, 今なら埋まり得るか.
VLA, テレオペデータ収集系, 大規模実機データセット等の具体名で).
why-not-yet に答えられない gap は ideation 入力から除外する
("単に誰も思いつかなかった"は通常誤りで, 既存研究の見落としを疑う).

### Phase 3: Ideate

`references/ideation_mechanisms.md` を読む. gap inventory + research-context を
入力に, **4 メカニズム(enabler-driven / cross-domain transfer /
benchmark-definition / assumption-busting)それぞれで 2 候補, 計 8 候補**を生成.

生成開始前にリーダーが **gap 重点割り当て**を行う
(ideation_mechanisms.md の"Gap 重点割り当て"節参照. 強い gap への候補殺到と
novelty 共食いを防ぐ. 割り当て表は会話出力に明示する).

- team モード: mechanism ごとに ideator メンバーを生成. spawn prompt には
  gap inventory・research-context 要約・担当 mechanism・**重点 gap 割り当て**・
  出力先パスを**全て明示**する(メンバーはリーダーの会話履歴を継承しない).
  **他 ideator の出力を読むことを禁止**する(anchoring 防止)
- serial モード: mechanism ごとに独立したパスで生成し, 前パスの候補を
  コンテキストに保持したまま次を生成しない工夫として, 各パス冒頭で
  ideation_mechanisms.md の該当節のみを再読してその枠に集中する

各候補はこの段階では 1 ページ概要(title / mechanism / 対応 gap / 中核主張 /
ラボ適合の初期見立て)でよい.

### Phase 4: Screen

3 層で絞る. **順序固定**(安い検証を先に):

1. **Novelty 層**: 各候補に `novelty-check` skill を適用(subagent 並列可,
   Sonnet tier). verdict が `duplicate` の候補は即落選. `incremental` は
   差分を明確化して再提出 1 回まで.
   ログ命名: `output/proposals/novelty/{candidate_id}-{slug}.md`(候補 ID で生成.
   P 番号は Phase 5 で確定後にリネーム)
2. **Red-team 層**: 生存候補に red-teamer(`.claude/agents/red-teamer.md`,
   `references/redteam_protocol.md` 準拠)を適用. 攻撃記録は提案書の
   Red-team Record セクションに残す
3. **Rubric 層**: リーダーが `references/heilmeier_rubric.md` で採点.
   閾値未達は**却下理由を明記して**差し戻し

**ループ制御**: 候補ごとの改訂は最大 2 回. 2 回で閾値未達なら落選として
INDEX.md に理由とともに記録(無限ループ防止). 生存目標は 3 件.
8 候補全滅の場合のみ Phase 3 を 1 回だけ再実行(gap inventory を見直してから).
改訂上限は**自律ループの暴走防止**が目的であり, human checkpoint 発の改訂指示は
上限にカウントしない(iteration は据え置き, 対応を Red-team Record に CR 行として
記録する).

### Phase 5: Writeup

生存候補ごとに `references/proposal_template.md` を**厳守**して
`output/proposals/P{N}-{slug}.md` を生成. 要点:

- YAML frontmatter は機械チェック(`.claude/hooks/check_proposal.py`)の
  検証対象. 全フィールド必須
- **status のライフサイクル**: draft(作成中)→ screened(ゲート通過を主張,
  機械チェックの対象)→ accepted(テーマ確定後の作業フェーズ)/ rejected(落選).
  検証されるのは screened のみ. テーマを確定して実装・執筆フェーズに移ったら
  status を accepted に変えること(screened のまま放置すると, 以降そのリポジトリの
  全セッションで提案書が毎ターン検証され差し戻されるため)
- Approach Sketch は手法の完全仕様ではなく"議論の土台": 構成要素の動作原理
  (どうコスト化・指標化するか), 要素間の依存関係(循環依存の不在), 統合方針
  (offline/online 等のスコープ宣言), 対抗系統(survey クラスタ単位),
  未確定事項を全フィールド埋める
- ミニ実験計画の Baselines は novelty-check が実在確認したものに限る
- kill criterion は数値で書く("うまくいかなければ"は不可)
- 全引用に対して `reference-verify` を一括実行
- **Cold-read 質問生成レビュー(必須・採点前)**: 提案書ごとに, パイプラインの文脈を
  持たない subagent へ提案書 1 本のみを渡し"本文から答えられない技術的質問"上位
  3–5 件を生成させる(例: 欠落入力でフォワードパスはどう通るか / その量は
  どう測るのか / その動作はどう実行するのか / 論理連鎖は本文だけで追えるか /
  各文の主張は直前の文から論理的に従うか — "書いてあるが接続していない"説明の検出 /
  登場する量・データは何のために存在するか — 目的が本文で確定しない量の検出).
  全質問に本文修正または未確定事項への明記で応答してから rubric 採点に進み,
  対応は Red-team Record に CR 行として追記する

最後に INDEX.md を更新し, モードに応じて会話出力を切り替える:

- **headless モード**: **各提案書の全文と rubric 採点表を会話出力に表示する**
  (/goal の評価器はファイルを読めず, 会話に表示された内容のみで判定するため.
  これを省くと headless 実行が終了しない)
- **interactive モード (serial / team)**: 各提案の要約 (title / 中核主張 /
  rubric 合計点 / kill criterion) と提案書ファイルパスのみ表示する.
  全文表示は出力が過剰になるため行わない (ユーザーはファイルを直接読める)

### Human Checkpoint

出力の最後に必ず以下を明示する:

> これらは"最初の de-risking 実験を実施する価値があるか"を人間が判断する
> ための候補です. novelty / feasibility の最終判定は実行なしには困難である
> ことが実証されています(README 参照). 各提案の kill criterion と
> de-risking 実験を確認の上, 着手判断をしてください.

## /goal との接続

headless 起動テンプレートは `references/goal_templates.md` を参照.
条件文は"機械チェック通過 + rubric 採点表の表示 + ターン上限"で構成する.

## 環境依存とフォールバック

- Semantic Scholar MCP / `resolve_oa_url` / `fetch_with_auth` 不通時:
  literature-survey / novelty-check 内の規約どおり OpenAlex script →
  arXiv API → WebSearch に縮退. Methodology に縮退内容を記録
- `~/.claude/rules/*.md` が無い環境(sandbox 等): 参照を skip し,
  本 skill 同梱の規約のみで動作
- エージェントチーム無効: serial モードに自動フォールバック(チームを
  必須にしない)
