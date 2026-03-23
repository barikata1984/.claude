# Claude Code (VSCode拡張) — Ubuntu 通知セットアップガイド

## 前提

- OS: Ubuntu (GNOME Desktop)
- Claude Code VSCode拡張がインストール済みであること
- **既知の制限:** `Notification` hookの `permission_prompt` / `idle_prompt` マッチャーは VSCode拡張では発火しない（未修正バグ）。本ガイドでは `Stop` hookを代替として使用する。

---

## アプローチ 1 — VSCode内通知（Claude Code Notifier拡張）

`/tmp/claude-notify` というファイルへの書き込みを監視し、VSCode内トースト通知を表示する拡張を使う方法。

### Step 1: 拡張インストール

```bash
code --install-extension erdemgiray.claude-code-notifier
```

またはVSCode Marketplace で "Claude Code Notifier" を検索してインストール。

### Step 2: 設定ファイルを編集

`~/.claude/settings.local.json` を開き（なければ新規作成）、以下を追記：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Claude is waiting for your input' > /tmp/claude-notify"
          }
        ]
      }
    ]
  }
}
```

### Step 3: 動作確認

VSCodeのコマンドパレット (`Ctrl+Shift+P`) で以下を実行：

```
Claude Code: Send Test Notification
```

VSCode右下にトースト通知が表示されれば成功。

### 仕組み

```
Claude Code (Stop hook)
    ↓
echo '...' > /tmp/claude-notify   ← ファイルに書き込む
    ↓
Claude Code Notifier 拡張          ← ファイルを監視
    ↓
VSCode トースト通知
```

### 注意点

- VSCodeにフォーカスが当たっていないと通知が見えない
- 別のウィンドウで作業中は気づきにくい
- OS全体への通知ではないため、離席・アプリ切り替え中には届かない

---

## アプローチ 2 — OS通知（notify-send）

Ubuntuのデスクトップ通知システムに直接通知を送る方法。VSCodeの外で作業していても通知が届く。

### Step 1: notify-send をインストール

```bash
sudo apt install libnotify-bin
```

インストール確認：

```bash
notify-send 'テスト' 'notify-send が動作しています'
```

デスクトップ右上に通知が出れば OK。

### Step 2: フックスクリプトを作成

CCのhookはTTYなしのデタッチドプロセスとして実行されるため、`DBUS_SESSION_BUS_ADDRESS` を明示的に設定しないと `notify-send` が失敗する。ラッパースクリプトとして作成する。

```bash
mkdir -p ~/.claude/hooks
```

```bash
cat > ~/.claude/hooks/notify.sh << 'EOF'
#!/bin/bash

# DBUSセッションバスを明示的に指定（hook実行環境はTTYなしのため必須）
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

TITLE="${1:-Claude Code}"
MESSAGE="${2:-Claude is waiting for your input}"
URGENCY="${3:-normal}"   # low / normal / critical

notify-send "$TITLE" "$MESSAGE" \
    --urgency="$URGENCY" \
    --icon=dialog-information \
    --app-name="Claude Code"
EOF
```

```bash
chmod +x ~/.claude/hooks/notify.sh
```

動作確認：

```bash
~/.claude/hooks/notify.sh 'Claude Code' 'テスト通知'
```

### Step 3: 設定ファイルを編集

`~/.claude/settings.local.json` を開き、以下を追記：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/notify.sh 'Claude Code' 'Claude is waiting for your input'"
          }
        ]
      }
    ]
  }
}
```

### Step 4: 動作確認

CCに何らかのタスクを依頼し、完了後にデスクトップ通知が出ることを確認する。

### 仕組み

```
Claude Code (Stop hook)
    ↓
~/.claude/hooks/notify.sh
    ↓
DBUS_SESSION_BUS_ADDRESS を設定
    ↓
notify-send → GNOME 通知デーモン
    ↓
デスクトップ通知（画面右上）
```

### 応用: 質問かどうかで通知を変える

`Stop` hookは「完了」と「質問待ち」を区別しないが、最後のメッセージ末尾で簡易判定できる。

`~/.claude/hooks/notify_smart.sh`:

```bash
#!/bin/bash

export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

LAST_MSG="${CLAUDE_LAST_ASSISTANT_MESSAGE:-}"

if echo "$LAST_MSG" | grep -qE '\?[[:space:]]*$'; then
    # 質問で終わっている場合 → critical（消えずに残る）
    notify-send 'Claude Code ❓' 'Claude is asking a question!' \
        --urgency=critical \
        --icon=dialog-question \
        --app-name="Claude Code"
else
    # それ以外 → normal
    notify-send 'Claude Code ✅' 'Task completed' \
        --urgency=normal \
        --icon=dialog-information \
        --app-name="Claude Code"
fi
```

```bash
chmod +x ~/.claude/hooks/notify_smart.sh
```

settings.json の `command` を差し替え：

```json
"command": "~/.claude/hooks/notify_smart.sh"
```

---

## 両方を組み合わせる

VSCode内通知とOS通知を同時に発火させることもできる。

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Claude is waiting' > /tmp/claude-notify && ~/.claude/hooks/notify.sh 'Claude Code' 'Claude is waiting for your input'"
          }
        ]
      }
    ]
  }
}
```

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| `notify-send` がスクリプト単体では動くがhookから動かない | DBUSアドレス未設定 | ラッパースクリプト内で `DBUS_SESSION_BUS_ADDRESS` を明示設定 |
| VSCode通知が出ない | 拡張が未アクティブ | 拡張パネルで有効化を確認 / テストコマンドを実行 |
| `Notification` hookが発火しない | VSCode拡張の既知バグ | `Stop` hookを代替として使用 |
| hookが実行されているか不明 | ログがない | `command` に `>> /tmp/cc-hook.log 2>&1` を追記してログ確認 |
