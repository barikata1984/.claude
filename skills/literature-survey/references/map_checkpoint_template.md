# Map Checkpoint テンプレート

Phase 2 末尾でユーザーに提示する完成形テンプレート。
SKILL.md の Phase 2 → Map Checkpoint 節から参照される。

以下をそのまま埋めて提示する：

```markdown
## Map Checkpoint — レビューお願いします

### Map Result (N papers, target: M)

#### By temporal tier
- Tier 1 (recent, last 2-3 yrs): N papers
- Tier 2 (established, 3-10 yrs): N papers
- Tier 3 (foundational, ~10+ yrs): N papers

#### By initial concept clusters
| # | Cluster | Count | Top venue | Sample papers (3 most cited) |
|---|---------|-------|-----------|------------------------------|
| 1 | [name]  | N     | [venue]   | [Author+ Year]; [...]; [...] |
| 2 | ...     | ...   | ...       | ...                          |

#### Coverage
- Search angles used: N — [list angles in 1 line]
- Snowballing: seed N + forward/backward 1-hop, total N papers
- Duplicates removed: N
- Papers excluded by I/E criteria: N — [list reasons]

### 確認事項（回答お願いします）

| # | 質問 | 回答候補 |
|---|------|---------|
| 1 | 既知の論文で **漏れているもの** はありますか？ | あれば: [タイトル / arXiv ID / DOI] / なし |
| 2 | **除外すべき方向 / クラスタ** はありますか？ | あれば: [cluster # or トピック] / なし |
| 3 | **I/E criteria 調整** が必要ですか？ | あれば: [追加 inclusion / 追加 exclusion] / なし |
| 4 | **採録規模** を調整しますか？ | 現状 N で進む / 増やす（target M' へ） / 減らす（target M' へ） |

承認 = 上記回答済みで「進めて」と一言。差し戻し = 質問への回答 + 「再 map」と一言。
```

## 提示後の挙動

- 回答待ちの間 Phase 3 には進まない
- 差し戻された場合は Map を更新して再提示
- auto-execution mode 時はテンプレを完成形 markdown で生成し、Methodology → Map に
  「(automated run: presented but not confirmed)」注記付きで inline 埋め込み（SKILL.md
  「Auto-execution Mode」節参照）
