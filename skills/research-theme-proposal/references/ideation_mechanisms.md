# Ideation Mechanisms

Phase 3 の発散は自由生成ではなく, 以下 4 メカニズムの**枠ごとに独立して**行う.
各メカニズムで 2 候補, 計 8 候補. 担当外メカニズムの発想が出たら破棄せず
担当メカニズムに翻訳できるか検討し, できなければ捨てる(枠の侵食を許さない).

共通入力: gap inventory(why-not-yet / enabler candidates 付き)+
research-context.md の capability summary + 担当 gap 割り当て(下記).
spawn prompt に capability summary が要約として与えられている場合は
その要約を正典として使う(research-context.md 本体の再読は不要).
各 mechanism の"手順"にある列挙・総当たりは内部作業であり,
出力ファイルには選定結果(候補 2 件)のみを書く.

## Gap 重点割り当て(リーダーが Phase 3 開始時に実施)

mechanism 枠の独立性は anchoring を防ぐが, gap の重複は防がない. 実測では
"強い gap"(enabler が新しく lab-fit が良い gap)に候補が殺到し(3 run 連続で
再現, 最悪 8 候補中 5 件が同一 gap), ポートフォリオの多様性が失われた上に
同一 gap 内で novelty を共食いする. これを防ぐため, リーダーは生成開始前に
gap を mechanism に重点割り当てる:

- 各 mechanism に**重点 gap を 1-2 個**割り当てる. 割り当ては"mechanism の問いと
  gap の性質の相性"で決める(例: enabler が新しい gap → M1, 評価手段が無い
  gap → M3, 強い共有前提に根差す gap → M4)
- 同一 gap を 3 つ以上の mechanism に重点割り当てしない
- 全 gap がどこかの mechanism でカバーされるようにする(gap 数 > mechanism 数 ×2
  の場合は lab-fit の良い gap を優先)
- 各 ideator は 2 候補のうち**少なくとも 1 件を重点 gap から**生成する.
  残り 1 件は任意の gap でよい(mechanism との相性が良い発想を妨げない)
- serial モードでも同じ割り当てを各パス冒頭で宣言してから生成する

共通禁止事項:

- 他 ideator / 他パスの候補を読むこと(anchoring 防止)
- gap inventory に無い gap を根拠にすること(思いつきの gap は survey の見落とし
  である可能性が高い. 必要なら gap inventory の追加提案として別途報告)
- research-context.md に無い機材・スキルを前提にすること(Readiness で
  New development に分類すれば前提にしてよいが, 過半が New になる候補は弱い)

---

## M1: enabler-driven

**問い**: 直近 24 ヶ月の enabler(新モデル・新データセット・新ハードウェア・
新データ収集手法)は, gap inventory のどの gap を"初めて攻撃可能"にしたか?

- 手順: enabler candidates を列挙 → gap × enabler の組を総当たりで眺め,
  why-not-yet が"この enabler の不在"で説明できる組を抽出.
  総当たりは全 gap × 全 enabler を一覧すれば足り, 深掘りは重点 gap 周辺を
  優先してよい
- 強い候補の形:"gap G は従来 X が無くて不可能だった. E の登場で X が
  手に入る. E を G に適用した研究はまだ無い(novelty-check で要確認)"
- 弱い候補の兆候: enabler が汎用すぎる("基盤モデルの進歩"),
  enabler→gap の対応が他の多数の gap にも同様に成り立つ(一意性が無い)

## M2: cross-domain transfer

**問い**: 隣接分野(CV / NLP / 制御 / 計算神経科学 / グラフィクス等)で
確立された手法・問題設定・評価プロトコルのうち, ロボット学習の gap に
未移植のものは何か?

- 手順: 各 gap について"この構造の問題は他分野でどう解かれているか"を問い,
  移植時に**何が非自明に壊れるか**(実時間制約・部分観測・接触力学・
  データ希少性)を特定する
- 強い候補の形: 移植の障害そのものが研究貢献になる(単純移植で済むなら
  既にやられているはずで, novelty-check で落ちる)
- 弱い候補の兆候:"X を robotics に適用"で説明が終わる(障害の特定が無い)

## M3: benchmark-definition

**問い**: gap inventory のうち"評価手段が無いから進まない"タイプの gap に対し,
新タスク・新ベンチマーク・新評価プロトコルの定義自体を貢献にできるか?

- 手順: concept matrix の疎な行・列のうち, 論文が無い理由が"興味が無い"
  ではなく"測れない"であるものを特定する
- ロボット学習固有の注意: 実機ベンチマークは再現性が本質的課題. 提案には
  再現性の担保方法(共通ハードウェアキット / sim 併設 / 評価手順の動画規約等)
  を必ず含める. これが無い benchmark 候補は red-team で確実に落ちる.
  独立フィールドは設けず, 動作原理スケッチまたは自己申告の弱点欄に組み込む
- 強い候補の形: ベンチマーク定義 + そのベンチマークが初めて可視化する
  既存手法間の未知の性能差の仮説. 対象 gap の評価指標自体が未確立の場合は
  "指標がモデル間・データ条件間でどう変化するか"の仮説で良い

## M4: assumption-busting

**問い**: survey の foundation(survey レポートの Foundation 節に列挙された,
全ハブが共有する技術的前提)のうち, 実は不要・有害かもしれないものはどれか?
survey レポート本体の Foundation 節は**読んでよい**(禁止事項が禁じるのは
他 ideator の候補のみ). team モードでは spawn prompt に Foundation 節の
全文を含めることを推奨.

- 手順: foundation の各要素について"これを外すと何が可能になるか /
  何が壊れるか"を問う. thesis の緊張(トレードオフ)を"両立"ではなく
  "前提の除去"で解消できないかを検討する
- 強い候補の形:"全手法が前提 A を置くが, A は歴史的経緯(当時の B の不在)
  によるもので, 現在は B があるため A 無しで成立し得る"(M1 との複合形は可.
  その場合 mechanism は M4 として記録し, enabler を why-now 欄に書く.
  Gap Grounding は Phase 5 提案書のセクションであり候補概要には無い)
- 弱い候補の兆候: 前提の除去が単なる一般化("より広いクラスで成立")で,
  除去の動機となる失敗事例を survey から示せない

---

## 候補 1 ページ概要の形式(Phase 3 出力)

```markdown
### Candidate {mechanism}-{n}: <title>
- mechanism: M1–M4
- gap_refs: [主たる gap を先頭に. why-not-yet / enabler が密接に関連する場合のみ複数可]
- 中核主張: <3 文以内>
- 動作原理スケッチ: <中核主張を実現する機構を 2-4 文.「どうやって」(何を入力に何を計算しどう使うか) に答える. 名前を挙げるだけの要素記述 (例:「ガウス測度を使う」) は不可>
- why-now: <全 mechanism で記載する. enabler 具体名は M1/M4 で必須, M2/M3 でも推奨>
- ラボ適合の初期見立て: <research-context のどの機材・スキルが効くか 1-2 文>
- 自己申告の最大の弱点: <red-team に先回りして 1 つ>
```
