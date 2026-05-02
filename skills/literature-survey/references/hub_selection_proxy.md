# Hub Selection: Citation Proxy 判定

SKILL.md Phase 3 → Hub Selection 基準の B（カテゴリ橋渡し性 + 影響力）における、
**citation 数が取得できない環境**（Semantic Scholar MCP / OpenAlex script 不通）
での代替判定手順。通常は Semantic Scholar / OpenAlex の citation count を直接使うが、
これらが利用不可の場合のみ本ドキュメントを読む。

## 3 proxy 軸

以下を **High / Mid / Low** で評価する：

### (i) venue tier

| 区分 | Venue 例 |
|------|---------|
| High | NeurIPS / ICML / ICLR / CVPR / ICCV / ECCV / SIGGRAPH / RSS / CoRL / IJRR / RA-L / T-RO |
| Mid  | ICRA / IROS / AAAI / Humanoids / WAFR / L4DC |
| Low  | Workshop / preprint only |

### (ii) WebSearch hit 数

論文タイトル + 第一著者名で WebSearch し、**論文本体以外**の関連言及（解説 blog /
re-implementation / 引用フォーラム / video summary 等）の件数：

| 区分 | 件数 |
|------|-----|
| High | ≥ 5 件 |
| Mid  | 1-4 件 |
| Low  | 0 件 |

### (iii) 本 survey 内被引用頻度

採録した他論文の references で当該論文に言及している本数：

| 区分 | 本数 |
|------|-----|
| High | ≥ 3 本 |
| Mid  | 1-2 本 |
| Low  | なし |

## 判定ルール

3 軸中 **2 軸以上が High** なら「上位 1/3 相当」と認定し、Hub 候補に含めて良い。

## Methodology への記録

各 hub の 3 軸スコアを明記し、「citation proxy used」と注記する。

例：
```
Hub-1: (High, High, Mid) — citation proxy used (S2 MCP unreachable)
Hub-2: (High, Mid, High) — citation proxy used
```
