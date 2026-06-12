# Skill Aliases Log

## 2026-06-12: スキル短縮名称 (エイリアス) の導入

### 背景

長い名前のスキル (`fault-tree-debug`, `empirical-prompt-tuning`) を短縮名で呼びたい.

### 調査結果

- **シンボリックリンク不可**: `ln -s fault-tree-debug fta` ではスキルシステムに認識されない. スキルの解決はディレクトリ名の symlink 追跡を行わない
- **ラッパースキル方式**: `skills/<alias>/SKILL.md` に薄いラッパー (frontmatter + 転送指示) を作成すれば動作する

### 作成したエイリアス

| エイリアス | 本体スキル | パス |
|---|---|---|
| `/fta` | `/fault-tree-debug` | `skills/fta/SKILL.md` |
| `/ept` | `/empirical-prompt-tuning` | `skills/ept/SKILL.md` |

### ラッパースキルの構造

```markdown
---
name: fta
description: "Alias for /fault-tree-debug. ..."
---

This is an alias. Run `/fault-tree-debug` with all arguments forwarded.
```

### 注意事項

- スキル一覧はセッション開始時に読み込まれるため, 作成後は新セッションで有効になる
- ラッパースキルは一覧に独立エントリとして表示される (description で alias であることを明示)
