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

---

## 2026-06-22: F19 手動トグル不動作の根本原因調査と修正

### 問題

F19 キーによる BT プロファイル手動トグルが動作しなくなっていた.

### 根本原因 1: WirePlumber による自動プロファイル切り替え

WirePlumber 0.4.17（Ubuntu）の `policy.lua.d/10-default-policy.lua` が `media-role.use-headset-profile = true` をデフォルト設定している.
GNOME Settings の「Peak detect」モニターなど, 入力ストリームが検出されると WirePlumber が自動的に BT プロファイルを HSP/HFP に切り替え, `pactl set-card-profile` による手動変更を上書きする.

**修正**: `~/.config/wireplumber/policy.lua.d/11-disable-autoswitch.lua` を作成し `media-role.use-headset-profile = false` を設定. ユーザー設定は番号が大きいファイルで上書きされる.

### 根本原因 2: xmodmap キーシムマッピングのリセット

WirePlumber の再起動, fcitx5 の初期化, その他の入力システム変更によって xmodmap のキーシムマッピング（`keycode 197 = F19`）がリセットされる.
マッピングが消えると GNOME カスタムショートカットが F19 を検出できなくなる.

**修正**: xmodmap + GNOME カスタムショートカットから xbindkeys へ移行.
xbindkeys は生の X11 キーコード（`c:197` 構文）に直接バインドするため, キーシム層をバイパスし xmodmap リセットの影響を受けない.

### 新規作成ファイル

- `~/.xbindkeysrc`: F19（キーコード 197）→ `toggle-bt-profile.sh`
- `~/.config/autostart/xbindkeys.desktop`: ログイン時の xbindkeys 自動起動
- `~/.config/wireplumber/policy.lua.d/11-disable-autoswitch.lua`: WirePlumber 自動プロファイル切り替え無効化

### 削除ファイル

- `~/.config/autostart/xmodmap-f19.desktop`: 不要になったため削除
- GNOME カスタムショートカット（custom0）: `gsettings` 経由で削除

### その他の知見

- WirePlumber の再起動は PipeWire オーディオグラフをリセットする. Flatpak アプリ（tidal-hifi 等）のアクティブストリームが切断されるため, アプリの再読み込みが必要になる.

---

## 2026-06-22: HSP/HFP → A2DP 切り替え不動作の修正

### 問題

HSP/HFP から A2DP への切り替え後, BT ヘッドセットから音が出ない.
PipeWire は A2DP シンクを RUNNING と報告し pw-top でデータフローも確認できるが, デバイスは無音.

### 根本原因

BlueZ が HSP/HFP から A2DP へ直接切り替えたとき, A2DP トランスポート（L2CAP チャンネル）の再確立に失敗する.
PipeWire 側のシンクは RUNNING 状態になるが, BT トランスポート層では音声データが実際にはデバイスに届いていない.

### 修正: toggle-bt-profile.sh の大幅改修

`~/workspace/dotfiles/toggle-bt-profile.sh` を書き直し, HSP/HFP → A2DP 切り替えパスに以下の処理を追加した.

**1. off プロファイルを経由した二段階切り替え（HSP/HFP → off → A2DP）**

直接切り替えではなく, 一度 `off` プロファイルに設定してからA2DPに切り替えることで BlueZ にクリーンなトランスポートの切断・再確立を強制する.

**2. シンク準備完了のポーリング**

A2DP プロファイル設定後, 2ch 48kHz シンクが PipeWire に現れるまで最大 4 秒間ポーリングして待機する. シンクが出現前に次の処理に進むと, sink-input の移行先が存在しないためエラーになる.

**3. sink-input の移行**

既存のすべてのストリーム（sink-input）を新しい BT シンクに `pactl move-sink-input` で移動する. プロファイル切り替え後, ストリームはデフォルトシンク（スピーカー等）に残留していることがあるため必要.

**4. メディアキーによる再トリガー（XF86AudioPause → XF86AudioPlay）**

Flatpak Chromium（tidal-hifi）は MPRIS をセッションバスに公開しないため, `pactl move-sink-input` でストリームを移動しても音声コンテキストが新シンクを認識しないことがある.
`xdotool key XF86AudioPause` → `xdotool key XF86AudioPlay` でメディアキーを模擬することで, Chromium/Flatpak の音声コンテキストを再トリガーする.

**5. `set -e` の削除**

スクリプト先頭の `set -e` を削除した. シンクが存在しない場合の `pactl move-sink-input` など, 非致命的な失敗でスクリプト全体が中断されることを防ぐ.

### WirePlumber 自動切り替えの無効化

