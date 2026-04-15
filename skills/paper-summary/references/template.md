# 論文サマリノート出力テンプレート

このファイルは paper-summary スキルが生成するノートの出力形式を定義する。
Zotero の Nunjucks 変数は含まない。各フィールドの値は PDF から抽出して埋める。

---

## 出力形式

```markdown
---
Authors:
  - LastName, FirstName
  # 全著者を記載
Year: YYYY
Venue: XXXX
Tags:
  - "tag1"
  - "tag2"
  # 論文の主要トピックから 3-6 個。小文字ハイフンつなぎ
PDF: "[[Citekey/main.pdf|📃]]"
Import Date: "YYYY-MM-DD"
Read Date: YYYY-MM-DD
Executive Summary: （## Executive Summary セクションと同一の内容）
Citekey: （フォルダ名をそのまま使用）
DOI: （存在する場合）
Relevance: （1-5。自身の研究との関連度）
Code Available: （URL or "no"）
Category: note
Template Version: v2.0
---
# 論文タイトル（英語のまま）

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

### 提案手法はその問い・課題にどのようにアプローチしたのか？

### そのアプローチの根幹をなす要素は何か？

### そのアプローチ・要素が特に参考とした既存研究と、それらと比した提案手法の新規性は何か？

### それらの要素を組み合わせて、どのようなフレームワークを構築し、どのように訓練・最適化したのか？

### どのように提案手法を検証したか？検証の指標はどのようなもので、どのような結果が得られたか？

### 検証結果に基づいた議論、明らかになった課題はあるか？

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
（BibTeX エントリ。citekey は lastnameYEARfirstword 形式）
```
</details>
```

---

## 記述ルール

### 言語
- 全セクションを日本語で記述
- 以下は英語のまま: 論文タイトル、著者名、手法名・アーキテクチャ名、数式、BibTeX キー

### ファイル名
出力ファイル名は論文タイトル（英語）をそのまま使用する（例: `Foundation Model-Driven Grasping of Unknown Objects via Center of Gravity Estimation.md`）。`summary.md` は使用しない。

### 自動リンク
Summary 本文中で既存ノートの論文に言及する場合、Obsidian wikiリンクを使用：
```
[[FolderName/論文タイトル|[N]]]          ← 引用番号が分かる場合
[[FolderName/論文タイトル|Author+ YYYY]] ← 引用番号が不明な場合
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
フォルダ名と Citekey は一致させること。
形式: {LastName}-{VenueYear}-{ShortTitle}
  - LastName: 第一著者の姓
  - VenueYear: Venue略称 + 西暦4桁（月は含めない）
  - ShortTitle: タイトルから識別に十分な3語程度を
               アンダースコアつなぎ、各語 Title Case
例: Nadeau-ICRA2026-Generating_Stable_Placements

Citekey はフォルダ名をそのまま使用する。
生成時にフォルダ名が上記形式から逸脱している場合は報告すること。
-->
