# 2026-07-20 subagent-execution-mode

## Topic

log-progress の lint パスが同期実行でメインをブロックしていた不具合の是正。
併せて委譲の実行モード (background/foreground) に関する一般則を追加し、他スキルが同じ失敗モードに陥っていないかを監査した。

## History

出発点は実運用での症状だった。
/log-progress の step 6 (最後の lint パス) で、メインが lint サブエージェントを同期実行 (`run_in_background: false`) し、その完了までユーザーの次の要求を受けられずブロックした。
ユーザーの不満は「応答性を保つために委譲したのに、同期で待つなら意味がない」。

診断を実ファイルで検証した。
提示された診断は 2 点。

- Agent ツールはデフォルトで background 実行であり、ツール側のバグではなく、メインが foreground を選んだのが直接原因
- 誘因は step 6 の「Spawn a subagent … It reads and reports … Fix legitimate findings yourself」という記述で、lint→報告→修正を 1 ターン内の逐次処理として読ませ、同期実行を促している

SKILL.md を読み、両方とも裏付けられた。
加えて step 7 が報告項目に「lint findings and fixes」を含めており、report する前に lint 完了が必要になる結合を発見した。
逐次的な文面 (step 6) と、報告に lint 結果を要求する結合 (step 7) の二重で同期ブロックを強制していた。

トレードオフの判断が要だった。
log-progress は /wrap-up-session の一部としてセッション終了直前に使われることがあり、background lint が完了前にセッションが閉じると修正が失われる。
選択肢は次の 3 つ。

- 全面同期 (現状): 応答性を捨てる
- 全面 background: wrap-up で lint 修正を取りこぼす恐れ
- 状況で分岐: standalone は background、wrap-up は同期

3 つ目を採った。
standalone では turn が step 7 の報告で閉じ、lint 結果を待つ理由がない (background にして完了通知で追報告)。
/wrap-up-session の中では次段の commit-and-push が同じファイルを commit するため、lint の修正が commit 前に着地する必要がある。
これは「結果が現ターンの続行に必要」に該当し、同期実行が正当化される。
この切り分けは、後述する delegation.md の一般則とそのまま整合する。

SKILL.md への修正は surgical に 2 箇所。
step 6 を「background by default」に書き換え、`run_in_background: false` を渡さない旨と、wrap-up 例外 (次段が同ファイルを commit するので同期) を明記した (違反リストと「reads and reports — does not edit」は不変更)。
step 7 は即時報告を write 側の項目に限定し、lint findings は subagent 復帰後の追報告へ分離した (wrap-up 時は同期なので同一報告に合流)。

この不具合は log-progress の局所修正で終えることもできたが、根因は各スキルが timing を文面で暗黙に決めていたことにあるため、delegation.md に一般則を 1 項目置いてクラス全体の指針とした: `run_in_background: false` は結果が現ターンの続行に必要なときだけ、応答性維持の委譲なら background にする。

修正後の文面が意図通りの挙動を引き出すかを、バイアスのない executor で軽く検証した。
背景の不具合には触れず、改訂後の step 6/7 だけを与えて実行計画を語らせたところ、standalone では (a) `run_in_background` を省略して background、(b) lint 完了前に step 7 を返す、(c) lint 結果は subagent 復帰後の追報告、と解釈し、wrap-up 例外も同期側に正しく振り分けた。
「同期でブロックすべき」という誤読は出ず、成功基準を満たした。

続いてユーザーの依頼で、他スキルが同じ失敗モードに陥っていないかを監査した。
`~/.claude/skills/` を grep して spawn に言及する 12 スキルを洗い出し、log-progress を除く 11 件を機能グループで 2 つに分けて並列調査した。
各エージェントには失敗モードの定義 (結果が続行に不要なのに同期ブロックする) と、正当なバリア (fan-out 結果の合成や下流ステップの入力など、結果が本当に必要なもの) との区別基準を渡した。
監査の内訳はこうだった。commit/push は subagent が成果物そのものを作り、literature-survey や reference-verify は fan-out 結果を次フェーズが消費し、いずれも正当なバリア。sweep-run は tmux の detached セッションで spawn せず、paper-summary/research-proposal は subagent を起動しない。
どれも同期待ちが正当か、そもそも spawn しないかのどちらかで、11 件に BLOCK-UNNECESSARY は 1 件もなかった。
分岐点は「subagent の出力が成果物・下流入力か、既に確定・保存済みの作業への事後チェックか」であり、後者は log-progress の lint だけだった。
監査で新たな不具合が出なかったので、他スキルへの予防的な文面調整は行わなかった。

最後に、報告で使った「delegation.md の一般則がこのクラス全体をガードする」という表現をユーザーに問われ、言い過ぎだったと訂正した。
設定ファイルの一文はセッション開始時に文脈へ読み込まれ判断を促す助言であって、自動で background にする強制機構ではない。

## Decisions

- lint 実行モードを background 既定 + wrap-up 例外で同期に決定 / 却下: 全面同期、全面 background — ユーザー確認済み
- delegation.md に一般則「run_in_background: false は結果が現ターンの続行に必要なときだけ」を追加 / 却下: log-progress の局所修正のみ — ユーザー確認済み
- 他 11 スキルは同じ失敗モードなしと判定し修正は log-progress + delegation.md に留める / 却下: 予防的な文面調整の横展開 — エージェント判断

## Changes

- `skills/log-progress/SKILL.md` — step 6 を background 既定 + wrap-up 例外に改訂、step 7 の報告を即時化し lint findings を追報告へ分離
- `rules/delegation.md` — 「実行モード」節を追加 (1 項目)
- 他スキルの監査は読み取りのみ、ファイル変更なし
- 上記 2 ファイルは未コミット (本 wrap-up の commit-and-push で処理)

## Open Items

- 実行モード則 + wrap-up 例外の実運用観察: standalone/wrap-up で background/同期が実際に正しく分岐するか (→ TODO)
