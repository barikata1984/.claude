# 論文サマリノート出力テンプレート

このファイルは paper-summary スキルが生成するノートの出力形式を定義する。
Zotero の Nunjucks 変数は含まない。各フィールドの値は PDF から抽出して埋める。

---

## 出力先パス

```
./literature/papers/{citekey}/{paper-title-slug}.md
```

- `{citekey}`: `{LastName}-{VenueYear}-{ShortTitle}` 形式（SKILL.md「citekey 規約」参照）
- `{paper-title-slug}`: 論文タイトルの完全 slugify（lowercase、空白とコロン等を `-` に、英数字とハイフンのみ）

例: `./literature/papers/Tanaka-ICRA2026-Foundation_Model_Grasping/foundation-model-driven-grasping-of-unknown-objects-via-center-of-gravity-estimation.md`

---

## 出力形式

```markdown
---
Title: （論文の正式タイトル、英語のまま）
Authors:
  - LastName, FirstName
  # 全著者を記載
Year: YYYY
Venue: XXXX
Tags:
  - "tag1"
  - "tag2"
  # 論文の主要トピックから 3-6 個。小文字ハイフンつなぎ
PDF: "[[papers/{citekey}/main.pdf|📃]]"
Import Date: "YYYY-MM-DD"
Read Date: YYYY-MM-DD
Executive Summary: （## Executive Summary セクションと同一の内容）
Citekey: （フォルダ名 = システム上の citekey をそのまま使用）
BibTeX Key: （BibTeX 慣習の lastnameYEARfirstword 形式。Citekey とは別物）
DOI: （存在する場合）
Relevance: （1-5。自身の研究との関連度）
Repository: <URL or "none">
Category: note
Template Version: v2.3
---

## Executive Summary
200字程度の日本語要約。内容の優先順位：
- 取り組んだ課題や問い（10-20%）
- 提案手法の根幹要素とその活用のされ方（60-80%）
- 確認された長所と短所（10-20%）
タイトルから読み取れる情報（手法名等）は省略可。
主語がなくても意味が通じるなら省略。

---
## Summary
論文を熟読・内容を熟考の上、簡潔かつ的確に以下の質問に答えよ。
重複した内容が複数の項目に記載されることなきよう注意すること。

### この論文が答えた問い、あるいは解決した課題は何か？

### 提案手法のアプローチと、その根幹をなす要素は何か？
1 段落で全体戦略を述べた後、必要不可欠な構成要素を bullet で列挙せよ。
要素は「これがなければ手法が成立しない」ものに限る
（差別化のための補助技法・対比は次の新規性セクションで扱う）。

### 特に参考とした既存研究と、それらと比した提案手法の新規性は何か？

### どのように訓練・最適化したのか？
以下の必須項目を漏れなく記述。理論的・解析的論文等で該当しない項目は
「N/A: <理由>」と明示すること（埋め草の創作は禁止）。
- **損失関数 / 最適化目的**: 数式または明確な日本語記述
- **データセット**: 名称、規模、スプリット

### どのように検証したか？指標と結果は？
検証プロトコル（ベースライン、メトリクス、評価シード/試行回数）と
得られた定量的結果を簡潔に記述。主要な表・数値を引用。

### 検証結果に基づいた議論、明らかになった課題はあるか？
著者が論文中で**明示的に**述べた議論・限界・future work のみを記述。
著者が限界に言及していない場合は「著者は限界に明示的には言及していない」
と書き、推測で補完しないこと。

各記述には可能な範囲で論文中のセクション名（または近接する引用語句）を
併記する：
- 例: 「(§5.2 Limitations より) センサーノイズへの頑健性は未検証」
- 例: 「(§6 Discussion 末尾) 大規模シーンへのスケーラビリティが
  今後の課題として挙げられている」

---
## 自身の研究との関連
本論文の知見・手法・成果のうち、自身の研究に活用・応用・発展可能な要素は何か？
また、自身の研究との差分や相補的な関係はどのようなものか？

---
## 追加議論
（空のまま出力。ユーザーが後から記述する領域）

---
## BibTex
<details>
<summary> Click to show/noshow the BibTex data </summary>
```bibtex
（BibTeX エントリ。BibTeX 内部 key は lastnameYEARfirstword 形式 = frontmatter `BibTeX Key`）
```
</details>
```

