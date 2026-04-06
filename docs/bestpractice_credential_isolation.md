# Claude Code スキルにおけるクレデンシャル管理のベストプラクティス

> 最終更新: 2026-04-06
> 対象: Claude Code のスキル（SKILL.md + スクリプト + MCP サーバー）を組織内で共有する際の、
> API キー等シークレットの安全な取り扱い

---

## 1. 脅威モデル

Claude Code 内の LLM エージェントは、ユーザーのシェル環境でツールを実行できる。
この環境にシークレット（API キー等）が存在する場合、以下のリスクがある:

- **意図しない漏洩**: エージェントが `env` や `echo $API_KEY` 等でシークレットを読み取り、
  ツール出力やログに含めてしまう
- **プロンプトインジェクション経由の悪用**: 悪意あるコンテンツ（リポジトリの README 等）が
  エージェントの行動を誘導し、シークレットを外部に送信させる
- **コンテキスト残留**: シークレットが会話履歴に残り、後続のやり取りで意図せず参照される

**対策の目標**: エージェントに必要な「機能」を提供しつつ、生のクレデンシャルには
一切アクセスさせない。

---

## 2. エビデンス

以下の一次情報源から、クレデンシャル管理に関する原則を抽出した。

### E1. Anthropic "Securely deploying AI agents"

- URL: https://platform.claude.com/docs/en/agent-sdk/secure-deployment
- 種別: Claude Code / Agent SDK の公式セキュリティガイド

**引用 (Security boundaries)**:
> "A security boundary separates components with different trust levels. For high-security
> deployments, you can place sensitive resources (like credentials) outside the boundary
> containing the agent. If something goes wrong in the agent's environment, resources
> outside that boundary remain protected."

**引用 (Credential management — The proxy pattern)**:
> "The recommended approach is to run a proxy outside the agent's security boundary that
> injects credentials into outgoing requests. The agent sends requests without credentials,
> the proxy adds them, and forwards the request to its destination."

**引用 (Credentials for other services — Custom tools)**:
> "Provide access through an MCP server or custom tool that routes requests to a service
> running outside the agent's security boundary. The agent calls the tool, but the actual
> authenticated request happens outside."

**引用 (Least privilege テーブル)**:
> Credentials → "Inject via proxy rather than exposing directly"

### E2. Errico, Ngiam & Sojan "Securing the Model Context Protocol" (arXiv:2511.20920)

- URL: https://arxiv.org/abs/2511.20920
- 種別: MCP のセキュリティリスクと制御に関する学術論文

**引用 (Section 3.4.2 — Secrets and Credentials Exposure)**:
> "For production operations, agents should never access secrets directly; instead, they
> should require users to run actions out of the agent context."

**引用 (Section 4.5 — Centralized Security Governance)**:
> "Centralized credential management eliminates user-managed tokens and API keys. All MCP
> servers authenticate using per-user OAuth flows integrated with organizational identity
> providers."

### E3. OWASP Top 10 for LLM Applications 2025 — LLM07: System Prompt Leakage

- URL: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- 種別: LLM アプリケーションのセキュリティリスク分類（業界標準）

**引用 (Mitigation)**:
> "Enforce credential externalization — store API keys, passwords, and tokens in secure
> configuration management systems, not in prompt instructions."

**引用 (Architectural principle)**:
> "Teams should never treat the system prompt as a secret or rely on it as a security
> control."

### E4. OWASP AI Agent Security Cheat Sheet

- URL: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- 種別: AI エージェントのセキュリティ実装ガイド

**引用 (Tool Security)**:
> "Grant agents the minimum tools required for their specific task"

**引用 (File Access Control)**:
> `blocked_patterns: ['*.env', '*.key', '*.pem', '*secret*']`

---

## 3. 原則

上記エビデンスから、以下の4原則を抽出する。

