# Skills 汎用化ログ

## 2026-03-19: スキル定義の調査と修正開始

### 調査対象
- commit, push, commit-and-push, log-progress, wrap-up-session

### 発見した問題

1. **commit/push に `ros-o` がハードコード** — 特定プロジェクトのメインブランチ名が埋め込まれており、汎用スキルとして不適切
2. **log-progress にファイルパスがハードコード** — `docs/TODO.md`, `docs/LOGS/`, `docs/ISSUES.md`, `docs/PLAN.md` が固定。フォークプロジェクト等で成立しない
3. **log-progress の参照処理ルール** — `.claude/rules/references.md` は研究プロジェクト固有
4. **ユーザーレベル CLAUDE.md にプロジェクト固有の内容が混在** — 検証コマンド、コンテナ環境、参照先、注意事項が osx_ose_for_learning_manipulation 固有

### 実施した修正
- commit/SKILL.md: `ros-o` への警告ルールを削除
- push/SKILL.md: `ros-o` への特別処理（警告・確認・force push 禁止）を削除

### 議論と方針決定
- ブランチ保護は必要なプロジェクトでプロジェクトレベルの CLAUDE.md に個別定義する
- log-progress は役割定義をスキルに残しつつ、パス解決は CLAUDE.md に委ねる方針に
- ユーザーレベル CLAUDE.md を汎用化し、スクラッチプロジェクトの標準ドキュメント構成を明記する

### 追加修正
- log-progress/SKILL.md: パスのハードコードを除去。CLAUDE.md からのパス解決 + ファイルが存在しなければスキップする設計に変更。参照処理は `.claude/rules/references.md` が存在する場合のみ適用に緩和
- CLAUDE.md: プロジェクト固有の内容（コマンド、コーディング規約の一部、注意事項、コンテナ環境、参照先）を `~/_CLAUDE.md` に退避。汎用的な内容のみ残し、「標準ドキュメント構成」セクションを新設
- wrap-up-session/SKILL.md: 確認の結果、変更不要

### 残作業
- `~/_CLAUDE.md` の内容を対象プロジェクトの CLAUDE.md に配置する（対象プロジェクトでの作業時に実施）

---

## 2026-04-20: 知識ソース明示ルールの策定と request-source スキル実装

### 背景

Isaac Sim ロープシミュレーションのデバッグ中、内部知識のみで API 挙動を断言し誤った説明をした。
その原因の内省と、再発防止のための構造的対策を議論・実装した。

### 内省の結論

- 「パターンマッチが発火した瞬間に確信に変わり、検証ステップが消えた」
- CLAUDE.md のルールは「外部から課された制約」であり、内側から自然に発火しない
- ルールの想起が能動的に必要な構造では、高速なパターンマッチに負ける

### 実装内容

**CLAUDE.md への追記（`~/.claude/CLAUDE.md`）:**
- 知識ソース明示ルール: 全回答末尾に `[知識ソース]` ブロック（内部知識／外部知識／観測事実 の3分類）を水平バーで分離して付与
- WebSearch/WebFetch 必須トリガー: A〜F の6カテゴリ（API仕様・エラー診断・推論マーカー・数値根拠・環境依存・学術工学情報）に該当する場合は判断なしに即実行

**request-source スキル（`~/.claude/skills/request-source/SKILL.md`）:**
- `/request-source この回答` または `/request-source 直前の回答` で知識ソースブロックを生成
- 発火タイミングはスキル内では定義せず、CLAUDE.md のルールに委ねる

### 調査で判明した構造的限界

- CLAUDE.md はセッション開始時のコンテキストに入るが、hooks のような確実な自動発火はない
- `Stop` フックはレスポンステキストを検査できないため、ブロック有無の機械的チェックは不可能
- スキルは tool call として実行され「編纂中の回答への末尾追記」は構造的に不可能
- 結論: CLAUDE.md ルール（自発的遵守）＋ユーザーの明示呼び出し（`/request-source`）の組み合わせが現時点の最善

