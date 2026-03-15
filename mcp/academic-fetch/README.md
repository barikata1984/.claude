# Academic Fetch MCP Server

Institutional authentication cookies to access paywalled academic papers
(IEEE, Elsevier, Springer, ACM) from Claude Code.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- Browser extension: [Cookie-Editor](https://cookie-editor.com/)
  (available for Chrome / Firefox / Edge)

## Setup

Run from the project root:

```bash
bash .claude/setup.sh
```

This creates a `.mcp.json` symlink that registers the MCP server with Claude Code.

## Cookie Export Workflow

1. Open your browser and navigate to a publisher site (e.g., IEEE Xplore)
2. Sign in via your institution (e.g., "Access via institution" → university login)
3. Click the Cookie-Editor extension icon
4. Click **Export** → **JSON** (copies to clipboard)
5. **クリップボードにクッキーが入った状態のまま**、ターミナルで以下をタイプ実行:

```bash
bash .claude/mcp/academic-fetch/save-cookies.sh
```

このスクリプトはクリップボードから JSON を読み取り、既存クッキーとマージして
`~/.academic_cookies.json` に保存する。複数出版社のクッキーを扱う場合も、
各出版社で手順 1-5 を繰り返すだけでよい（自動マージ、重複排除付き）。

**注意**: コマンドは手でタイプすること。README からコピペするとクリップボードが
上書きされ、クッキー JSON が失われる。

## Session Expiry

Institutional cookies typically expire after 8–24 hours. When the server
detects session expiry, it returns a message asking you to re-export cookies.

Re-export flow:
1. Open the publisher site in your browser (should still be logged in or re-login)
2. Export cookies again via Cookie-Editor
3. Run `bash .claude/mcp/academic-fetch/save-cookies.sh`

No server restart is needed — the cookie file is re-read on each request.

## Rate Limiting

Requests are rate-limited to one every 3 seconds to respect institutional
access agreements. This is not configurable by design.

## Supported Publishers

| Publisher | URL Pattern | Notes |
|-----------|------------|-------|
| IEEE Xplore | `ieeexplore.ieee.org` | Article pages |
| Elsevier / ScienceDirect | `sciencedirect.com`, `elsevier.com` | |
| Springer | `link.springer.com` | |
| ACM DL | `dl.acm.org` | |
| Other | Any URL | Generic text extraction fallback |

## Troubleshooting

**"Cookie file not found"**
→ Export cookies and save to `~/.academic_cookies.json`

**"No cookies found for domain"**
→ Make sure you exported cookies while logged in to that specific publisher

**"Session expired"**
→ Re-login in browser and re-export cookies

**Empty or garbled output**
→ Some publishers render content via JavaScript, which this server cannot
execute. Use ar5iv for arXiv papers, or access the paper manually.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ACADEMIC_COOKIE_FILE` | `~/.academic_cookies.json` | Path to cookie file |