| ID | 原則 | 内容 | 根拠 |
|----|------|------|------|
| P1 | クレデンシャル外部化 | シークレットをエージェントのコンテキスト（環境変数・プロンプト・ツール出力）に置かない | E1, E2, E3 |
| P2 | セキュリティ境界分離 | クレデンシャルを保持するコンポーネントと、エージェントが動作するコンポーネントを異なる信頼ゾーンに配置する | E1 |
| P3 | 仲介者パターン | エージェントと外部 API の間にプロキシまたは仲介プロセスを置き、クレデンシャルの注入を仲介者側で行う | E1 |
| P4 | 最小権限 | エージェントには必要な機能（検索結果の取得等）のみを公開し、生のクレデンシャルへのアクセスを与えない | E1, E4 |

---

## 4. 推奨パターン

### 4.1 Claude Code における実装選択肢

P1-P4 を満たす実装パターンは複数存在する。以下はその比較:

| パターン | P1 外部化 | P2 境界分離 | P3 仲介者 | P4 最小権限 | 実装コスト |
|---------|:-:|:-:|:-:|:-:|:-:|
| 環境変数に直接 export | x | x | x | x | 最小 |
| スクリプト内で `pass` 呼び出し | o | x | partial | partial | 小 |
| **MCP サーバー** | **o** | **o** | **o** | **o** | 中 |
| HTTP プロキシ (Envoy 等) | o | o | o | o | 大 |

**MCP サーバーと HTTP プロキシは同等の原則充足度を持つ。** Claude Code の文脈では、MCP サーバー
がツール拡張の標準機構であるため、もっとも自然な選択となる。

> **注**: 「MCP サーバーが唯一の正解」と述べた文献は存在しない。上記は確立されたセキュリティ
> 原則 (P1-P4) を Claude Code のアーキテクチャに適用した結果としての推奨であり、
> 推論に基づく判断である。

### 4.2 アーキテクチャ

```
┌──────────────────────────────┐     MCP protocol     ┌────��────────────────────┐
│  Claude Code (エージェント)    │ ◄── tool I/O ──►    │  MCP サーバー (別プロセス)  │
│                              │  検索結果のみ返る      │                         │
│  - SKILL.md の指示に従い      │                      │  - API キーを保持         │
│    MCP ツールを呼び出す        │                      │  - HTTP リクエストを発行   │
│  - API キーに触れない         │                      │  - 結果のみ返却           │
└──────────────────────────────┘                      └─────────────────────────┘
                                                              ▲
                                                              │ 起動時に注入
                                                       ┌──────┴──────┐
                                                       │ シークレット  │
                                                       │ ストア       │
                                                       │ (pass, Vault,│
                                                       │  env, etc.)  │
                                                       └─────────────┘
```

**セキュリティ境界**: MCP プロトコルが境界となる。エージェントはツールの入出力のみアクセス可能で、
サーバープロセスの内部状態（環境変数、HTTP ヘッダー等）にはアクセスできない。

---

## 5. 実装ガイド

### 5.1 MCP サーバーの実装例

以下は Semantic Scholar API を MCP サーバーとして提供する最小実装例:

```python
#!/usr/bin/env python3
"""Semantic Scholar MCP Server — API キーをサーバー内部に隔離する."""

import json
import os
import sys
import urllib.request
import urllib.parse


def search(query: str, limit: int = 10, year: str | None = None) -> list[dict]:
    """Semantic Scholar API を呼び出し、結果を返す."""
    # API キーはサーバープロセスの環境変数から取得（エージェントには見えない）
    api_key = os.environ.get("S2_API_KEY")

    base = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": str(limit),
        "fields": "title,authors,year,abstract,citationCount,url,externalIds",
    }
    if year:
        params["year"] = year

    url = f"{base}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    if api_key:
        req.add_header("x-api-key", api_key)

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    return data.get("data", [])


def main():
    """MCP stdio サーバーのメインループ（簡略版）."""
    # 実際の実装では mcp ライブラリを使用する
    # ここでは概念を示すための擬似コード
    for line in sys.stdin:
        request = json.loads(line)
        if request.get("method") == "tools/call":
            params = request["params"]
            if params["name"] == "semantic_scholar_search":
                args = params["arguments"]
                results = search(
                    query=args["query"],
                    limit=args.get("limit", 10),
                    year=args.get("year"),
                )
                # 結果のみ返す（API キーは含まれない）
                response = {"result": results}
                print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
```