### 用語の整理

- 「未検証」「WebSearch/WebFetch 未実施」という表現を廃止
- 「内部知識」（学習データ由来）と「外部知識」（このセッションでの WebSearch/WebFetch 結果）に統一

---

## 2026-04-21: request-source スキル description 最適化と自動発火評価

### 変更内容

**CLAUDE.md（`~/.claude/CLAUDE.md`）:**
- 知識ソース明示ルールに `/request-source` スキル参照を追加（`/request-source スキルの出力フォーマットに従う`）
- ブロック省略時の自動補完ルールを追加：「ブロックの付与を省略した場合、次の自分の返答の冒頭で `/request-source 直前の回答` を自動実行して補完せよ」

**request-source/SKILL.md:**
- description を改訂：英語フレーズのみ → 日本語フレーズ列挙（「ソースは？」「内部知識？」「根拠は？」「WebSearch した？」等）を追加、"Always use" と積極的なトリガー指示に変更

### 自動発火メカニズムの実測

**評価手法**: skill-creator の `run_eval.py` で description マッチ型トリガーを 20 クエリ × 3 回測定（Iter 1: 元 description、Iter 2: 改訂 description）

**結果:**

| 発火経路 | 結果 |
|---|---|
| Description マッチ（自律判断） | **0%**（Iter 1・2 ともに recall=0%、precision=100%） |
| CLAUDE.md 明示ルール経由 | **成功**（意図的省略 → 次返答で自動補完：1/1） |
| Explicit `/request-source` | ~100%（設計上） |

**知見:**
- `run_eval.py` は description マッチ型トリガーを UUID 付き一時コマンドで測定する。明示 slash command 呼び出しはカウントされない
- description の記述をどう変えても Claude が自律的にこのスキルを選ぶことは起きない（recall=0% が 2 iter で安定）
- 信頼できる自動発火は CLAUDE.md 明示ルールのみ。名前を `append-sources` 等に変えても description マッチ改善は見込めない
- `ANTHROPIC_API_KEY` が環境変数として未設定のため `improve_description.py`（API 直呼び出し）は利用不可。`run_eval.py`（`claude -p` 経由）は動作する

## 2026-06-04: 原典照合検証の追加と EPT

### 背景

literature-survey と paper-summary に原典照合検証を追加。LLM による要約が原論文と一致しない記述を生むリスクへの対策。

- **paper-summary Step 6**: 同一エージェントが PDF に戻って self-verification
- **literature-survey Phase 3 クロス検証**: 別エージェントがハブ深読みノートを PDF と照合
- **literature-survey Phase 5 Synthesis Trace-back**: synthesis の主張をハブ深読みノートと照合

2 段階で「原典 → 深読みノート → synthesis」の連鎖全体を検証する設計。

### EPT 結果: paper-summary Step 6

3 iterations で収束。テスト材料: Hogan-WAFR2016 の要約に 3 エラーを植え込み。

| Iter | 修正 | 精度 | 新出不明瞭点 |
|---|---|---|---|
| 1 | baseline | 100% | 1（検証対象セクションの範囲） |
| 2 | 対象/対象外セクション明示、limitation カテゴリ追記 | 100% | 1（limitation 出力形式） |
| 3 | limitation 区別の注記方法を明示 | 100% | 0 |

### EPT 結果: literature-survey Synthesis Trace-back

3 iterations で収束。テスト材料: ft_estimation_placement.md の synthesis 抜粋 + Nadeau-TRO2025 ハブノート。

| Iter | 修正 | A 精度 | B 精度 | 新出不明瞭点 |
|---|---|---|---|---|
| 1 | baseline | 100% | 100% | 3（スコープ、粒度、修正 vs 削除基準） |
| 2 | スコープ明示 + 粒度例示 + 修正/削除基準 | 100% | 100% | 2（パラフレーズ、否定的主張） |
| 3 | 否定的主張 + 合理的意訳の判定基準 | 100% | 100% | 0（実質） |

