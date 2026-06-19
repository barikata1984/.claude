# Log: Bluetooth プロファイル切り替え (ZMK キーボード F19 キー)

## 2026-06-19: A2DP / HSP・HFP トグルスクリプト + GNOME ショートカット設定

### 目的

Bluetooth ヘッドセットの A2DP（高音質）と HSP/HFP（マイク付きヘッドセット）プロファイルを ZMK キーボードのキー一つで切り替えられるようにする.

### 成果物

- `~/workspace/dotfiles/toggle-bt-profile.sh`: `pactl` を使って現在アクティブなプロファイルを確認し, A2DP と HSP/HFP を交互に切り替えるスクリプト. プロファイル名の末尾コーデックバリアント（`a2dp-sink-sbc`, `a2dp-sink-aac` 等）に対応するため, 前方一致（`a2dp-sink*` / `headset-head-unit*`）でマッチングする.
- `~/workspace/dotfiles/bt-profile-toggle.md`: 設定手順ドキュメント.
- `~/.config/autostart/xmodmap-f19.desktop`: ログイン時に `xmodmap` でキーコード 197 を F19 キーシムにマップする autostart エントリ. 再起動後も設定が永続する.

### XKB キーコード調査

F13–F24 の XKB キーコードと XF86 キーシムのマッピングを調査した結果:

| キー | キーコード | 備考 |
|------|-----------|------|
| F13 | 191 | XF86Tools |
| F14 | 192 | XF86Launch5 |
| F15 | 193 | XF86Launch6 |
| F16 | 194 | XF86Launch7 |
| F17 | 195 | XF86Launch8 |
| F18 | 196 | XF86Launch9 |
| **F19** | **197** | **NoSymbol（安全）** |
| F20 | 198 | XF86AudioMicMute |
| F21 | 199 | XF86TouchpadToggle |
| F22 | 200 | XF86TouchpadOn |
| F23 | 201 | XF86TouchpadOff |
| **F24** | **202** | **NoSymbol（安全）** |

F19（キーコード 197）と F24（キーコード 202）が NoSymbol でシステムに横取りされないと確認. F23 を最初に試みたが XF86TouchpadOff として解釈されタッチパッドがオフになったため F19 に変更.

### GNOME ショートカット設定

`Settings > Keyboard > Custom Shortcuts` で F19 キーに `~/workspace/dotfiles/toggle-bt-profile.sh` を割り当て. ZMK キーボードでは F19 レイヤーキーをバインド済み.

### 技術的ポイント

- `pactl list cards` でカード名とプロファイルを取得し, `pactl set-card-profile` で切り替える.
- コーデックによってプロファイル名のサフィックスが変わるため（`a2dp-sink-sbc` / `a2dp-sink-aac` 等）, 完全一致ではなく前方一致でプロファイルを判定する必要がある.
- `xmodmap -e "keycode 197 = F19"` を autostart に仕込むことで, ログイン後に GNOME が XKB マップを上書きしても F19 キーシムが復元される.
