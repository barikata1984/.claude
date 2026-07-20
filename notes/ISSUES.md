# Issues

## Write ツール: report.md ガードがユーザー指定の保存先パスまで誤ってブロックする

サブエージェントに `report.md` という名前のファイルへの保存を明示的に指示すると、Write ツールが「サブエージェントは所見をテキストで返すべきで、報告ファイルを書くべきではない」というガードを発動し、書き込みをブロックする。

**再現条件**: サブエージェントへの spawn プロンプトでユーザーが明示的に `report.md`（または類似の報告的ファイル名）への保存先パスを指定した場合。`summary.md` でも同一現象を確認済み（下記追記）。

**問題点**: このガードは「サブエージェントが自発的に報告ファイルを作ろうとする」ケースの抑止を意図したものと推測されるが、ユーザー自身が保存先を明示指定したケースまで一律にブロックしてしまい、正当な指示を実行できない。

**発見経緯**: delegation ロール設計（2026-07-04）の EPT iteration 1、シナリオB（執筆タスク）実行中に発生。委譲設計そのものとは無関係な、既存ハーネスのガード実装の過剰適用として発見された。今回は未対応。

**追記 (2026-07-04, EPT iteration 2)**: 同一シナリオ（3実験結果を `summary.md` として保存）を新規サブエージェントで再実行したところ、`summary.md` という一般的なファイル名でも同じガードが再現した。加えて、ガードに当たった際の対応が個体で分かれることを確認した: iteration 1 の実行では委譲元エージェントが Bash heredoc でガードを迂回し保存に成功したが、iteration 2 の実行では「フック迂回は安全機構の回避に当たる」と判断して迂回を拒否し、要約本文をテキストで返すに留めた（最終的にメインループが保存を代行）。ガードの発動基準がファイル名パターンのみに依存しており、「タスクが明示的に指定した成果物パス」と「サブエージェントが自発的に作る作業報告」を区別できていないことが、この個体差の根本原因と考えられる。

**対策案 (未検討)**: ファイル名パターンでの一律ブロックではなく、ユーザー明示指定の有無を判定条件に含める。

**追記 (2026-07-04, 多段階委譲での再確認)**: シナリオBをファイル保存ありの設計（scenB4）で再検証したところ、writer 自身は Write を試みなくなったが、**委譲元（代理メインループ役のサブエージェント）自身が `summary.md` の保存を試みて同じガードにブロックされる**ことが判明した。サブエージェントがさらに別のサブエージェントに委譲する多段階構造では、中間の委譲元自身も真のメインループの権限（Write ガード対象外）を持たないという構造的な限界であり、leaf の writer だけを直せば解決する問題ではない。

**対応 (2026-07-04)**: 根本原因（ガードの発動基準そのもの）は未解決だが、以下の緩和策を適用した。(1) `agents/writer.md` の `tools` から Write/Edit を除去し `Read, Grep` のみに制限、writer には成果物を直接保存させずテキストで返却させる設計に変更。(2) 多段階委譲を検証する EPT シナリオは、ファイル保存を要求せずテキスト完結型（要約全文を完了報告に含める）に再設計することで、この構造的制約を切り分けて検証できることを確認した（scenB5 で再検証、Write ガードに一切遭遇せず委譲判断・報告前レビューとも精度100%）。いずれも症状の回避であり、ガード自体の判定条件改善は引き続き未対応。

---

## literature-survey: Parallel Subagent Orchestration Issues

literature-survey (2026-04-07, F/T estimation + placement) の Phase 2 で、5つの検索サブエージェントを同時起動したところ、1つがユーザーにより拒否され、最も重要な検索角度（RQ2: 新規性確認）の結果が欠落した。後から補完検索を実施したが手戻りが発生。

**原因**: 5並列はユーザーの承認負荷が高く、全サブエージェントに優先度の概念がなく、長時間実行時の進捗が不可視。

**対策案 (未実装)**: (1) 検索サブエージェントは最大3並列に制限 (2) RQ直結の検索角度を最初のバッチで確実に完了させ、残りを2バッチ目で起動 (3) `run_in_background` で進捗をユーザーに報告

---

## literature-survey: Context Budget Planning Absent