---

## 記述ルール

### 言語
- 全セクションを日本語で記述
- 以下は英語のまま: 論文タイトル、著者名、手法名・アーキテクチャ名、数式、BibTeX キー

### ファイル名（paper-title-slug）
論文タイトルを完全 slugify したものを使用：

1. lowercase に変換
2. 空白・コロン・カンマ・スラッシュ等の区切り文字を全て `-` に置換
3. 英数字とハイフン以外の文字（カンマ、ピリオド、引用符等）は削除
4. 連続するハイフンは 1 つにまとめる
5. 先頭・末尾のハイフンを除去

**例:**

| 原タイトル | slug |
|---|---|
| Generating Stable Placements via Bisection Search | `generating-stable-placements-via-bisection-search` |
| Foundation Model-Driven Grasping of Unknown Objects via Center of Gravity Estimation | `foundation-model-driven-grasping-of-unknown-objects-via-center-of-gravity-estimation` |
| Shelving, Stacking, Hanging: Relational Pose Diffusion for Multi-Modal Rearrangement | `shelving-stacking-hanging-relational-pose-diffusion-for-multi-modal-rearrangement` |
| BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | `bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding` |

### 自動リンク
Summary 本文中で既存ノートの論文に言及する場合、Obsidian wikilink を使用：

```
[[papers/{citekey}/{paper-title-slug}|[N]]]          ← 引用番号が分かる場合
[[papers/{citekey}/{paper-title-slug}|Author+ YYYY]] ← 引用番号が不明な場合
```

既存ノートに存在しない論文へのリンクは生成しない。

---

<!-- 以下はサマリ生成時の参照用。生成ノートには含めない。 -->
<!--
## Venue 略称リスト（参照用）

### ロボティクス会議
ICRA, IROS, RSS, CoRL, Humanoids, HRI, CASE

### ロボティクスジャーナル
TRO, RAL, IJRR, AR, JFR, RAS

### ML/AI 会議
NeurIPS, ICML, ICLR, AAAI, L4DC

### コンピュータビジョン会議
CVPR, ICCV, ECCV, 3DV

### その他
ISRR, WAFR, ISER, SII

### 上記以外
arXiv, 書籍チャプター等は自由記述

## Citekey / フォルダ名の命名規則（参照用）

形式: `{LastName}-{VenueYear}-{ShortTitle}`

- LastName: 第一著者の姓
- VenueYear: Venue 略称 + 西暦 4 桁（月は含めない）
- ShortTitle: SKILL.md「ShortTitle 自動生成ルール」に従う。
  原則は Better BibTeX shorttitle 規約（stop word 除外、コロン前打ち切り、
  先頭 3 語を Title Case + underscore 連結）。
  ハイフン語が中間に来る／コロン前が短い等のエッジケースは
  ユーザー確認プロンプトで決定。

例: `Nadeau-CoRL2024-Generating_Stable_Placements`

Citekey はフォルダ名と完全一致させること。
生成時にフォルダ名が上記形式から逸脱している場合は報告すること。

## システム citekey と BibTeX 内部 key の区別

- **システム citekey** (= フォルダ名 = frontmatter `Citekey`):
  `{LastName}-{VenueYear}-{ShortTitle}` — パス・wikilink・cross-reference の主 ID
- **BibTeX 内部 key** (BibTeX エントリ内 = frontmatter `BibTeX Key`):
  `lastnameYEARfirstword` — BibTeX/BibLaTeX 慣習に従う、論文引用用

両者は別物として併存させる。混同しないこと。
-->
