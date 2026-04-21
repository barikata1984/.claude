---
paths:
  - "literature/**"
  - "docs/LOGS/**"
  - "docs/REPORTS/**"
---

# 参考文献引用規約

## MAIN.md の役割

`literature/references/main.md` はプロジェクト全体の文献データベースである。
どのスキル・どのドキュメントから論文に言及する場合でも、書誌情報は MAIN.md に一元管理する。

## Key の命名規則

`AuthorYear_keyword` 形式を使用する。

- `Author`: 第一著者の姓
- `Year`: 出版年 (4桁)
- `keyword`: 内容を端的に示す英小文字 (snake_case)

例: `Xu2024_inertia`, `Kumar2021_rma`

## MAIN.md のエントリ形式

```markdown
### Key

**Title**
Authors — Venue, Year
DOI: `10.xxxx/xxxxx` | [URL]

> 1-2 文の要約（このプロジェクトにとっての意義を含む）
```

DOI と URL は少なくとも一方を記載する。両方あれば両方記載する。

## BibTeX 自動生成

`literature/references/references.bib` は MAIN.md への Write/Edit 時にフックが自動生成する。
手動で .bib を編集してはならない。MAIN.md が唯一の編集対象である。

## 参考文献処理手順

論文に言及するすべてのスキルは以下の手順に従う。

1. **本文中の引用**: `[[Key]](references/main.md#Key)` 形式のクリッカブルリンクにする
2. **存在検証**: MAIN.md に新規追加する論文は、事前にハルシネーションチェック（後述）を通過しなければならない
3. **MAIN.md の更新**: 検証に通過したエントリのみ追加する
4. **出力ファイル末尾**: 参考文献セクション（`## 参考文献` or `#### 参考文献`）にキー + 1行要約を列挙する。引用がなければセクション自体を省略する

## ハルシネーションチェック

MAIN.md に論文を新規追加する際、その論文が実在することを検証する。
既に MAIN.md に存在するエントリは検証済みとみなし、再チェック不要。

### 検証方法

各論文について、以下のいずれかで実在を確認する:

- **DOI**: `https://doi.org/<DOI>` を WebFetch し、HTTP 200/302 で解決されることを確認
- **URL**: 論文の URL を WebFetch し、ページにタイトルまたは著者名が含まれることを確認

### 判定

- **PASS**: DOI/URL が確認できた → MAIN.md に追加してよい
- **FAIL**: DOI/URL が解決できない、またはタイトル不一致 → WebSearch で再検索する。
  再検索でも見つからない場合、その論文は引用しない

### スケールに応じた実施方法

- **少数 (1-5 件)**: インラインで検証する
- **大量 (6 件以上)**: サブエージェントを起動してバッチ検証する。
  サブエージェントは各論文について `PASS: [Title] — DOI/URL confirmed` または
  `FAIL: [Title] — reason` を報告する

## サーベイ Paper Catalogue での引用形式

literature-survey の Paper Catalogue では、分析的注釈 (thesis/core/diff/limit) を付与する。
書誌詳細は MAIN.md に集約し、Catalogue では以下の形式を使う:

```markdown
1. [[Key]](references/main.md#Key) — Authors, "Title" (Year)
   - **thesis**: 著者の中心的主張
   - **core**: 手法の中核要素
   - **diff**: 先行研究との対比
   - **limit**: 著者が認めた制約・未到達点
```

分析的注釈 (thesis/core/diff/limit) は MAIN.md には書かない。サーベイ固有の情報である。