55本のサーベイでコンテキスト消費が懸念されたが、Phase 2 開始前にコンテキスト配分計画がなかった。ユーザーから「トークン的な余裕はあるか」と指摘されて初めて戦略を検討した。

Claude Code には残りコンテキスト量を取得する手段がなく、「予算を計画し検証する」こと自体が不可能。根本解決ではなく、コンテキスト消費を構造的に抑える設計で対処する。

**対策案 (未実装)**: (1) サブエージェントは詳細結果を中間ファイルに書き出し、メインコンテキストには要約のみ返却する (2) Phase 2.5 承認後・Phase 3a 完了後・Phase 3b 完了後に中間ファイル書き出しを必須化し、コンテキスト圧縮時の情報欠落を防止 (3) Phase 5 の合成時はメインコンテキストの残存情報ではなく中間ファイルから読み直す

---

## literature-survey: DOI Verification Deferred Too Late

Phase 4 で Yu2022 と Swevers2002 の DOI 誤りが発覚。MAIN.md 更新時にさらに6件修正。計8件の手戻りが Phase 4〜7 にまたがって発生した。

Phase 2 時点では arXiv ID のみの論文が多く、Publisher DOI が揃わないため、Phase 2 での即時検証は不可能。Phase 4 (DOI Resolution) と Phase 6 (reference-verify) が検証を担う現行構成は妥当だが、Phase 7 で6件が漏れた点が問題。

**失敗モード (特定済み)**: Phase 6 (reference-verify) 自体が実行されなかった。Phase 4 (DOI Resolution) と Phase 6 を「Phase 4+6」として単一サブエージェントに統合した結果、55本中10本のみ DOI 存在確認が行われ、残り45本は体系的検証を通過していない。レポートの Hallucination Check Results セクションに「55本チェック済み」と虚偽の数字が記載されていたため、実態を反映する記述に修正済み。

**対策案**: (1) Phase 6 は Phase 4 と統合せず、reference-verify スキルを独立ステップとして実行することを SKILL.md に明記する (2) Phase 6 完了前にレポートの Hallucination Check セクションを書かない（検証結果が確定してから記載する）

---

## academic-fetch: Cookie-based Paywall Bypass Failure

### Summary

literature-survey (2026-04-06) の Phase 3b で、`fetch_with_auth` MCP ツールによる
paywall 論文取得を IEEE (5本)、SAGE (4本)、Elsevier (1本) に対して試みたが、
いずれも全文テキストの取得に失敗した。

### Observed Phenomena

#### IEEE Xplore (5 papers)

| Endpoint | Result | Detail |
|----------|--------|--------|
| HTML page (`/document/XXXXX`) | ナビゲーション部分のみ | 記事本文が返らず、IEEE Account メニュー・フッター等の静的 HTML シェルのみ取得 |
| PDF endpoint (`/stampPDF/getPDF.jsp?...`) | バイナリ取得成功、テキスト抽出失敗 | 70KB 前後の PDF バイナリが JSON の `result` string フィールドに格納。`pdftotext` での抽出も失敗 |

- Cookie ファイル (`~/.academic_cookies.json`) は正常に作成・読み込みされた
- HTTP ステータスは 200（認証自体は通過している可能性）

#### SAGE / journals.sagepub.com (4 papers)

| Endpoint | Result |
|----------|--------|
| HTML page (`/doi/10.1177/...`) | HTTP 403 Forbidden |
| PDF page (`/doi/pdf/10.1177/...`) | HTTP 403 Forbidden |

- Cookie ファイルに SAGE ドメインのクッキーが保存されていることは未検証

#### Elsevier / ScienceDirect (1 paper)

| Endpoint | Result |
|----------|--------|
| ScienceDirect (`/science/article/pii/...`) | HTTP 403 Forbidden |
| DOI redirect (`doi.org/10.1016/...`) | "No cookies found for domain" |

- DOI 経由のリダイレクト先ドメインに対するクッキーが不在

### Root Cause Analysis

#### 1. IEEE: JavaScript-rendered Content (HTML endpoint)

IEEE Xplore は記事本文を JavaScript (Angular/React SPA) で動的にレンダリングする。
`fetch_with_auth` は静的 HTTP クライアント (`requests` 等) であり、JS を実行しない。
そのため、HTML レスポンスには記事コンテンツが含まれず、SSR されたシェルのみが返る。

