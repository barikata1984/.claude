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

paplay /usr/share/sounds/freedesktop/stereo/complete.oga &