2026-06-22 セッションで新たに判明: WirePlumber 0.4.17 の `policy-bluetooth.lua` は, `media.role=Communication` を持つ入力ストリームが存在するか, Chromium 等のハードコードされたアプリが実行中の場合に BT プロファイルを自動的に HSP/HFP に戻す.
`~/.config/wireplumber/policy.lua.d/11-disable-autoswitch.lua` で `media-role.use-headset-profile = false` を設定することで抑制済み（2026-06-22 の調査でも引き続き有効と確認）.

### voice-input スクリプトの修正

`~/workspace/dotfiles/voice-input/voice-input.py` に 2 件の修正を加えた.

**言語検出の追加**

faster-whisper の `transcribe()` に `language` パラメータを追加. fcitx5-remote の現在入力メソッド（`fcitx5-remote -n`）を参照し, 日本語 IME がアクティブなら `"ja"`, それ以外なら `"en"` を動的に設定する.
言語パラメータなしでは Whisper が短い発話を誤って他言語と判定することがある.

**孤立 parecord プロセスの修正**

SIGTERM/SIGINT シグナルハンドラ `cleanup_recording()` を追加した. 終了シグナル受信時に `parecord` サブプロセスを確実に終了させる. これまでは voice-input.py が強制終了されると `parecord` が孤立プロセスとして残留し, マイク入力を占有し続けていた.

### chocofi BT TX パワーの増加

`~/workspace/chocofi-bt/config/corne.conf` に `CONFIG_BT_CTLR_TX_PWR_PLUS_8=y` を追加し, nRF52840 の BLE TX パワーを 0 dBm（デフォルト）から +8 dBm（最大値）に引き上げた. ファームウェアビルドをトリガーするためにリポジトリへプッシュ済み.
nRF52840 では +8 dBm と 0 dBm の消費電力差は無視できる.

### 知見

- BlueZ は HSP/HFP から A2DP への直接切り替えで A2DP トランスポート確立に失敗する. `off` 経由の二段階切り替えでトランスポートの完全な切断・再確立が保証される.
- PipeWire はシンクを RUNNING 状態で報告し pw-top でもデータフローが確認できるが, BT トランスポートが実際には音声をデバイスに届けていないことがある.
- xbindkeys の `c:NNN` 構文は生の X11 キーコードにバインドするため, キーシム層をバイパスし xmodmap のリセットの影響を受けない（前回セッションで確認済みの修正が引き続き有効）.
- Flatpak Chromium（tidal-hifi）は MPRIS をセッションバスに公開しないため, パイプライン経由のストリーム制御ができない.
- nRF52840 の BLE TX パワーデフォルトは 0 dBm. +8 dBm が上限で消費電力増加は無視できる.

---

## 2026-06-23: voice-input 言語切り替え確認と BT キーボード切断時の再接続修正

### 言語切り替えの動作確認

`fcitx5-remote -n` が mozc アクティブ時に `mozc` を、英語入力時に `keyboard-us` を返すことを確認した。
faster-whisper の `language` パラメータに正しく `"ja"` / `"en"` が渡されていることも確認済み。

**補足: 「英語入力なのに日本語認識」問題の原因**

以前報告した「英語入力しているのに日本語として認識される」問題は、mozc がアルファベット入力モード（トレイアイコンが [A] を表示）になっていた状態が原因と考えられる。
この状態では fcitx5 の入力メソッドとして mozc がアクティブなままであるため、`fcitx5-remote -n` は `mozc` を返し、voice-input.py は `language="ja"` を設定する。
fcitx5 レベルの入力メソッド（mozc が選択されているか）と mozc 内部のモード（アルファベット入力か日本語入力か）は別であり、voice-input.py は前者のみを参照する。

### BT キーボード切断時のデーモン終了問題の修正

**問題**

voice-input デーモンが、BT キーボード（chocofi）の切断時に終了していた。

**根本原因**

python-evdev はデバイスが消えたとき OSError を発生させるが、切断に対する組み込みの再接続機能を持たない（[github issue #64](https://github.com/gvalkov/python-evdev/issues/64)）。
イベントループがその OSError をキャッチせずに終了していた。

**修正内容**

`~/workspace/dotfiles/voice-input/voice-input.py` に以下の変更を加えた。

- `wait_for_keyboard()` 関数を追加: デバイスファイルが `/dev/input/` に現れるまでポーリングし、接続を待機する。
- イベントループを `try/except OSError` で囲み、切断時に `wait_for_keyboard()` を呼び出して再接続するループに変更した。

### 知見

- python-evdev はデバイス切断時に OSError を発生させる。`OSError` をキャッチして再試行するのが標準的なアプローチ（pyudev によるカーネルイベント監視は過剰設計）。
- `fcitx5-remote -n` が返す値は fcitx5 レベルの入力メソッド名であり、mozc 内部のアルファベット/日本語モードは反映されない。
