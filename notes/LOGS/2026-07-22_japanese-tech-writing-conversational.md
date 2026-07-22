# 2026-07-22 japanese-tech-writing スキル化と会話応答への試験投入

## Topic

GitHub 由来の日本語文章規範 markdown を正式なスキルに変換し、その規範を会話応答にも常時適用する構成を EPT で検証したうえで試験投入した。姉妹スキル cognitive-rhythm-writing の追加も含む。

## History

発端は CLAUDE.md が `@~/.claude/skills/japanese-tech-writing.md` を @import している構成が「スキルとして」正しく読めているのかという疑問。
確認すると、当該ファイルは @import(常時メモリ)としては読めているがスキル登録はされていなかった(スキル一覧に不在、`concise` は `skills/concise/SKILL.md` 形式なので登録済み)。スキル登録には `skills/<name>/SKILL.md` のディレクトリ形式が要る。

出所を researcher で調査。オリジナルはラムダノート代表 鹿野桂一郎 (k16shikano) が 2026-06-16 に公開した Gist `fd287c3133457c4fd8f5601d34aa817d` の `SKILL.md`(frontmatter 付き)。スキル共有マーケットプレイス(skills.sh, mcpmarket 等)への掲載は確認できず。手元ファイルは句読点を全角→半角に変換した派生版で、かつ 7-09 改訂の一文(辞書型断定の禁止)を欠く古い版だった。

管理方式を検討。候補は3つ挙がった。

- (a) 現状維持 + 出自コメント
- (b) Gist をクローンしてリポジトリ化
- (c) submodule 化

(b)(c) は却下。理由は、追随したい差分が実質「適用範囲の一行」だけであり、そのために GitHub リポジトリ新設・`.gitmodules`・fetch/merge/push/ポインタ commit の運用を背負うのは釣り合わないため。「規範がどう書かれているか」は upstream の領分、「いつ適用するか」はユーザーのポリシーで、後者を vendored ファイルに埋めると活発改訂中(6 月に 5 回)の upstream に対し恒久マージ負担が生じる。ポリシーは CLAUDE.md 側に置き、ファイルは純粋ミラーに保つ方式を採用。句読点は「どちらでもよい」との判断で、upstream 最新を全角のまま verbatim 取得(curl 上書き)する形にした。

スキル化を実施: `skills/japanese-tech-writing/SKILL.md` に upstream 最新を配置、旧 `skills/japanese-tech-writing.md` を削除、CLAUDE.md を新パスに差し替え。姉妹スキル cognitive-rhythm-writing (Gist `eb2929f13ed19c97188393d297be8432`) も追加。後者は本文冒頭で `../japanese-tech-writing/SKILL.md` を相対参照するため、兄弟ディレクトリ配置が前提になる(今回のレイアウトが条件を満たす)。

次に「会話応答にも規範を効かせたい」という要望。@import は本文を常時 context に載せるだけで、規範自身が適用範囲を「原稿の執筆・推敲時」に自己限定しているため会話応答には効かない。適用範囲を広げる指示の置き場所として、3案を比較した。

- description 書換: SKILL.md の description に会話応答も使用場面として含める。upstream verbatim を崩す難点
- @import 単独: 本文は載るが適用範囲の自己限定を上書きできない
- @import + UserPromptSubmit フック併用: 本文供給と適用指示を分離

併用案を採用。@import が本文を一度だけ載せ(重複を避ける)、search-first で実績のあるフックが適用指示を recency 込みで毎ターン注入する役割分担で、description を触らず verbatim ミラーを保てる。

「本当に効くか」を EPT で検証。素朴な self-report では「効いたっぽい」で終わるため、証拠は成果物(トランスクリプト JSONL と出力テキスト)の機械検査に限定する設計にした。主要指標は規範「LLM っぽい表現の禁止」節由来の禁止字面 18 種のカウント(正規表現、モデル判定なし)。engineer (ept-runner) に委譲。

実験中に2つの制約が判明。(1) サブエージェントによるグローバル `~/.claude` 改変が権限分類器にブロックされた(健全なガードレール、回避せず)。project-level 代替(作業ディレクトリごとに CLAUDE.md + フックを置き cwd で ON/OFF 切替)に変更。(2) @import 本文は子セッション JSONL に serialize されないため、本文有無は採点対象外の使い捨てメタプローブで判定。Phase 1 を並列化した際は条件境界(OFF 全終了 → 設定切替 → ON 開始)を JSONL タイムスタンプで機械検証し PASS。