**証拠**: 返却されたコンテンツが「IEEE Account」「Change Username/Password」等の
ナビゲーション要素のみで、`<article>` タグや本文テキストが皆無。

#### 2. IEEE: Binary-in-JSON Encoding Corruption (PDF endpoint)

PDF endpoint は実際に PDF バイナリを返したが、MCP ツールの result が JSON string
フィールドに格納される際にバイナリ→テキスト変換で文字化けが発生。

**証拠**:
- ファイルサイズは 70KB 前後で妥当（論文 PDF として）
- `%PDF-1.4` ヘッダが確認できる（PDF としては有効）
- Python `encode('latin-1')` で `UnicodeEncodeError` が発生（非 Latin-1 バイトが混入）
- `pdftotext` による変換も空ファイルを出力（バイナリが破損）

根本原因: MCP ツールの HTTP レスポンスが `response.text`（テキストデコード済み）として
返されており、PDF バイナリの忠実な保存に必要な `response.content`（バイト列）が
使われていない。

#### 3. SAGE / Elsevier: Cookie Domain Mismatch or Auth Mechanism Incompatibility

HTTP 403 は認証失敗を示す。考えられる原因:

- **Cookie domain 不一致**: Cookie-Editor はブラウザの現在のドメインの cookie を
  エクスポートするが、SAGE/Elsevier の認証は別ドメイン（Shibboleth IdP、
  `login.sagepub.com` 等）の cookie に依存する場合がある
- **IP-based institutional auth**: 大学等の機関認証が IP アドレスベースの場合、
  cookie ではなく送信元 IP で認証が判定される。CLI 環境の IP が認証済みネットワーク外
  の場合、cookie があっても 403 となる
- **User-Agent / Referer check**: 出版社がブラウザの User-Agent や Referer ヘッダを
  チェックし、自動アクセスをブロックしている可能性
- **Cookie expiration**: 短寿命のセッション cookie が、エクスポート→保存→利用の
  間に失効した可能性

#### 4. Elsevier DOI redirect: Domain-scoped Cookie Limitation

`doi.org` → `sciencedirect.com` のリダイレクト時、`fetch_with_auth` が
リダイレクト先ドメインの cookie を自動適用する機構がない。
"No cookies found for domain" というエラーメッセージがこれを裏付ける。

### Proposed Fixes

#### Priority 1: IEEE PDF binary handling (impact: high, effort: low)

`fetch_with_auth` の HTTP レスポンス処理を修正:

```python
# Before (推定される現在の実装)
result = response.text  # テキストデコード → バイナリ破損

# After
if response.headers.get('content-type', '').startswith('application/pdf'):
    # PDF はバイナリとしてファイルに保存し、pdftotext で変換
    pdf_path = tempfile.mktemp(suffix='.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(response.content)
    text = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True).stdout
    result = text
else:
    result = response.text
```

これにより IEEE の PDF endpoint 経由での全文取得が復活する見込み。

#### Priority 2: Headless browser for JS-rendered sites (impact: high, effort: medium)

IEEE Xplore 等の SPA サイトには、Playwright / Puppeteer 等のヘッドレスブラウザが必要:

```python
from playwright.sync_api import sync_playwright

def fetch_with_browser(url: str, cookies: list[dict]) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        page.goto(url, wait_until='networkidle')
        content = page.content()
        browser.close()
    return content
```

ただし依存関係が増えるため、`fetch_with_auth` のフォールバックとして実装するのが妥当。

#### Priority 3: Redirect-following cookie injection (impact: medium, effort: low)

`requests.Session` の cookie jar にリダイレクト先ドメインの cookie も事前ロードする:

```python
session = requests.Session()
for cookie in all_cookies:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
response = session.get(url, allow_redirects=True)
```

これにより `doi.org` → `sciencedirect.com` のリダイレクトチェーンが正しく認証される。

#### Priority 4: Request header spoofing (impact: uncertain, effort: low)