Phase 3 クロス検証はコア検証ロジックが paper-summary Step 6 と同一のため、構造審査のみで完了。

## 2026-06-17: 日本語技術文書・論証ギャップ編集スキル登録

### 追加スキル

**japanese-tech-writing** (`~/.claude/skills/japanese-tech-writing.md`):
- k16shikano の gist (日本語技術文書の文章規範) をスキルとして登録
- CLAUDE.md に `@~/.claude/skills/japanese-tech-writing.md` を追加し, 全セッション常時読み込み化
- EPT 実施: 2 iter + hold-out, 全シナリオ 100% 収束. description の修正のみで完了 (本文修正不要)
- 設計判断: 技術的・学術的な話しかしない前提で常時読み込み (@include) を採用

**argument-gap-edit** (`~/.claude/skills/argument-gap-edit.md`):
- 論証ギャップ編集スキルとして登録
- japanese-tech-writing の適用手順の具体化として位置づけ
- 明示的に呼びたいときのみ使うスキルとして残置 (常時読み込みにはしない)

### 関連ファイル修正

- `literature-survey/SKILL.md`: 壊れた `japanese_style.md` 参照を削除
- `request-source/SKILL.md`: 節名参照を「参照情報の検証」→「外部ソース事前参照」に更新
- `rules/japanese_style.md`, `rules/japanese-writing.md` を `.bak` に退避

## 2026-06-22: research-theme-proposal Heilmeier H7/H8 設計問題の発覚

### 背景

P1 提案書（View-Dropout-Robust Multi-View JEPA World Models）のレビュー中に、H7 と H8 mid-term が同一対象を指しているのに別ラベルが付いている不整合に気づいた。
原典と照合した結果、テンプレート側の H7 改変が原因と判明した。

### 発見した問題

DARPA 原典の Heilmeier Catechism Q7 は "How long will it take?" であり、プロジェクト全体の所要期間を問う。
`research-theme-proposal` スキルでは以下の改変が加えられていた。

- `proposal_template.md` L36: H7 を "How long will the **first de-risking** take?" に書き換え
- `heilmeier_rubric.md` L16–17: H7 を「de-risking までの期間のみ答える」と定義し、H8 mid-term を「de-risking 実験 + kill criterion」と定義

結果として H7（de-risking の期間）と H8 mid-term（de-risking 実験 + kill criterion）が同じ工程を別ラベルで指す重複構造になっている。
また "first de-risking" の "first" は後続の de-risking が存在しない場合に誤解を招く。

### 初期修正案とその問題

H7 を原典に戻し, H7 でフェーズ構成を述べ, H8 で mid-term / final を Phase に紐付ける案を検討した.
しかし mid-term = de-risking に固執すると以下の問題が残った:

- Phase 2 (sim 本実験) が mid-term にも final にも位置づかない (P1 は Phase 1/2/3 の 3 フェーズ構成)
- de-risking は kill/go の二値判定であり, 進捗を測る「exam」とは性質が異なる
- 原典 Q8 の "exams to check for success" は成功に向けた中間確認であり, 撤退判定は含意されていない

### 最終修正方針: H8/H9 分離

上記を踏まえ, H8 と H9 を分離する案に至った:
- H7: 原典に戻す ("How long will it take?") → フェーズ構成・内容・期間
- H8: De-risking gate → kill criterion をここに集約 (原典にない追加設問)
- H9: 原典 Q8 ("What are the mid-term and final exams to check for success?") → mid-term = sim 本実験完了, final = 実機検証完了

テンプレートは既に原典から離れており (H6 が "Resource estimate" に改変済み), 8 問に固執する理由は薄い.
P1 には先行適用済み. テンプレート・ルブリックは未実施.

詳細は ISSUES.md「research-theme-proposal: Heilmeier H7/H8 テンプレート設計の問題」に記録。
