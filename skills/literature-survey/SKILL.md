---
name: literature-survey
description: "Conduct an academic literature survey that maps a research field — produces a concept matrix, gap analysis, and curated hub-paper deep reads. Use this skill whenever the user asks for a literature review, survey, related work search, prior art investigation, field mapping, or wants to know what research exists on X. Also trigger when the user says things like papers about, survey the field of, what is the state of the art in, find relevant publications, prior work, related work, or any request to systematically gather and map academic references. The skill defers per-paper deep analysis to /paper-summary, invoking it only on selected hub papers."
---

# Literature Survey Skill

Purpose: produce a **landscape map** of a research area — a concept matrix
spanning all surveyed papers, a synthesis of the field's thesis / progress /
gap, and curated **hub-paper deep reads** generated via `/paper-summary`.
This is a scoping/mapping review (Webster & Watson 2002; Arksey & O'Malley),
not a systematic review of evidence.

## Output Layout

```
./literature/
├── surveys/
│   └── {survey_slug}.md                  ← この skill が生成するメインレポート
└── papers/
    └── {citekey}/
        ├── main.pdf                       ← ハブ論文の PDF（取得・配置）
        └── {paper-title-slug}.md          ← /paper-summary が生成する深読みノート
```

- **`{survey_slug}`**: Phase 1 で「core topic + RQ」から自動生成し、ユーザー確認の上で確定する slug（lowercase + ハイフン）
- **`{citekey}`** / **`{paper-title-slug}`**: `/paper-summary` の規約に準拠（`{LastName}-{VenueYear}-{ShortTitle}` / 完全 slugify）

## Language Rule

レポート全体は単一言語で記述する。言語はユーザーのトピック記述の言語で決定：

- 日本語入力 → レポート本文は日本語
- 英語入力 → レポート本文は英語

本 skill 固有の構造ラベル（`thesis / foundation / progress / gap / seed`）は
言語に関わらず英語のまま使用する。それ以外の日本語ライティング規約（英語のまま
残す範囲、一般語彙の日本語化、構文の英語直訳禁止など）は CLAUDE.md 経由で
読み込まれる `~/.claude/rules/japanese_style.md` に従う。

## Subagent Policy

並列検索や hub 深読みでサブエージェントを使う場合は **Sonnet tier**
（現在 `claude-sonnet-4-6`）。コスト・コンテキスト効率と注釈品質のバランス。

## Auto-execution Mode

通常 workflow は Phase 1 (Frame: depth / RQ / I/E criteria / 既知略語 / survey_slug)、
Phase 2 (Map Checkpoint)、Phase 3 (Hub Selection) でユーザー確認を取る。

**live user が応答できない環境**（自動 batch 実行、empirical evaluation、
無人 dispatch 等）では以下のフォールバックに従う：

| 確認項目 | フォールバック挙動 |
|---|---|
| Phase 1 — depth | ヒントなしなら `focused` デフォルト |
| Phase 1 — RQ | core topic から 2-4 個を auto-derive、Methodology → Frame に記録 |
| Phase 1 — I/E criteria | peer-reviewed + 主要 preprint / 対象領域内 / 英語 を auto-derive |
| Phase 1 — 既知略語 | 収集せず、初出展開ルールで対応（誤展開は許容） |
| Phase 1 — survey_slug | auto-suggest をそのまま採用、Methodology に記録 |
| Phase 2 — Map Checkpoint | 完成形 markdown を Methodology → Map に「(automated run: presented but not confirmed)」注記付きで inline 埋め込み |
| Phase 3 — Hub Selection | Hub 候補表を生成し同様の注記を残し、承認待ちせず deep read に進む |

判定: 呼び出し側が「自動実行」「empirical eval」「batch」「headless」を明示した場合、
または会話文脈にスコープブロック（research-framing 連携節参照）があり対話相手が
登場しない場合に有効化。曖昧な場合は対話的モードを優先する（誤って skip するより
確認を求める方が安全）。

## Workflow

5 フェーズ構成: **Frame → Map → Hubs → Synthesize → Verify & Output**

### Phase 1: Frame

調査の境界を確定する。

- **Core topic**: 具体的な研究課題・領域
- **Research Questions (RQs)**: 2–4 個。survey の目的を明確化する。例：
  - RQ1: What algorithmic approaches have been proposed for [problem]?
  - RQ2: Under what conditions are these approaches evaluated?
  - RQ3: What are the unresolved technical challenges?
- **Depth / Breadth**: 採録規模を決定
  - `focused` — 中核トピックのみ。**20–40 papers**
  - `broad` — 隣接領域も含める。**40–60 papers**
  指定なしなら確認する。

  **target 内のどこに着地すべきか**: snowballing が自然飽和した点
  （直近 1 hop で発見される新規 paper が大部分既に採録済み）で止めるのが原則。
  - 下限を割って飽和: OK（小さい field の正直な signal）。Methodology に明記
  - 上限を超えても飽和しない: I/E criteria を狭めて再 map（領域が広すぎ）
  - 中央値前後 (focused なら 25-30) が典型的な着地点
- **Inclusion / Exclusion criteria**: スコープ境界を明示
  - Inclusion 例: peer-reviewed + 主要 preprint、特定タスク領域
  - Exclusion 例: poster-only、英語以外、対象領域外

ユーザー要求が既に具体的なら、RQ と criteria を提示して確認だけ取る。

#### survey_slug の生成

Frame 完了時、core topic と RQ から `{survey_slug}` を自動生成し、ユーザーに確認する
（auto-execution mode 時は確認 skip — Auto-execution Mode 節参照）。

**slug 化規則（auto-suggest 生成時）:**

1. core topic から英語キーワードを抽出（日本語入力なら英訳）
2. lowercase 化、空白とコロン等の区切り文字をハイフン `-` に置換
3. stop word（`a`, `an`, `the`, `of`, `for`, `via`, `with`, `from`, `in`, `on`, `and`, `or`,
   `is`, `are`, `to`）を除外
4. 残った先頭 **3-5 語**を `-` 連結（5 語超なら核心 3-5 語に絞る）
5. 年号は core topic に元々含まれている場合のみ末尾に付与（例: "2026 update of X" → `...-2026`）。
   時事 survey 用に勝手に付けない

Alternatives は (i) 1 語短縮版、(ii) 別のキー語を主軸にした版、(iii) "-survey" suffix 付き
の 3 案を提示する。

```
core topic: "Multi-Robot Task Allocation under Uncertainty"
RQ1: algorithmic approaches?
RQ2: evaluation conditions?

Auto-suggest: multi-robot-task-allocation-uncertainty
Alternatives:
  - multi-robot-task-allocation         (1 語短縮)
  - uncertainty-aware-task-allocation   (別主軸)
  - multi-robot-task-allocation-survey  (suffix 付き)
  - <free input>
```

承認された slug でメインレポートを `./literature/surveys/{survey_slug}.md` に書く。

#### research-framing 連携

会話コンテキストに以下のスコープブロックがある場合、Phase 1 をスキップして Phase 2 へ。
RQ と I/E criteria はトピックと depth から導出し、確認は取らない。`目的` が
"Niche 特定" なら open challenges と frontier gaps を強調する RQ を組む。

```
文献調査のスコープ:
- トピック: [topic]
- 深度: focused / broad
- seed: 不要 / 必要
- 目的: [purpose]
```

ただし `survey_slug` の確認は省略しない（Frame スキップ時もユーザーに 1 回確認）。

### Phase 2: Map

論文を集めて軽量に分類する。**ここでは深読みしない** — 1 行 contribution と
3-5 個の concept tag だけ。深読みは Phase 3 でハブ論文のみ実施。

#### Search Strategy

3 つの時間層で検索：

- **Tier 1 — Recent (last 2-3 years)**: preprint・主要会議・ジャーナルを網羅的に
- **Tier 2 — Established (3-10 years)**: 高被引用・ベンチマーク・データセット原典
- **Tier 3 — Foundational (~2015 以前)**: 当該領域を定義した seminal works のみ

主要手法は **snowballing**（Wohlin 2014）：

1. WebSearch + Semantic Scholar / OpenAlex で **seed 5–10 本**を確定
2. 各 seed の前方・後方引用を **1–2 hop** 追跡
3. 並行して直接トピック検索（補完）と既存 survey 論文の発見
4. 必要なら著者追跡・venue 限定検索

`references/search_sources.md` を Phase 2 開始時に読み、ツール仕様
（Semantic Scholar MCP、OpenAlex script、`resolve_oa_url`）を把握。
ロボティクス系トピックなら `references/venues_robotics.md` も読む。

サブエージェントで並列化可（角度ごとに分担）。

#### Keyword Construction

RQ から構造化キーワードセットを導出：

1. 各 RQ から key concept を抽出（population, intervention, outcome）
2. 各 concept について synonyms, abbreviations, spelling variants をリスト
3. Boolean で結合

例: `("multi-robot" OR "multi-agent" OR "swarm") AND ("task allocation" OR "task assignment") AND ("cooperation" OR "coordination")`

#### Per-paper Extraction（軽量）

採録した各論文に対して、検索結果メタデータと abstract から以下を抽出：

- **title, authors, year, venue, citation count**
- **DOI / arXiv ID / URL**（少なくとも 1 つ。なければ除外）
- **1-line contribution**: abstract から 1 文で要約
- **concept tags**: 3-5 個。後の concept matrix の列見出し候補となる

**深い 4 フィールド注釈（thesis/core/diff/limit）はここでは付けない**。これは
ハブ論文に対してのみ Phase 3 で `/paper-summary` 経由で生成される。

#### DOI Resolution（インライン）

arXiv ID のみで採録した論文は、可能なら publisher DOI に解決する。
`scripts/resolve_dois.py` を使ってバッチ処理：

```bash
python3 scripts/resolve_dois.py --input papers.json --output resolved.json
```

DBLP → `resolve_oa_url` MCP → Crossref のカスケード。Phase 4 として独立工程化せず、
Map の終わりに 1 回流す。

#### Deduplication

- Primary: DOI / arXiv ID（URL prefix 除去後に比較）
- Fallback: タイトル正規化（lowercase, punctuation/whitespace 除去）後の比較
- Merge 時は最も richest なメタデータを残す

#### Map Checkpoint

Phase 3 に進む前に、Map 結果をユーザーに提示して承認を取る
（auto-execution mode 時は確認 skip — Auto-execution Mode 節参照）。

提示する完成形テンプレート（Map Result 表 + 確認事項表）は
`references/map_checkpoint_template.md` を読み、そのまま埋めて提示する。

回答待ちの間 Phase 3 には進まない。差し戻された場合は Map を更新して再提示。

### Phase 3: Hub Selection & Deep Read

Map された論文の中から **ハブ論文** を選び、それぞれに `/paper-summary` を
適用して深読みノートを生成する。これがレポートの synthesis 段階での主要素材になる。

#### Hub から除外する論文タイプ

まず Map から以下のタイプを除外する（深読みノートの粒度が合わないため）：

- **教科書 / monograph**: contribution が章ごとに分かれており 1 deep note に収まらない。
  特定の章が survey の中心テーマに直結する場合のみ、その章を別途 `/paper-summary` に
  かける（citekey は `{Author}-Book{Year}-{Chapter}` 等で区別）
- **Survey / review 論文**: それ自体が複数論文の集約であり、本 survey の参照対象
  として Map に置くのは有用だが、Hub にすると機能重複する。Foundational Works 扱い
  として Methodology または Map で言及するに留める
- **Platform / framework / dataset 論文**: 単一研究 contribution というより
  infrastructure。関連する応用論文（その platform を使った具体研究）を Hub にする
  方が deep read の情報密度が高い

これらを例外的に Hub に入れる場合は、"Why hub" 列でその理由を明示する。

#### Hub Selection 基準

除外後の候補から **B + C のユニオン**で選定し、**上限 5–10 本**に絞る：

- **B. カテゴリ橋渡し性 + 影響力**: 以下の両方を満たす：
  - **論文単体が 2 つ以上の concept cluster** に属する技術要素を組み合わせている
    （単に著者が複数 cluster で活動しているだけでは bridging に当たらない）
  - **外部引用数が survey 全体（cluster 横断）の上位 1/3** に入る。発表 2 年以内の
    recent paper は citation velocity（年あたり引用数）で全体の上位 1/3 を代替判定
  - **citation 数が取得できない環境**（Semantic Scholar MCP / OpenAlex script
    不通）では `references/hub_selection_proxy.md` の 3 proxy 軸（venue tier /
    WebSearch hit / 本 survey 内被引用頻度）で代替判定する
- **C. Synthesis 主役性**: thesis / gap セクションで論じる中心となる論文
  （Phase 4 の synthesis 想定をプレビューして判定）

引用数だけ（criterion A）は survey 規模が小さい場合に信号が弱いため、
B + C を主軸とする。

選定したハブ論文を以下のように提示してユーザー承認を取る：

```
## Hub Papers (N selected for deep read)

| # | Title | Year | Venue | Why hub | Citekey |
|---|---|---|---|---|---|
| 1 | ... | 2024 | NeurIPS | B: bridges cluster A (X) + cluster B (Y), top-tertile cite (123/yr velocity) | Author-NeurIPS2024-... |
| 2 | ... | 2023 | RSS    | C: thesis 軸の主役（Z 制約と W 制約の両立を最初に示した） | Author-RSS2023-... |
| ... | ... | ... | ... | ... | ... |

各ハブに対して /paper-summary を実行します。続行しますか？
追加・削除があれば教えてください。
```

**Why hub の記述ルール**: 1-2 文で、B / C / B+C のいずれに該当するかを冒頭で明示し、
具体的な根拠を続ける：

- **B 該当**: 「B: bridges cluster X + cluster Y, top-tertile cite (具体数値 or velocity)」
- **C 該当**: 「C: <thesis/foundation/progress/gap> 軸の主役（具体的な役割を 1 文で）」
- **B + C 両方**: 「B+C: <両方の根拠を 1 文ずつ>」

vague な表現（"important", "influential", "key paper"）は使わず、必ず cluster 名 / 軸名 /
具体的な数値・役割を書く。

#### Hub PDF 取得

承認されたハブ論文ごとに：

1. PDF を取得：
   - `openAccessPdf`（Semantic Scholar 結果）→ ダウンロード
   - 不在なら `resolve_oa_url` で OA URL を取得 → ダウンロード
   - 不在なら `fetch_with_auth`（paywall）でユーザー cookie 経由取得
2. `./literature/papers/{citekey}/main.pdf` として配置
   - citekey は `/paper-summary` 規約 (`{LastName}-{VenueYear}-{ShortTitle}`) で生成
   - ShortTitle のエッジケースは `/paper-summary` 内のプロンプトに委ねる

PDF が取得できないハブ論文がある場合：
- 別のハブ候補に差し替えるか、深読み無しのまま留め置く（Paper Catalogue 内では
  `[deep read unavailable: PDF inaccessible]` と注記）かをユーザーに確認

#### Hub Deep Read

各ハブ論文について `/paper-summary` を呼び出す。**呼び出しモードはコンテキストで使い分け**：

- **対話的 / 通常実行モード**: subagent dispatch で `/paper-summary` を起動
  ```
  /paper-summary literature/papers/{citekey}/
  ```
  サブエージェントで並列化可（同時 3-5 本まで、コンテキスト消費に注意）

- **自動実行 / batch / context budget 制約モード**: `/paper-summary` の SKILL.md と
  references/template.md を inline で読み込み、template 厳守でノートを直接 Write する。
  recursive subagent dispatch によるトークン乗算を回避。Methodology に「inline mode」
  と注記

両モードとも出力先は同じ `./literature/papers/{citekey}/{paper-title-slug}.md`。
完了後、生成されたパスを記録する。これが Phase 4 の synthesis 入力となる。

**並列実行時の wikilink coordination**: 並列で `/paper-summary` を起動すると
ハブ間の相互 wikilink が欠落する。回避策（逐次実行 / 並列 + 補完 pass）の詳細は
`references/hub_parallel_coord.md` を参照。

### Phase 4: Synthesize

Map で得た concept matrix（全論文）と、Phase 3 で得たハブ深読みノート（5–10 本）を
入力として、survey-level の知見を導出する。これが survey の主要な知的貢献。

`references/synthesis_guide.md` を読んで、各セクションの記述ガイドラインに従う。
4 つの軸を導出：

1. **thesis** — ハブ深読みノート + 全論文の 1-line contribution から、
   field の根本的な未解決問題を articulate
2. **foundation** — ハブ深読みノートから、field が依拠する技術的 building blocks を抽出
3. **progress** — ハブ深読みノートを時系列に並べ、解決された問題の trajectory を描く
4. **gap** — ハブ深読みノートの limitations + concept matrix の空欄 / 疎な行 / 欠落セルから、
   構造的に未解決な問題を identify

加えて、Map メタデータから cross-cutting analysis を生成（追加検索不要）：

5. **Quantitative trends**: publication count by year / 主要 venue / sim/real 内訳
6. **Concept matrix**: 全論文 × 4-6 concepts のテーブル。本 survey の主要 artifact

#### Seed (conditional)

ユーザーが研究提案を要求した場合のみ、`references/seed_format.md` を読んで
Seed セクションを追加。「reading list が欲しい」だけなら省略。

### Phase 5: Verify & Output

#### Verify

`reference-verify` skill を起動して採録論文を一括検証：

- DOI / URL の存在確認（hallucination check）
- 検証不可な論文は除外、その数を Methodology に記録

**skip の許可**: Auto-execution mode かつ呼び出し側が「reference-verify は形式的に通過」
と明示した場合のみ skip 可。Methodology → Verify に「reference-verify skipped per
caller instruction (lightweight run)」と明記する。通常実行では skip しない。

#### Output

メインレポートを `./literature/surveys/{survey_slug}.md` に生成。
出力構造は `references/report_template.md` を参照。

セクション順序（出力上限を避けるため分割生成）：

1. Metadata + Research Landscape Overview + Survey Findings
   (Thesis / Foundation / Progress / Gap, 条件付きで Seed)
2. Concept Matrix + Quantitative Trends + Hub Papers + Paper Catalogue
3. Survey Methodology（Search summary / Hub selection rationale /
   Verification result の 1 ブロック）

ハブ論文は Paper Catalogue で 1 行 + Obsidian wikilink で深読みノートに飛ばす：

```
[[papers/{citekey}/{paper-title-slug}|{Author+ Year}]] — 1-line contribution
```

非ハブ論文は concept matrix と Paper Catalogue の 1 行 entry のみ。

引用規約は `.claude/rules/references.md` に従う（ファイルが存在しない環境では参照を skip）。

#### Post-output Bookkeeping

メインレポート書き出し後の永続化:

1. **`literature/surveys/README.md` の更新**: 新規 survey を一覧テーブルに追記
   - ファイルが存在しない場合は新規作成（一覧テーブルのヘッダ + 1 行 entry）
   - cwd が scratch directory（`/tmp/...` 等）で永続化が無意味な場合は skip し、
     Methodology に「README/LOGS update skipped (scratch environment)」と記録
2. **執行ログ**: `docs/LOGS/literature-survey.md` に追記（検索プロセス、出力パス、
   プロジェクトへの含意）
   - `docs/` 構造が存在しない環境では skip。Methodology に同様に記録

#### Final Quality Check

レポート完了前に `references/quality_checklist.md` の各項目を確認する。
未充足項目があれば修正してから完了とする。

## Abbreviation Convention

レポート全体に以下を適用：

- **初出**: `Discrete Elastic Rods (DER)`, `Bayesian Optimization (BO)` のように完全名 + 略語
- **2 回目以降**: 略語のみ
- **ユーザー既知略語** (3DGS, FEM, MPM 等): 初出から略語のみ。Phase 1 で確認
- **末尾に Abbreviation Glossary**: 略語 / 完全名 / 初出セクション の 3 列テーブル