結果: 主要指標は全域で床効果。違反は OFF 計 3 / ON 計 3(各 25 応答)。sonnet は誘発質問でも禁止字面をほぼ出さず、ON 効果は方向すら未決(レート比 95%CI [0.13, 7.5])。減衰仮説もテスト不能(床効果に加え、ON 腕が静的 @import と毎ターン注入を束ねており注入の寄与を分離できない設計不足)。機構検査(注入回数=ターン数、Skill 呼び出し 0、グローバル 2 ファイル無変更)は全 PASS。唯一頑健な効果は「ON で応答が一貫して長い」(sonnet、24/25 ペアで ON が長い、+35%)。

analyst で解釈。長さ増加の質的原因として3つの競合仮説を切り分けた。

- H1: 規範の論証充実(因果機構・根拠・留保の追加)
- H2: 文脈量による content-neutral な水増し
- H3: 準拠の演技(従っている姿を見せる)

判定は H1 が主因(増分は因果機構・根拠・留保という新規命題)、H2 は反証(REST vs GraphQL の一問で OFF>ON の符号反転が起き、長さは文脈量でなく論点数に追随)、H3 は書式とメタ文の薄い上塗りとして存在するが長さは駆動しない。副産物として、モデルが「厳密に論証する姿」を見せようとしてメタ文(「まずこの点を明示してから立場を述べる」等)を出し、これは規範自身が禁じる予告・メタ枠取りに抵触するという失敗モードを確認。

採用判断: 再実験ではなく実運用での試験投入を選択。導入コストが小さく(CLAUDE.md + フック)可逆で、「方向としては効く/失敗モードは長文化とメタ文」まで判明済みのため、対策込みで日常投入し観察する方が情報効率が高い。フック文言に失敗モードへの対抗(整形の節を適用しない、予告・メタ枠取り禁止の優先、concise の削減圧優先)を組み込んだ。

投入後、Opus 4.8 で ON/OFF ×2 の小プローブを実施(グローバル設定を実行中だけ OFF にし復元)。sonnet と逆に、Opus ON は OFF 比で短縮(キャッシュ解説 3413→1816 字)、禁止表現 0、メタ文・整形滲みなし。同一質問の sonnet ON(昨日の応答をトランスクリプトから再抽出)と比較すると齟齬は明確: sonnet は一文一改行・用語太字・網羅的列挙で「原稿」化し膨張、Opus は会話体裁を保ち機構に絞って圧縮。共通するのは です・ます→である調の転換と禁止表現の消失。実運用のメインループ(Fable/Opus)では失敗モードが出ず、sonnet 系サブエージェント(writer 等)でのみ原稿化の滲みが観察対象になる、という運用上の含意を得た。

## Decisions

- japanese-tech-writing を `skills/<name>/SKILL.md` 形式でスキル化、本文は upstream Gist の verbatim ミラー / 却下: 素 markdown 維持 — ユーザー確認済み
- 管理方式は curl 上書きミラー + 出自コメント / 却下: リポジトリ化 fork、submodule 化 — ユーザー確認済み
- cognitive-rhythm-writing を姉妹スキルとして追加 (兄弟ディレクトリ配置) / 却下: 追加しない — ユーザー確認済み
- 会話応答への適用は @import + UserPromptSubmit フック毎ターン注入の併用 / 却下: @import 単独、フック単独、description 書換 — ユーザー確認済み
- 効果検証は成果物の機械検査 (禁止字面カウント + JSONL 機構検査) / 却下: モデル自己申告 — ユーザー確認済み
- 実運用への試験投入を採用 (失敗モード対抗をフック文言に組込) / 却下: 再設計版 EPT を先に実施 — ユーザー確認済み

## Changes

- 追加: `skills/japanese-tech-writing/SKILL.md`(upstream verbatim)、`skills/cognitive-rhythm-writing/`、`hooks/style-rule-reminder.sh`
- 削除: `skills/japanese-tech-writing.md`(旧 @import 対象)
- 変更: `CLAUDE.md`(@import 張替 + 出自コメント)、`settings.json`(style-rule フック登録)
- 実験成果物は scratchpad(/tmp)にあり揮発。トランスクリプト JSONL(`~/.claude/projects/`)は永続
- 未コミット(このセッションで commit/push は未実施)

## Open Items

- 試験投入の実運用観察: メインループ(Fable/Opus)で失敗モード(長文化・メタ文・整形滲み)が出ないか、文体の である調転換を許容するか
- sonnet 系サブエージェント(writer/researcher)での原稿化の滲みを監視
- 決めきれない論点が溜まったら再設計版 EPT を別セッションで(判定型指標で床効果回避、対象を Fable/Opus に、OFF/静的のみ/静的+注入の 3 腕化)
- 実験記録本体(results.md, scores CSV, analyst メモ)は /tmp のみで揮発済み。必要なら次回トランスクリプトから再構成
