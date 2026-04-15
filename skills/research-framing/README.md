# RA-L論文執筆スキル

Claude Codeを用いてIEEE RA-Lに投稿する論文を執筆するためのスキル群。
4フェーズ・17アイテムのワークフロー（`ra-l_workflow_macro.md`参照）に対応する。

## ディレクトリ構成

```
.claude/skills/
├── research-framing/
│   └── SKILL.md          # Research Framing: 研究・提案の方向づけ
└── literature-survey/
    └── SKILL.md          # 文献調査（research-framingから呼び出し、単独使用も可）
```

## スキル一覧

### `/research-framing` — Research Framing: 研究・提案の方向づけ

RA-L論文の土台となる3アイテムを対話形式で確立する。

| アイテム | 内容 |
|----------|------|
| A1: Take-home message | 研究の核心メッセージを1文に |
| A2: Contribution statement | 貢献を3〜5文で定義、先行研究との差分を明示 |
| A3: 研究ポジショニング | CARSモデル（Territory→Niche→Occupation）で Introduction骨格を構築 |

**2つの動作モード**:

- **モードB（テーマ確定済み）**: 実験が進行中のプロジェクト向け。A1の言語化から始め、文献調査でA3を補強する。
- **モードA（テーマ探索中）**: 新規プロジェクト向け。広域文献調査でギャップを発見し、A1へ収斂する。

**A3サブエージェントレビュー**: CARS統合骨格の生成後、ユーザーへの提示前にTaskツール経由で
サブエージェントを起動し、生成時の会話コンテキストを持たない独立したエージェントが
Territory→Nicheの導線・Niche→Occupationの対応・A1/A2との整合・RA-L査読者視点の
4基準で評価する。骨格とA1/A2はファイル（`.tmp/cars_review_input.md`）経由で渡し、
評価結果もファイル（`.tmp/cars_review_output.md`）経由で受け取る。
アクター・クリティック形式をA3に限定して適用し、文脈リセットで独立性を確保した設計。

**出力**: `research_framing_output.md`（Phase Bへの引き継ぎ情報を含む）

**依存スキル**: `/literature-survey`（A3構築のために内部から呼び出す）

---

### `/literature-survey` — 文献調査

指定トピックの先行研究を体系的に収集・分析し、構造化されたレポートを生成する。

**単独使用**: トピックを指定して起動すると、スコープをインタラクティブに確認してから調査を開始する。

**research-framingからの呼び出し**: research-framingスキルが会話コンテキストにスコープ情報（トピック・深度・seed要否・制約）を置いた上で起動する。スキルはコンテキストを読んでスコープ確認をスキップし、直接調査を開始する。

**出力**: `docs/SURVEYS/<topic_slug>.md`

出力レポートの構成:

| セクション | Research FramingのCARSへの対応 |
|------------|----------------------|
| Research Landscape Overview + Foundation | Move 1: Territory |
| Survey Findings → Gap | Move 2: Niche |
| Survey Findings → Seed（要求時のみ） | Move 3: Occupationの検証材料 |

**調査深度**:

| 深度 | 対象論文数 | 用途 |
|------|-----------|------|
| `focused` | 20〜40本 | モードB（テーマ確定済み、A3補強目的） |
| `broad` | 40〜60本 | モードA（テーマ探索中、隣接分野を含む） |

---

## 典型的な使用フロー

### パターン1: 実験が進行中の論文（モードB）

```
/research-framing
→ モードB選択
→ A1のヒアリング・確定
→ /literature-survey（focused、seed不要）が自動起動
→ A2・A3の構築
→ research_framing_output.md 生成
```

### パターン2: 新規テーマの探索（モードA）

```
/research-framing
→ モードA選択
→ 探索の起点ヒアリング
→ /literature-survey（broad、seed必要）が自動起動
→ Seedからテーマを絞り込み → A1確定
→ A2・A3の構築
→ research_framing_output.md 生成
```

### パターン3: 文献調査のみ実行

```
/literature-survey
→ スコープをインタラクティブに確認
→ 調査実行
→ docs/SURVEYS/<topic_slug>.md 生成
```

---

## 将来追加予定のスキル

| スキル名 | フェーズ | 内容 |
|----------|---------|------|
| `/phase-b` | Phase B | 技術アプローチの選定・実装・実験実行 |
| `/phase-c` | Phase C | ストーリーライン設計・セクション別ドラフト・推敲 |
| `/phase-d` | Phase D | クロスモデル査読・引用検証・投稿前チェックリスト |

---

## 関連ドキュメント

| ファイル | 内容 |
|---------|------|
| `ra-l_workflow_macro.md` | マクロフロー（4フェーズ・17アイテム・完了ゲート） |
| `discussion_summary_updated.md` | 先行システム調査まとめ（AutoResearchClaw、AI-Researcher等） |
| `flow_comparison.md` | AutoResearchClaw / AI-Researcherとの比較表 |
| `docs/SURVEYS/` | 文献調査レポートの保存先 |
| `research_framing_output.md` | Research Framing完了後の成果物 |
