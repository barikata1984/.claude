---
name: paper-summary
description: "Generate a structured summary note for an academic paper by reading its PDF. Reads the PDF, extracts metadata, fills in a standardized template with Executive Summary and 7 structured questions (in Japanese), auto-links to related existing notes, and validates the citekey/folder naming convention. Use this skill whenever the user wants to summarize a paper, create a literature note, generate a reading note from a PDF, or asks to process a paper in the literature directory. Also trigger when the user points to a PDF and asks for a summary, or says things like 'read this paper', 'summarize this paper', 'create a note for this paper', 'process this PDF', or refers to a paper in the literature folder."
---

# Paper Summary Skill

論文PDFを読み込み、構造化されたサマリノートを生成するスキル。

## 入力

以下のいずれかをユーザーから受け取る：
- PDFファイルのパス（例: `literature/Author-Venue2026-Short_Title/main.pdf`）
- 論文フォルダのパス（例: `literature/Author-Venue2026-Short_Title/`）
- フォルダ名のみ（例: `Author-Venue2026-Short_Title`）

フォルダパスのみが与えられた場合、`main.pdf` がそのフォルダ内に存在することを確認する。

## 出力

論文フォルダ内に `{論文タイトル}.md` を生成する（例: `Foundation Model-Driven Grasping of Unknown Objects via Center of Gravity Estimation.md`）。論文タイトルはPDFから抽出した英語タイトルをそのまま使用する。既に同名ファイルが存在する場合は、上書きしてよいかユーザーに確認する。

出力の形式・セクション構成・記述ルールは、本スキルのベースディレクトリ内の `references/template.md`（絶対パス: `~/.claude/skills/paper-summary/references/template.md`）に定義されている。
ノート生成時は必ずこのテンプレートを読み込み、その形式に厳密に従うこと。

## ワークフロー

### Step 1: テンプレートの読み込み

`~/.claude/skills/paper-summary/references/template.md` を読み込み、出力形式・記述ルール・参照情報（Venue略称リスト、命名規則）を把握する。

### Step 2: 入力の検証とフォルダ名チェック

1. PDFファイルの存在を確認する
2. フォルダ名をテンプレート内の命名規則と照合する
3. 齟齬がある場合は**ノート生成の前に**ユーザーに報告する。例：
   - Venue略称にハイフンや月が含まれている
   - VenueとYearの順序が逆
   - LastNameのスペルが論文の著者名と異なる
   - ShortTitleがタイトルと対応していない

報告の形式：
```
フォルダ名の命名規則チェック:
  フォルダ名: Simoenov-2023CoRL-Shelving_Stacking_Hanging
  検出された齟齬:
    - VenueYear: "2023CoRL" → 推奨 "CoRL2023"（Venue略称が先）
    - LastName: "Simoenov" → 論文著者名は "Simeonov"（スペル相違）
  続行しますか？
```

### Step 3: PDFの読み込みとメタデータ抽出

PDFを読み込み、以下のメタデータを抽出する：
- 論文タイトル
- 著者リスト（姓, 名 の形式）
- 出版年
- Venue（会議名/ジャーナル名 → テンプレート内の略称リストで変換）
- DOI（存在する場合）
- BibTeX情報

### Step 4: 既存ノートの読み込み（自動リンク用）

`literature/` ディレクトリ内の既存ノート（各フォルダ内の `.md` ファイル。`main.pdf` 以外）をすべて読み込み、各ノートから以下を取得する：
- フォルダ名（= citekey）
- 論文タイトル（`# ` 見出し = ファイル名）
- Executive Summary
- 著者リスト

この情報は Step 5 で相互参照リンクを生成するために使用する。

### Step 5: サマリノートの生成

PDFの内容を熟読し、`~/.claude/skills/paper-summary/references/template.md` の形式に従ってサマリノートを生成する。
テンプレートに定義された全フィールド・全セクションを漏れなく出力すること。

### Step 6: 最終確認

生成完了後、以下をユーザーに報告する：
1. 生成したファイルのパス
2. 抽出したメタデータの概要（タイトル、著者数、Venue、タグ）
3. 生成した自動リンクの一覧（あれば）
4. Step 2 で検出した命名規則の齟齬（あれば、再掲）
