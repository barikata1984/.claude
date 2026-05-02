# スキル開発引き継ぎ文書

## このドキュメントの目的

Claude Codeのローカルインスタンスがゼロコンテキストから作業を引き継ぐための文書。
経緯・設計意図・残課題・即座に着手できるタスクを記述する。

---

## 経緯

### 背景

Atsushi（トロント大学博士課程、OMRON在籍中）が、IEEE RA-L投稿論文を
Claude Codeを使って執筆するためのスキル群を設計・実装している。

直前のセッション（Claude.ai上）では以下の先行調査を実施済み。

- エージェントによる論文執筆自律化の先行研究（AI Scientist v1/v2、Agent Laboratory等）
- 論文化されていないツール群（ARIS、AutoResearchClaw、AI-Researcher等）の調査
- 上記との比較に基づく、5層17アイテムのRA-L論文執筆ワークフロー設計
- 4フェーズ構成（Phase A〜D）のマクロフロー定義

詳細は `docs/discussion_summary_updated.md`、`docs/ra-l_workflow_macro.md`、
`docs/flow_comparison.md` を参照。

### このセッションで行ったこと

4フェーズのうちPhase A（研究の方向づけ）に相当するスキルを設計・実装した。
実装の過程で以下の設計判断を行った。

1. **文献調査の並行実施**: 当初はPhase Aスキル内に文献調査サブルーティンを埋め込む設計だったが、
   既存の`/literature-survey`スキルが高品質であったため、委譲する設計に変更。

2. **モードA/B分岐**: テーマ確定済み（実験進行中）のモードBと、
   テーマ探索中のモードAに分岐する設計。Atsushiが両方のプロジェクトを持つため。

3. **A3サブエージェントレビュー**: CARS骨格生成後にサブエージェントで独立レビューを実施。
   `context: fork`フロントマターにバグがあるため、Taskツール経由で実装。
   ファイル（`.tmp/cars_review_input.md`→`.tmp/cars_review_output.md`）経由でデータを渡す。

4. **レビュー結果の3パス分岐**:
   - パスX: 全OK → そのまま提示
   - パスY: 文章表現・論理構造の問題 → 修正案提示→ユーザー承認→再レビュー（ループはユーザーが終了）
   - パスZ: A1/A2との不整合 → エージェントは修正しない、ユーザーが判断

5. **スキル名**: `phase-a`から`research-framing`に改名。
   Take-home message・Contribution statements・CARSの3成果物は論文以外（ビジネスピッチ等）にも汎用的に使えるため。
   デフォルトは論文モード（RA-L）。他文脈への対応は本文の汎用化で対処（未実施）。

---

## スキルの設計意図

### `research-framing`スキル

**何をするか**: 新しいことを始める際の「フレーミング」を構造化する。
具体的には以下の3成果物を対話形式で生成する。

| 成果物 | 内容 | RA-L論文での対応 |
|--------|------|-----------------|
| Take-home message | 研究・提案の核心を1文で | Abstract冒頭 |
| Contribution statements | 貢献を3〜5文で | Introduction末尾 |
| CARS骨格 | Territory→Niche→Occupation | Introduction第1〜2段落 |

**なぜこの構造か**:
- A1（Take-home message）は研究者の頭の中にある答えを「引き出す」作業であり、
  エージェントが生成するのではなくユーザーが彫刻する設計。
- A3（CARS）は学術的論理構造であり、エージェントが評価基準を内部化できるため、
  サブエージェントによる独立レビューが有効。
- A1/A2は人間が確定するため、それとの不整合（パスZ）はエージェントが解決しない。

**他フェーズとの関係**:

```
research-framing（このスキル）
    ↓ research_framing_output.md を生成
Phase B: 技術的実現（未実装）
    ↓
Phase C: 論文化（未実装）
    ↓
Phase D: 品質保証と投稿（未実装）
```

`research_framing_output.md`の「Phase Bへの引き継ぎ情報」セクションが
Phase Bスキルへの入力仕様を兼ねる。

### `literature-survey`スキル

Atsushiが事前に設計・実装済みのスキル。このセッションで以下の変更を加えた。

- **Phase 1にコンテキスト参照ロジック追加**: `research-framing`から呼ばれた場合、
  会話コンテキストにスコープ情報が置かれていればインタラクティブ確認をスキップ。
  スタンドアロン稼働時は従来通り。
- **`references/venues_robotics.md`追加**: ロボティクス系トピック検出時に
  自動読み込みされるベニューリストと検索戦略。

---

## ファイル構成

```
.claude/skills/
├── README.md                              ← スキルディレクトリ概要
├── research-framing/
│   └── SKILL.md                           ← メインスキル（このセッションで作成）
└── literature-survey/
    ├── SKILL.md                           ← 既存スキル（このセッションで一部変更）
    ├── README.md                          ← スキルディレクトリ向け仕様書（新規作成）
    └── references/
        └── venues_robotics.md             ← ロボティクスベニューリスト（新規作成）
```

**`literature-survey`スキルが参照する既存ファイル（要確認）**:

```
references/report_template.md              ← レポート構造テンプレート（必須）
references/seed_format.md                  ← Seedセクション構造（seed使用時必須）
.claude/rules/references.md               ← 引用規則・BibTeX規則（必須）
scripts/search_semantic_scholar.py         ← Semantic Scholar APIスクリプト（必須）
scripts/search_openalex.py                 ← OpenAlex APIスクリプト（必須）
```

これらがリポジトリに存在するか確認し、なければ`literature-survey`スキルは
一部の機能が動作しない。

---

## 残課題

### 短期（次のセッションで着手すべき）

**1. 配置・動作確認（最優先）**

成果物をリポジトリの正しいパスに配置し、Claude Codeで実際に起動できるか確認する。

