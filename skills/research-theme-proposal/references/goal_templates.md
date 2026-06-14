# /goal Templates

headless / 自走実行用の起動テンプレート。条件文は「Claude が会話に表示した
内容だけで評価器（Haiku tier）が判定できる」形で書くこと。ファイルの存在や
内容を条件にする場合は、**本文を会話に表示する指示を条件文に含める**。

## 前提

- Claude Code v2.1.139+（/goal）。エージェントチームを使う場合は
  `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`（`.claude/settings.json` 設定済み）
- `research-context.md` 記入済み（placeholder 残存だと Phase 0 で停止し、
  /goal はターン上限まで空転するので注意）

## Template A: serial / 標準

```
claude -p "/goal research-theme-proposal スキルに従いロボット学習の新規研究テーマ提案を作成する。完了条件: output/proposals/ に status: screened の提案書が 3 件存在し、各提案書の全文と Rubric Scores 採点表（全 6 軸、Evidence 列付き）が会話に表示されており、check_proposal.py の検証が全件 PASS したことが表示されている。or stop after 40 turns"
```

## Template B: team モード（Phase 3+4 並列化）

```
claude -p "/goal research-theme-proposal スキルに従い、エージェントチームを使って（ideator 3 名を mechanism 別に、red-teamer 1 名）ロボット学習の新規研究テーマ提案を作成する。完了条件: Template A と同一。or stop after 60 turns"
```

注意: チームはトークン消費がメンバー数で線形に増える。まず Template A で
パイプライン自体の品質を確認してから B に移ること。

## Template C: survey 再利用（イテレーション時の節約）

```
claude -p "/goal 既存 survey（literature/surveys/<slug>.md）を再利用し、research-theme-proposal スキルの Phase 2 以降のみを実行する。完了条件: Template A と同一。or stop after 25 turns"
```

## 条件文を書くときの規則

1. 「良い提案」「十分な品質」等の主観語を入れない（非収束の原因）
2. 検証可能条件は 3 点セット: ①成果物の存在（件数・status）
   ②内容の会話表示（評価器の可視性）③機械チェック通過の表示
3. ターン上限を必ず付ける（serial 40 / team 60 / 部分実行 25 が初期値。
   実測で調整）
4. /goal はセッションあたり 1 つ。フェーズ別に条件を変えたい場合は
   セッションを分け、Template C 方式で部分実行する