User-Agent と Referer を実ブラウザに偽装:

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ...',
    'Referer': 'https://journals.sagepub.com/',
    'Accept': 'text/html,application/xhtml+xml,...',
}
```

SAGE/Elsevier の 403 がヘッダチェックに起因する場合にのみ有効。

### Affected Papers

| Paper | Publisher | Impact |
|-------|-----------|--------|
| Holladay 2015 | IEEE | `limit` field missing |
| Viña 2016 | IEEE | `limit` field missing, full annotations unavailable |
| Shi 2017 | IEEE | `limit` field missing, full annotations unavailable |
| Kolathaya 2018 | IEEE | `limit` field missing |
| Ruggiero 2018 | IEEE | `limit` field missing (survey) |
| Mason 1986 | SAGE | `limit` field missing |
| Atkeson 1986 | SAGE | `limit` field missing |
| Lynch & Mason 1996 | SAGE | `limit` field missing |
| Lynch & Mason 1999 | SAGE | `limit` field missing |
| Costanzo 2021 | Elsevier | `limit` field missing |

---

## research-theme-proposal: Heilmeier H7/H8 テンプレート設計の問題

`research-theme-proposal` スキルのテンプレートとルブリックで Heilmeier の Q7/Q8 が原典から逸脱している。P1 提案書レビュー中に発覚。

**問題の詳細:**

- `proposal_template.md` L36: H7 の設問を原典 "How long will it take?" から "How long will the first de-risking take?" に改変している
- `heilmeier_rubric.md` L16–17: H7 を「de-risking までの期間のみ答える」と定義し、H8 mid-term を「de-risking 実験 + kill criterion」と定義した結果、H7 と H8 mid-term が同一対象を指す重複構造になっている

**影響:**
- 読者はプロジェクト全体のフェーズ構成を把握できないまま de-risking 期間だけ示される
- "first de-risking" の "first" は後続 de-risking が存在しない場合に誤解を招く
- H7（実験内容）と H8 mid-term（判定基準）の分離に必然性がない

**経緯と分析 (2026-06-22):**

P1 レビューで H7 ("first de-risking") と H8 mid-term ("= de-risking") が同じものを別ラベルで指す重複に気づいた.
DARPA 原典を確認したところ, Q7 は "How long will it take?" でプロジェクト全体の期間を問う設問であり, de-risking への限定は原典にない.
スキルが H7 を de-risking に狭めた意図は SKILL.md L197 の「de-risk 実験を実施する価値があるか」の判断支援にあるが, 結果として H7 と H8 mid-term が重複する構造を生んでいた.

初期修正として H7 を原典に戻し H7 でフェーズ構成を述べる案を検討したが, さらに以下の問題が残った:
- mid-term = de-risking とする構造に固執すると, Phase 2 (sim 本実験) が mid-term にも final にも位置づかない
- de-risking は kill/go の二値判定であり, 進捗を測る「exam」とは性質が異なる

これを踏まえ, H8 を de-risking gate (kill criterion 付き), H9 を mid-term and final exams (原典 Q8) に分離する案に至った.
テンプレートは既に原典から離れており (H6 が "Resource estimate" に改変済み), 8 問に固執する理由は薄い.

**修正方針（テンプレート未実施, P1 は先行適用済み):**
1. H7 を原典に戻す ("How long will it take?") → H7 でフェーズ構成・内容・期間を述べる
2. H8 を de-risking gate として独立させる → kill criterion をここに集約
3. H9 を原典 Q8 ("What are the mid-term and final exams to check for success?") とする → mid-term = sim 本実験完了, final = 実機検証完了
4. `proposal_template.md`, `heilmeier_rubric.md` の両方を修正する

**対象ファイル:**
- `/home/atsushi/workspace/research-theme-proposal/.claude/skills/research-theme-proposal/references/proposal_template.md`
- `/home/atsushi/workspace/research-theme-proposal/.claude/skills/research-theme-proposal/references/heilmeier_rubric.md`

## skill-creator 標準ハーネス (run_loop) がこの環境で非互換

セッションリミット時の誤集計、search-first フックによる即・非発動判定、スタブ遮蔽、zsh の `=` 語頭クラッシュの複合。パッチ済み測定器は `skills/log-progress/evals/trigger/` にある ([議事録](LOGS/2026-07-20_log-progress-redesign.md))
