---
name: paper-summary
description: "Generate a structured summary note for an academic paper by reading its PDF. Reads the PDF, extracts metadata, fills in a standardized template with Executive Summary and 6 structured questions (in Japanese) covering problem, approach, novelty, training, validation, and limitations. Auto-links to related existing notes and validates the citekey/folder naming convention. Use this skill whenever the user wants to summarize a paper, create a literature note, generate a reading note from a PDF, or asks to process a paper in the literature directory. Also trigger when the user points to a PDF and asks for a summary, or says things like 'read this paper', 'summarize this paper', 'create a note for this paper', 'process this PDF', or refers to a paper in the literature folder."
---

# Paper Summary Skill

論文 PDF を読み込み、構造化された日本語サマリノートを生成するスキル。
`/literature-survey` のハブ論文深読みステップからも呼び出される。

## ディレクトリ規約

すべての論文は以下の構造で管理する：

```
./literature/papers/{citekey}/
├── main.pdf                              ← 論文 PDF（必ずこのファイル名）
└── {paper-title-slug}.md                 ← 本スキルが生成するサマリノート
```

- **citekey**: `{LastName}-{VenueYear}-{ShortTitle}` 形式（後述「citekey 規約」参照）
- **{paper-title-slug}**: 論文タイトルを完全 slugify したもの（lowercase、空白とコロン等を `-` に置換、英数字とハイフンのみ）
  - 例: `"Foundation Model-Driven Grasping of Unknown Objects via Center of Gravity Estimation"`
    → `foundation-model-driven-grasping-of-unknown-objects-via-center-of-gravity-estimation.md`

## 入力

以下のいずれかをユーザー（またはスキル呼び出し元）から受け取る：

- PDF ファイルのパス（例: `literature/papers/Nadeau-CoRL2024-Generating_Stable_Placements/main.pdf`）
- 論文フォルダのパス（例: `literature/papers/Nadeau-CoRL2024-Generating_Stable_Placements/`）
- citekey のみ（例: `Nadeau-CoRL2024-Generating_Stable_Placements`）

フォルダパスのみが与えられた場合、そのフォルダ内に `main.pdf` が存在することを確認する。

## ワークフロー

### Step 1: テンプレートの読み込み

`~/.claude/skills/paper-summary/references/template.md` を読み込み、出力形式・記述ルール・参照情報（Venue 略称リスト、citekey 命名規則）を把握する。

### Step 2: PDF の存在確認とメタデータ抽出

1. `main.pdf` の存在を確認
2. PDF を読み込み、以下のメタデータを抽出：
   - 論文タイトル（英語そのまま）
   - 著者リスト（姓, 名 の形式）
   - 出版年
   - Venue（会議名/ジャーナル名 → テンプレート内の略称リストで変換）
   - DOI（存在する場合）
   - BibTeX 情報

### Step 3: citekey の検証または生成

入力が citekey/フォルダパスで与えられた場合：**検証モード**。フォルダ名を「citekey 規約」と照合し、齟齬があれば**ノート生成の前に**ユーザーに報告する。

入力が PDF パスのみ（フォルダ未確定）の場合：**生成モード**。下記「citekey 規約」に従って自動候補を作り、ユーザー確認を取った上でフォルダを作成し PDF を配置する。

#### citekey 規約

形式: **`{LastName}-{VenueYear}-{ShortTitle}`**

- **LastName**: 第一著者の姓（PDF メタデータから抽出。スペル相違は要確認）
- **VenueYear**: Venue 略称 + 西暦 4 桁（月は含めない）。例: `CoRL2024`, `ICRA2026`, `arXiv2025`
- **ShortTitle**: タイトルから抽出した短縮句（下記「ShortTitle 自動生成ルール」参照）

例: `Nadeau-CoRL2024-Generating_Stable_Placements`

#### ShortTitle 自動生成ルール

**基本ルール（Better BibTeX `shorttitle` 規約に準拠）:**

1. タイトルにコロン `:` が含まれる場合、**コロン前**の部分のみを対象とする（コロン前が 2 語未満の場合はフォールバックして全体を対象）
2. 以下の stop word を除外する: `a`, `an`, `the`, `of`, `for`, `via`, `with`, `from`, `in`, `on`, `at`, `to`, `and`, `or`, `is`, `are`, `be`
3. 残った先頭 **3 語**を Title Case にしてアンダースコア連結

**例（自動で確定するケース）:**

| タイトル | ShortTitle |
|---|---|
| Generating Stable Placements via Bisection Search | `Generating_Stable_Placements` |
| A Survey of Reinforcement Learning for Robot Manipulation | `Survey_Reinforcement_Learning` |
| Shelving, Stacking, Hanging: Relational Pose Diffusion ... | `Shelving_Stacking_Hanging` |
| ImageNet Classification with Deep Convolutional Neural Networks | `ImageNet_Classification_Deep` |

#### ShortTitle がエッジケースに該当する場合 — ユーザー確認

以下のいずれかに該当する場合、自動候補に加えて代替案を提示し、ユーザーに選択を求める：

