#!/bin/bash
# stop-taxonomy-check.sh
#
# Mode: blocking
#
# 応答に taxonomy / enumerative 構造が含まれているにもかかわらず、
# このターンで検証アクション (WebSearch/WebFetch/Agent) が実行されておらず、
# かつ自前合成の disclaimer もない場合に、応答を block して再生成を強制する。
#
# stop_hook_active=true の場合は無限ループ防止のため通過させる。

set -euo pipefail

LOG_FILE="$HOME/.claude/hooks/taxonomy-warn.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Hook input は stdin で渡される
INPUT=$(cat)
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || echo "false")

# 既に Stop hook 経由で再生成中 → 無限ループ防止
if [ "$STOP_ACTIVE" = "true" ]; then
    exit 0
fi

# transcript が取得できなければ何もしない
if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
    exit 0
fi

# このターンの境界を判定し以降のエントリだけを切り出す
# (tool_result type=user は除外、真のユーザー入力のみを境界として使う)
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

# このターンで使われたツール一覧
TOOLS=$(echo "$TURN_DATA" | jq -r '
  map(select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name)
  | unique
  | .[]
' 2>/dev/null || echo "")

# このターンの最後の assistant の text 応答
RESPONSE=$(echo "$TURN_DATA" | jq -r '
  map(select(.type == "assistant"))
  | (.[-1].message.content // [])
  | map(select(.type == "text") | .text)
  | join("\n")
' 2>/dev/null || echo "")

# 応答が空 (ツールのみのターンなど) は対象外
if [ -z "$RESPONSE" ]; then
    exit 0
fi

# 検証アクションの有無
# Agent は subagent transcript で WebSearch/WebFetch を実行している可能性があるため
# 検証アクションとしてカウントする
VERIFIED=0
if echo "$TOOLS" | grep -qE "^(WebSearch|WebFetch|Agent)$"; then
    VERIFIED=1
fi

# taxonomy 構造インジケーター（複数の候補を OR で評価）
# grep -c は 0 マッチ時に exit 1 を返すので || true で吸収

# (a) 数量詞 + 助数詞 (「N 個の」「3 つの」「4 種類」等)
QUANTIFIER=$(echo "$RESPONSE" \
    | grep -cE "[0-9一二三四五六七八九十]+[[:space:]]*(個の|種類|つの|軸|分類|タイプ)" \
    || true)

# (b) 英字ラベル列挙 (「(A)」「(B)」… が 3 つ以上)
LETTER_LABELS=$(echo "$RESPONSE" \
    | grep -oE "\([A-Z]\)" \
    | sort -u \
    | wc -l)

# (c) 比較表構造 (3 行以上の | col | col | パターン)
TABLE_ROWS=$(echo "$RESPONSE" \
    | grep -cE "^\|[^|]+\|[^|]+\|" \
    || true)

# 構造インジケーターが何らかの形で立っているか
STRUCTURE=0
if [ "$QUANTIFIER" -gt 0 ] || [ "$LETTER_LABELS" -ge 3 ] || [ "$TABLE_ROWS" -ge 3 ]; then
    STRUCTURE=1
fi

# taxonomic な名詞の存在
NOUN=$(echo "$RESPONSE" \
    | grep -cE "(条件|要因|原因|カテゴリ|軸|分類|タイプ|要素|レベル|段階|フェーズ|経路)" \
    || true)

# 自前合成 disclaimer の存在
DISCLAIMER=$(echo "$RESPONSE" \
    | grep -cE "(自前の再構成|私の再構成|文献的裏付け未確認|私の即興|standard taxonomy ではない|私の独自|未確認の|私の創作)" \
    || true)

# トリガー条件: 構造インジケーター + taxonomic 名詞、disclaimer なし、検証なし
if [ "$STRUCTURE" -eq 1 ] && [ "$NOUN" -gt 0 ] && [ "$DISCLAIMER" -eq 0 ] && [ "$VERIFIED" -eq 0 ]; then
    {
        echo "=================================================="
        echo "Timestamp: $(date -Iseconds)"
        echo "Session: $SESSION_ID"
        echo "Tools used in turn: $(echo "$TOOLS" | tr '\n' ' ')"
        echo "Pattern matches: quantifier=$QUANTIFIER, letter_labels=$LETTER_LABELS, table_rows=$TABLE_ROWS, noun=$NOUN, disclaimer=$DISCLAIMER, verified=$VERIFIED"
        echo "--- Response excerpt (first 800 chars) ---"
        echo "$RESPONSE" | head -c 800
        echo ""
        echo "--- End ---"
    } >> "$LOG_FILE"

    REASON="taxonomy ハルシネーション疑い：応答に分類構造（数量詞・ラベル・表）と taxonomic 名詞（条件/要因/原因/カテゴリ/軸/分類/タイプ/要素/レベル/段階/フェーズ/経路）が含まれていますが、検証アクション（WebSearch/WebFetch/Agent）が未実行で、自前合成 disclaimer もありません。WebSearch / WebFetch / Agent で裏付けを取るか、自前再構成である旨を明示（『自前の再構成』『文献的裏付け未確認』『私の独自』等）して再生成してください。"

    jq -n --arg reason "$REASON" '{decision: "block", reason: $reason}'
fi

exit 0
