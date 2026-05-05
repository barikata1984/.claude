#!/bin/bash
# stop-scope-check.sh
#
# Mode: blocking
#
# CLAUDE.md「応答スコープ規約」bullet 1 の hook 化。
# 応答中に未要求サブセクション（以下のいずれかの形式で
# 「なぜ/結論/推奨/次のステップ/要点/まとめ/補足/例/比較/方針」を含む）
# が検出された場合、応答を block して再生成を強制する。
#   (a) Markdown 見出し: `## なぜ` / `### 推奨` 等
#   (b) 行頭 bold 強調: `**推奨進行順**: ...` 等
#       (見出し代わりに使う section header 相当の用法を捕捉)
#
# stop_hook_active=true の場合は無限ループ防止のため通過させる。

set -euo pipefail

LOG_FILE="$HOME/.claude/hooks/scope-violation.log"
mkdir -p "$(dirname "$LOG_FILE")"

INPUT=$(cat)
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || echo "false")

# 既に Stop hook 経由で再生成中 → 無限ループ防止
if [ "$STOP_ACTIVE" = "true" ]; then
    exit 0
fi

if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
    exit 0
fi

# このターンの境界を判定し以降のエントリだけを切り出す
TURN_DATA=$(jq -s '
  ([
    range(0; length) as $i
    | select(
        .[$i].type == "user"
        and (.[$i].message.content | type == "array")
        and (.[$i].message.content | any(.type == "text"))
        and (.[$i].message.content | any(.type == "tool_result") | not)
      )
    | $i
  ] | last // 0) as $idx
  | .[$idx+1:]
' "$TRANSCRIPT" 2>/dev/null) || exit 0

# このターンの最後の assistant の text 応答
RESPONSE=$(echo "$TURN_DATA" | jq -r '
  map(select(.type == "assistant"))
  | (.[-1].message.content // [])
  | map(select(.type == "text") | .text)
  | join("\n")
' 2>/dev/null || echo "")

if [ -z "$RESPONSE" ]; then
    exit 0
fi

# 未要求サブセクションキーワードを以下の 2 形式で検出:
#   (a) ## / ### 等の Markdown 見出し
#   (b) 行頭 bold 強調 `**...keyword...**` を section header 代用として使う形式
VIOLATIONS=$(echo "$RESPONSE" \
    | grep -nE "^(#{2,}[[:space:]]+.*(なぜ|結論|推奨|次のステップ|要点|まとめ|補足|例|比較|方針)|\*\*[^*]*(なぜ|結論|推奨|次のステップ|要点|まとめ|補足|例|比較|方針)[^*]*\*\*)" \
    || true)

if [ -z "$VIOLATIONS" ]; then
    exit 0
fi

# 違反を検出 → ログ記録 + block JSON 出力
{
    echo "=================================================="
    echo "Timestamp: $(date -Iseconds)"
    echo "Session: $SESSION_ID"
    echo "--- Violating headers ---"
    echo "$VIOLATIONS"
    echo "--- Response excerpt (first 800 chars) ---"
    echo "$RESPONSE" | head -c 800
    echo ""
    echo "--- End ---"
} >> "$LOG_FILE"

VIOLATING_HEADERS=$(echo "$VIOLATIONS" | head -3 | tr '\n' '|')
REASON="応答スコープ規約違反：質問で明示されていないサブセクション（「なぜ」「結論」「推奨」「次のステップ」「要点」「まとめ」「補足」「例」「比較」「方針」等）が検出されました。これらの見出しを削除し、ユーザーが字義通りに要求した内容のみで再生成してください。違反箇所: ${VIOLATING_HEADERS}"

jq -n --arg reason "$REASON" '{decision: "block", reason: $reason}'

exit 0