```bash
# 確認コマンド
/skills          # research-framing と literature-survey が表示されるか
/research-framing  # スキルが起動するか、モード選択が機能するか
```

モードBのフローを最低1回通しで実行し、以下を確認する。
- A1のヒアリング→候補提示→確定のループが意図通り動くか
- `literature-survey`が会話コンテキストを読んでスコープ確認をスキップするか
- A3サブエージェントレビューが`.tmp/`ファイル経由で正しく動作するか
- `research_framing_output.md`が正しい形式で生成されるか

**2. スキルクリエイターによるeval（配置確認後）**

`/skill-creator`を使って`research-framing`のevalを実施する。
テストケースの最低限のセット:

```
# モードB（テーマ確定済み）
「ACTを使った物体操作の実験が進んでいるが、論文のtake-home messageがまだ言語化できていない」

# モードA（テーマ探索中）
「慣性特性を活用したロボット操作で新しいテーマを探したい。UR5eとMuJoCoが使える」

# 論文以外の文脈（汎用性の確認）
「新しいプロダクトをVCに説明するためのピッチの骨格を作りたい」
```

**3. `literature-survey`の不足3への対処**

`references/seed_format.md`の内容を確認し、実験環境の制約が
seed生成の実現可能性評価に反映されているかを確認する。
不足があれば`seed_format.md`を更新する。

### 中期（Phase Bスキル設計前に着手すべき）

**4. `research-framing`本文の汎用化**

現在の本文には「RA-L」「ロボティクス」「論文」の文脈が埋め込まれている。
ビジネスピッチ等の他文脈での実行経験が蓄積したら、
ユーザーが文脈を指定した場合に質問・出力フォーマットが適応するよう本文を更新する。

**5. `literature-survey`の不足2への対処（部分対処済み）**

`venues_robotics.md`を追加済みだが、検索スクリプト（`search_semantic_scholar.py`等）に
ベニューフィルタを渡すオプションが実装されているか確認する。
なければスクリプトを更新する。

### 長期（Phase C・D実装後）

**6. Phase B〜Dスキルの設計・実装**

`ra-l_workflow_macro.md`に定義された4フェーズのうち、Phase Bが次のターゲット。
`research_framing_output.md`の「Phase Bへの引き継ぎ情報」セクションを入力仕様として使う。

| フェーズ | 主なスキル | 状態 |
|---------|-----------|------|
| Phase A | `research-framing` | ✅ 実装済み（eval未実施） |
| Phase B | `technical-approach`（仮称） | ❌ 未着手 |
| Phase C | `paper-draft`（仮称） | ❌ 未着手 |
| Phase D | `paper-review`（仮称） | ❌ 未着手 |

**7. `research-framing`のevalセット拡張**

スキルクリエイターのワークフローに従い、テストケースを20件以上に拡張し、
description optimizationループを回す。

---

## ローカルClaude Codeでの即時着手手順

### ステップ1: ファイルの配置

```bash
# このハンズオフ文書と同じディレクトリにいる前提
# research-framing スキル
mkdir -p .claude/skills/research-framing
cp research-framing/SKILL.md .claude/skills/research-framing/SKILL.md

# literature-survey スキル（変更分のみ上書き）
cp literature-survey/SKILL.md .claude/skills/literature-survey/SKILL.md
cp literature-survey/README.md .claude/skills/literature-survey/README.md
mkdir -p .claude/skills/literature-survey/references
cp literature-survey/references/venues_robotics.md \
   .claude/skills/literature-survey/references/venues_robotics.md

# スキルディレクトリのREADME
cp README.md .claude/skills/README.md
```

### ステップ2: 既存ファイルの存在確認

```bash
# literature-survey スキルが必要とするファイルを確認
for f in \
  ".claude/skills/literature-survey/references/report_template.md" \
  ".claude/skills/literature-survey/references/seed_format.md" \
  ".claude/rules/references.md" \
  ".claude/skills/literature-survey/scripts/search_semantic_scholar.py" \
  ".claude/skills/literature-survey/scripts/search_openalex.py"; do
  [ -f "$f" ] && echo "OK: $f" || echo "MISSING: $f"
done
```

### ステップ3: 動作確認

Claude Codeを起動して以下を順番に実行する。

```
/skills
```
→ `research-framing` と `literature-survey` が一覧に表示されることを確認。

```
/research-framing
```
→ 「研究テーマや技術的アプローチはすでに固まっていますか？」と問われることを確認。

モードBを選択し、Atsushiの現在の研究（ACTを使った物体操作、慣性特性の活用）で
フローを最後まで通す。

### ステップ4: 問題があった場合の確認ポイント

| 症状 | 確認箇所 |
|------|---------|
| スキルが一覧に出ない | ファイルパスとSKILL.mdのnameフィールドを確認 |
| モード分岐が機能しない | SKILL.mdのステップ0の記述を確認 |
| literature-surveyが呼ばれない | 会話上のスコープ情報の書式を確認（B-2節） |
| サブエージェントレビューが動かない | `.tmp/`ディレクトリへの書き込み権限を確認 |
| research_framing_output.mdが生成されない | 「Phase A 完了」セクションの手順を確認 |

---

## 参照ドキュメント

| ファイル | 内容 |
|---------|------|
| `docs/discussion_summary_updated.md` | 先行システム調査まとめ |
| `docs/ra-l_workflow_macro.md` | マクロフロー（4フェーズ・17アイテム） |
| `docs/flow_comparison.md` | AutoResearchClaw / AI-Researcherとの比較 |
| `.claude/skills/README.md` | スキル群の概要 |
| `.claude/skills/research-framing/SKILL.md` | メインスキル本体 |
| `.claude/skills/literature-survey/README.md` | 文献調査スキルの仕様書 |
