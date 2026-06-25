# ~/.claude/ ディレクトリ整理ログ

## 2026-06-25: 重複ファイル削除と empirical-prompt-tuning APM 移行

### 背景

`~/.claude/` 内に未追跡の重複ディレクトリが複数蓄積していた。
また、ローカルで独自管理していた `skills/empirical-prompt-tuning/` を upstream (mizchi/skills) 版に置き換えた。

### 実施内容

1. **重複削除**
   - `skills/empirical-prompt-tuning.bak/` — ローカル版と同一内容の未追跡コピー。削除
   - `plugins/marketplaces/karpathy-skills.bak/` — root 所有のバックアップ。sudo で削除
   - `plugins/cache/karpathy-skills/` — キャッシュディレクトリ。削除

2. **empirical-prompt-tuning APM 移行**
   - ローカル `skills/empirical-prompt-tuning/` を削除（git 管理 2 コミット、独自作成）
   - APM (`apm install -g mizchi/skills/meta/empirical-prompt-tuning`) で upstream 版をインストール

### 判明した事実

- karpathy-skills プラグインのコピーが本体・.bak・cache の 3 つ存在していた。本体のみ残存
- ローカル empirical-prompt-tuning は .bak と同一内容で、プラグインマーケットプレイスからではなく独自作成
- mizchi/skills は Claude Code のプラグインシステムではなく APM (Agent Package Manager) で配布
- APM v0.20.0 がインストール済み（最新は v0.21.0）

### 残存 .bak ファイル（意図的に残置）

- `plugins/marketplaces/anthropic-agent-skills.bak/`
- `plugins/marketplaces/claude-plugins-official.bak/`
- `rules/japanese-writing.md.bak`
- `rules/japanese_style.md.bak`
- `settings.json.bak`
