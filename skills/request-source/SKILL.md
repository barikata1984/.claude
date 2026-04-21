---
name: request-source
description: >
  Generates a [知識ソース] knowledge source block for a specified Claude response,
  classifying information as internal knowledge (training data), external knowledge
  (retrieved via WebSearch/WebFetch), or observations (session logs, code, errors).
  Always use this skill when: the user asks about sources, basis, or credibility of
  a Claude response in any phrasing — including Japanese (「ソースは？」「内部知識？」
  「根拠は？」「検索した？」「WebSearch した？」「ソースブロックがない」「知識ソースが欠けている」);
  the user calls /request-source explicitly; a previous response is missing its
  [知識ソース] block and needs retroactive annotation; or the user questions whether
  information came from training data vs. actual web retrieval.
---

Analyze the response specified in `$ARGUMENTS` and generate a knowledge source block.

`$ARGUMENTS` can be a contextual reference such as "直前の回答" or "この回答" (resolve from conversation history), or literal response text.

## Output format

The complete source block below is your entire response — no text before it, no text after it, and do not reproduce the original response text. All three sections (内部知識, 外部知識, 観測事実) must always be present; write "なし" for any section with no entries.

```
---

[知識ソース]
内部知識：
- <item from training data>

外部知識：
- <URL> — <summary of retrieved information>
- なし

観測事実：
- <logs, code, error output, or execution results directly confirmed in this session>
- なし
```

## Category definitions

- **内部知識**: Items derived from training data that have not been verified via WebSearch/WebFetch in this session. Write each item as a concise factual statement; do not add meta-annotations like "〜由来の知識" or "training data より".
- **外部知識**: Information retrieved via WebSearch/WebFetch in this session. Include URL and a brief summary. If nothing was retrieved, write "なし".
- **観測事実**: Logs, code, error output, or execution results directly confirmed in this session. A third category distinct from both internal and external knowledge. If nothing was observed, write "なし".
