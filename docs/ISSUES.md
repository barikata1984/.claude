# Issues

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