### 5.2 MCP サーバーの起動設定

`~/.claude/mcp.json` にサーバーを登録する。API キーの注入方法は環境に応じて選択する。

**パターン A: ラッパースクリプト経由（`pass` / Vault / 任意のシークレットストア）**

```bash
#!/bin/bash
# ~/.claude/mcp/semantic-scholar/start.sh
export S2_API_KEY="$(pass show api/semantic-scholar 2>/dev/null)"
exec python ~/.claude/mcp/semantic-scholar/server.py
```

```json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "bash",
      "args": ["~/.claude/mcp/semantic-scholar/start.sh"]
    }
  }
}
```

**パターン B: mcp.json の env フィールド（平文 — 開発用途向け）**

```json
{
  "mcpServers": {
    "semantic-scholar": {
      "command": "python",
      "args": ["~/.claude/mcp/semantic-scholar/server.py"],
      "env": {
        "S2_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

> **注意**: パターン B は `mcp.json` にキーが平文で保存される。`mcp.json` を git 管理する場合は
> パターン A を使用すること。

### 5.3 SKILL.md 側の記述

スキルの SKILL.md では、エージェントに MCP ツールの使用を指示する:

```markdown
## 検索ツール

Semantic Scholar の検索には `semantic_scholar_search` MCP ツールを使用せよ。
直接の HTTP リクエストや API キーの参照は禁止する。
```

### 5.4 スキル共有時のチェックリスト

スキルを組織内で共有する際、以下を確認する:

- [ ] **API キーがスキルのコード・ドキュメントに含まれていないこと**
- [ ] **SKILL.md が MCP ツール名で機能を参照し、API キーの直接使用を指示していないこと**
- [ ] **MCP サーバーのコードが API キーを出力（print / logging）していないこと**
- [ ] **MCP サーバーの起動設定例が文書化されていること**（ユーザーが自身の環境で設定できる）
- [ ] **API キーの取得元（サービスの登録ページ等）が文書化されていること**

### 5.5 gpg-agent の設定（`pass` 使用時の利便性向上）

`pass` をシークレットストアとして使う場合、GPG パスフレーズの再入力頻度を減らせる:

```conf
# ~/.gnupg/gpg-agent.conf
default-cache-ttl 14400   # 4 時間
max-cache-ttl 28800        # 8 時間
```

```bash
gpgconf --reload gpg-agent
```

---

## 6. エビデンスの限界

本文書の透明性のため、以下を明記する:

1. **「MCP サーバーがベストプラクティスである」と明示した文献は存在しない。**
   MCP サーバーは、Anthropic が "one of" の選択肢として記述した仲介パターンの一つであり、
   HTTP プロキシ等と同等に扱われている (E1)。

2. **原則 (P1-P4) は複数の権威ある情報源で裏付けられている。**
   クレデンシャル外部化、セキュリティ境界分離、仲介者パターン、最小権限は
   いずれも直接的なエビデンスを持つ。

3. **「Claude Code スキルでは MCP サーバーが最も自然な実装である」は推論である。**
   Claude Code のアーキテクチャにおいて MCP がツール拡張の標準機構であることに基づく
   判断であり、文献による直接的な裏付けではない。

---

## 参考文献

- [E1] Anthropic. "Securely deploying AI agents."
  https://platform.claude.com/docs/en/agent-sdk/secure-deployment

- [E2] Errico, H., Ngiam, J. & Sojan, S. "Securing the Model Context Protocol: Risks,
  Controls, and Governance." arXiv:2511.20920, 2025.
  https://arxiv.org/abs/2511.20920

- [E3] OWASP. "Top 10 for Large Language Model Applications 2025."
  https://owasp.org/www-project-top-10-for-large-language-model-applications/

- [E4] OWASP. "AI Agent Security Cheat Sheet."
  https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