**Case A: ハイフン語が中間に来る**
```
Title: "Foundation Model-Driven Grasping of Unknown Objects ..."
Auto:        Foundation_Model-Driven_Grasping
Alternatives:
  - Foundation_Model_Grasping  (skip "Driven")
  - <free input>
```

**Case B: コロン前が 1 語のみ**
```
Title: "BERT: Pre-training of Deep Bidirectional Transformers ..."
Note: title before ":" has only 1 word ("BERT"), falling back to full title.
Auto:        BERT_Pre-training_Deep
Alternatives:
  - BERT  (use model name as the entire ShortTitle)
  - <free input>
```

**Case C: コロン前が 2 語（通称化している可能性）**
```
Title: "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion"
Auto:        Diffusion_Policy_Visuomotor  (3 words, padded from after colon)
Alternatives:
  - Diffusion_Policy  (2 words, common name of the model)
  - <free input>
```

確認を取った後、最終的な citekey を確定する。

### Step 4: 既存ノートの読み込み（自動リンク用）

`literature/papers/` 配下の既存サマリノート（各 `{citekey}/` フォルダ内の `.md` ファイル。`main.pdf` 以外）を全件スキャンし、以下を取得する：

- citekey（= フォルダ名）
- 論文タイトル（frontmatter `Title` フィールド）
- 出力ファイル名（`.md` のスラッグ）
- Executive Summary
- 著者リスト

この情報は Step 5 で相互参照リンクを生成するために使用する。

### Step 5: サマリノートの生成

PDF の内容を熟読し、`~/.claude/skills/paper-summary/references/template.md` の形式に従ってノートを生成する。出力先は：

```
./literature/papers/{citekey}/{paper-title-slug}.md
```

既に同名ファイルが存在する場合は、上書きしてよいかユーザーに確認する。

テンプレートに定義された全フィールド・全セクションを漏れなく出力すること。本文中で既存ノートに言及する場合は Obsidian wikilink を使用：

```
[[papers/{citekey}/{paper-title-slug}|[N]]]          ← 引用番号が分かる場合
[[papers/{citekey}/{paper-title-slug}|Author+ YYYY]] ← 引用番号が不明な場合
```

### Step 6: 原典照合検証

生成したサマリノートの正確性を, 原論文 PDF に戻って検証する。LLM による要約は
もっともらしいが原典と一致しない記述を生みやすい。このステップでそれを潰す。

#### 検証対象の抽出

Step 5 で生成したノートの以下のセクションから, **検証可能な事実主張**を抽出する:

- **対象セクション**: Executive Summary + Summary 内の 6 つの構造化質問
  （問い・課題 / アプローチと根幹要素 / 既存研究との新規性 / 訓練・最適化 /
  検証方法と結果 / 議論と課題）
- **対象外**: 「自身の研究との関連」「追加議論」（ユーザーの研究文脈に関する記述であり,
  原論文の事実主張ではない）, YAML フロントマター, BibTeX

抽出する主張の 4 カテゴリ:

- 具体的な手法名・アルゴリズム名とその説明
- 数値（精度, 成功率, 比較結果, データセット規模, パラメータ値, 参考文献の著者名・年など）
- 因果関係・優位性の主張（「X が Y より優れる」「X により Y が可能になった」等）
- 著者が述べた limitation（「議論と課題」セクションの記述。本文中の仮定で
  §7 等の議論に現れないものも検証対象に含める。照合結果で「著者が limitation として
  議論」vs「本文中の前提として記載のみ」を注記で区別すれば十分）

一般的な背景説明・ドメイン知識の記述は対象外。

#### 照合手順

各主張について PDF の該当箇所（セクション・段落）を特定し, 以下を確認:

1. **存在性**: 主張が原文に実際に存在するか（捏造でないか）
2. **数値正確性**: 数値が原文と一致するか
3. **文脈保持**: 原文では限定付き（条件付き・一部のケースで等）の主張を
   断定的に書いていないか
4. **意図の忠実性**: 著者の主張を正しく反映しているか

#### 修正ルール

- 原文に存在しない主張 → 削除
- 数値の誤り → 原文の値に修正
- 文脈の歪曲 → 限定句の追加・表現の修正
- 検証不能（PDF 内に該当箇所が見つからない）→ 主張を削除

#### `/literature-survey` からの呼び出し時

literature-survey Phase 3 から subagent で呼ばれた場合, 本ステップは
subagent 内で完結させる。literature-survey 側で別途クロス検証が走るため,
ここでは self-verification で十分。

### Step 7: 最終確認

生成完了後、以下をユーザーに報告する：

1. 生成したファイルのパス（`./literature/papers/{citekey}/{paper-title-slug}.md`）
2. 抽出したメタデータの概要（タイトル、著者数、Venue、Tags）
3. 生成した自動リンクの一覧（あれば）
4. Step 3 で検出した命名規則の齟齬または確認結果（あれば、再掲）
5. Step 6 で修正があった場合: 修正件数と概要（全件パスなら報告不要）
