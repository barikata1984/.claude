---
name: request-source
description: >
  Analyzes a specified response and generates a knowledge source block that
  classifies the information used into three categories: internal knowledge,
  external knowledge, and observations. Use when the user asks "what are your
  sources?", "show me the basis for this", or when a knowledge source block
  is missing from a response.
---

Analyze the response specified in `$ARGUMENTS` and generate a knowledge source block.

Place the block at the end of the response, separated from the main text by a horizontal rule (`---`).

## Output format

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
```

## Category definitions

- **内部知識**: Items derived from training data that have not been verified via WebSearch/WebFetch in this session.
- **外部知識**: Information retrieved via WebSearch/WebFetch in this session. Include URL and a brief summary. If nothing was retrieved, write "なし".
- **観測事実**: Logs, code, error output, or execution results directly confirmed in this session. A third category distinct from both internal and external knowledge.

## Notes

- Always include all three categories, even if a category has no entries.
