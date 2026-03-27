# literature-survey スキル

指定したトピックの先行研究を体系的に収集・分析し、構造化されたMarkdownレポートを生成する。
単独でも、`/research-framing`スキルからの呼び出しでも動作する。

## 起動方法

```
/literature-survey
```

引数は不要。起動後にスコープを確認してから調査を開始する。
ただし`/research-framing`から呼び出された場合は、会話コンテキストにスコープ情報が置かれているため、
確認をスキップして直接調査に進む（後述）。

## ワークフロー概要

| フェーズ | 内容 | ユーザー操作 |
|---------|------|-------------|
| Phase 1: スコープ定義 | トピック・深度・seed要否・制約を確認 | 対話（コンテキストがあればスキップ） |
| Phase 2: 検索 | 3つの時間的層で体系的に収集 | なし（自動） |
| Phase 2.5: チェックポイント | 論文リストをユーザーに提示・承認 | **承認が必要** |
| Phase 3: 論文分析 | thesis/core/diff/limitの4軸でアノテーション | なし（自動） |
| Phase 4: DOI解決 | arXiv IDをpublisher DOIに昇格 | なし（自動） |
| Phase 5: 統合分析 | thesis/foundation/progress/gap（seedは任意） | なし（自動） |
| Phase 6: 参照検証 | `reference-verify`スキルで幻覚チェック | triage対応が必要な場合あり |
| Phase 7: レポート生成 | `docs/SURVEYS/<topic_slug>.md`に出力 | なし（自動） |

**Phase 2.5の承認なしにPhase 3は開始しない。** Phase 3はトークンと時間を最も消費するため、
論文リストを確認してから着手する設計になっている。

## スコープパラメータ

| パラメータ | 選択肢 | デフォルト |
|-----------|--------|-----------|
| 深度 (depth) | `focused`（コアトピックのみ、20〜40本）/ `broad`（隣接分野含む、40〜60本） | インタラクティブに確認 |
| seed | `required`（研究アイデアの提案を生成）/ `not-required`（Gapまでで終了） | `not-required` |
| 制約 (constraint) | 実験環境・ハードウェア・リソースの制限（seedの実現可能性評価に使用） | なし |

## 出力レポートの構成

```
docs/SURVEYS/<topic_slug>.md
├── メタデータ表（トピック、日付、論文数、使用ソース）
├── Research Landscape Overview（分野の全体像）
├── Survey Findings
│   ├── Thesis（分野の根本的未解決問題）
│   ├── Foundation（共有技術基盤）
│   ├── Progress（解決済み問題の軌跡）
│   ├── Gap（構造的未解決問題）← Research FramingのMove 2: Nicheに対応
│   └── Seed（任意、research proposals）
├── Paper Catalogue（論文ごとのthesis/core/diff/limitアノテーション）
└── Survey Methodology（検索ログ、DOI解決ログ、幻覚チェック）
```

## 論文アノテーションの4軸

各論文に以下の4フィールドを付与する。

| フィールド | 内容 | 注意 |
|-----------|------|------|
| `thesis` | 著者の中心的主張（「何をした」ではなく「何が真であると主張しているか」） | |
| `core` | 手法の不可欠な要素（これがなければ成立しない部分） | 具体的に記述 |
| `diff` | 先行研究との差分（どの限界を克服したか） | 先行研究を名指しで |
| `limit` | 著者が明示した制約・未解決問題 | **著者の発言のみ。推測・追加不可** |

## 情報ソース

| ソース | 用途 |
|--------|------|
| WebSearch | 主要な発見ツール。幅広い検索に使用 |
| arXiv API | プレプリントの網羅的収集 |
| ar5iv | arXiv論文の全文アクセス（Limitations/Future Work取得） |
| `scripts/search_semantic_scholar.py` | 引用数・DOI・venue情報の取得 |
| `scripts/search_openalex.py` | 2億5000万件以上の文献からの検索 |
| `fetch_with_auth` MCP | ペイウォール論文へのアクセス（機関認証クッキー使用） |
| DBLP API | publisher DOIの解決（第1候補） |
| Semantic Scholar API | publisher DOIの解決（第2候補、レート制限: 1 req/sec） |
| Crossref API | publisher DOIの解決（フォールバック） |

`fetch_with_auth` MCPを使用するには機関認証クッキーの事前エクスポートが必要。
詳細は `.claude/mcp/academic-fetch/README.md` を参照。

## `/research-framing`スキルとの連携

`/research-framing`スキルは、このスキルを起動する直前に会話上に以下の形式でスコープ情報を置く。

```
文献調査のスコープ:
- トピック: [英語キーワード]
- 深度: focused / broad
- seed: 不要 / 必要
- 目的: [research-framingのどのステージのためか]
```

このスキルはPhase 1の冒頭でこれを検出し、確認をスキップして調査を開始する。

**Research FramingのCARSムーブとの対応**:

| レポートセクション | Research FramingのCARSムーブ |
|-------------------|-------------------|
| Research Landscape Overview + Foundation + Progress | Move 1: Territory |
| Survey Findings → Gap | Move 2: Niche |
| Survey Findings → Seed（要求時のみ） | Move 3: Occupationの検証材料 |

文献調査完了後、`/research-framing`スキルはCARSの3ムーブからCARS統合骨格（8〜12文）を生成し、
ユーザーへの提示前にサブエージェントによるレビューを実行する。骨格とA1/A2をファイルに
書き出してTaskツール経由でサブエージェントを起動し、生成時の会話コンテキストを持たない
独立したエージェントがTerritory→Nicheの導線・Niche→Occupationの対応・A1/A2との整合・
RA-L査読者視点の4基準で評価する。NGがあれば修正してから提示する。

## 参照ファイル

このスキルは実行時に以下のファイルを読み込む。事前に配置しておくこと。

| ファイル | 内容 | 必須/任意 |
|---------|------|---------|
| `references/report_template.md` | レポートの完全な構造テンプレート | **必須** |
| `references/seed_format.md` | Seedセクションの構造（seed要求時のみ読み込み） | seed使用時は必須 |
| `references/venues_robotics.md` | ロボティクス分野のベニューリストと検索戦略（ロボティクス系トピック時に自動読み込み） | ロボティクス系トピック時は必須 |
| `.claude/rules/references.md` | 引用規則・BibTeX規則 | **必須** |
| `scripts/search_semantic_scholar.py` | Semantic Scholar APIスクリプト | **必須** |
| `scripts/search_openalex.py` | OpenAlex APIスクリプト | **必須** |

## 更新履歴

| 日付 | 変更内容 |
|------|---------|
| 2026-03-27 | `references/venues_robotics.md`を追加。ロボティクス系トピック検出時に自動読み込みされるベニューリストと検索戦略を定義。 |
| 2026-03-27 | Phase 1にコンテキスト参照ロジックを追加（`/research-framing`スキルとの連携対応） |
