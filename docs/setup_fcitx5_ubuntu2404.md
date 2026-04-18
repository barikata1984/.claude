# Ubuntu 24.04 + Ghostty で日本語入力 (fcitx5-mozc) を有効にする

## 前提

- Ubuntu 24.04 LTS (X11 セッション)
- Ghostty 1.1 以降（GTK アプリのため `fcitx5-frontend-gtk3` が必須）

## 手順

### 1. ibus-mozc の削除（競合回避）

Ubuntu 24.04 のデフォルトでは `ibus-mozc` が入っており、`fcitx5-mozc` と共存すると `mozc_server` を取り合って
「Conversion engine is not responding」エラーの原因となる。また `ibus-mozc-gnome-initial-setup.sh` が GNOME の
dconf 入力ソースに `('ibus', 'mozc-jp')` を書き込み、状態を複雑にするので先に purge する。

```bash
sudo apt remove --purge -y ibus-mozc
```

### 2. fcitx5-mozc のインストール

```bash
sudo apt update
sudo apt install -y fcitx5-mozc
```

`fcitx5` 本体、`fcitx5-frontend-gtk3`（Ghostty に必要）、Mozc がまとめて入る。

### 3. im-config で fcitx5 を既定の IM に設定

```bash
im-config -n fcitx5
```

`~/.xinputrc` に `run_im fcitx5` が書き込まれる。

### 4. XDG autostart で fcitx5 を自動起動

`im-config` だけでは fcitx5 デーモンがログイン時に起動しないケースがある。
パッケージ同梱の `.desktop` ファイルを `~/.config/autostart/` にコピーすることで確実に自動起動させる（[fcitx5 公式 wiki 推奨](https://www.fcitx-im.org/wiki/Setup_Fcitx_5)）。

```bash
mkdir -p ~/.config/autostart
cp /usr/share/applications/org.fcitx.Fcitx5.desktop ~/.config/autostart/
```

### 5. 環境変数の設定

`~/.xprofile` に以下を記述する。値は `fcitx5` ではなく **`fcitx`** が正しい。

```bash
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
```

> **注意**: `.bashrc` / `.zshrc` 等に `GTK_IM_MODULE=ibus` のような記述が残っていると上書きされて動かない。必ず確認し、あれば削除する。

### 6. fcitx5 のプロファイルに Mozc を追加

`~/.config/fcitx5/profile` を以下の内容にする。

```ini
[Groups/0]
Name=Default
Default Layout=us
DefaultIM=mozc

[Groups/0/Items/0]
Name=keyboard-us
Layout=

[Groups/0/Items/1]
Name=mozc
Layout=

[GroupOrder]
0=Default
```

GUI で設定する場合は `fcitx5-configtool` を起動し、入力メソッドに Mozc を追加する。

### 7. Ghostty の合字対策（任意）

`~/.config/ghostty/config` に追記する。

```
font-feature = -dlig
```

これで「ます」が「〼」に化ける問題を防げる。

### 8. ログアウト → ログイン

再ログインで fcitx5 デーモンが自動起動する。**Ctrl+Space** で英字 / 日本語を切り替えられる。

## ワンライナー（コピペ用）

```bash
# Remove conflicting ibus-mozc
sudo apt remove --purge -y ibus-mozc

# Install
sudo apt update && sudo apt install -y fcitx5-mozc

# Set fcitx5 as default IM
im-config -n fcitx5

# XDG autostart (ensures fcitx5 starts on login)
mkdir -p ~/.config/autostart
cp /usr/share/applications/org.fcitx.Fcitx5.desktop ~/.config/autostart/

# Environment variables
cat >> ~/.xprofile << 'EOF'
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
EOF

# Add Mozc to fcitx5 profile
mkdir -p ~/.config/fcitx5
cat > ~/.config/fcitx5/profile << 'EOF'
[Groups/0]
Name=Default
Default Layout=us
DefaultIM=mozc

[Groups/0/Items/0]
Name=keyboard-us
Layout=

[Groups/0/Items/1]
Name=mozc
Layout=

[GroupOrder]
0=Default
EOF

# Ghostty ligature fix (optional)
mkdir -p ~/.config/ghostty
grep -q 'font-feature' ~/.config/ghostty/config 2>/dev/null || echo 'font-feature = -dlig' >> ~/.config/ghostty/config

echo "Done. Please logout and login again."
```

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| Ghostty だけ日本語入力できない | `fcitx5-frontend-gtk3` が未インストール | `sudo apt install fcitx5-frontend-gtk3` |
| どのアプリでも日本語入力できない | `im-config` が ibus のまま | `im-config -n fcitx5` → 再ログイン |
| 再ログインしても fcitx5 が起動しない | XDG autostart 未設定 | `cp /usr/share/applications/org.fcitx.Fcitx5.desktop ~/.config/autostart/` |
| 環境変数は正しいのに動かない | `.bashrc` / `.zshrc` で ibus に上書きされている | 該当行を削除 |
| fcitx5 は動いているが Mozc に切り替わらない | プロファイルに Mozc が未登録 | `fcitx5-configtool` で Mozc を追加 |
| 「ます」が「〼」になる | Ghostty の合字 (ligature) | `font-feature = -dlig` を設定 |
| 「Conversion engine is not responding」のポップアップ | `ibus-mozc` と `fcitx5-mozc` が `mozc_server` を取り合っている | `sudo apt remove --purge ibus-mozc` → 再ログイン |
| GNOME の入力ソースに ibus-mozc-jp が勝手に入る | `ibus-mozc-gnome-initial-setup.sh` が走った | `ibus-mozc` を purge するか `dconf reset /org/gnome/desktop/input-sources/sources` |

## 参考

- [Arch LinuxでGhostty使ったら日本語が打てなかった - Qiita](https://qiita.com/Usuyuki/items/8f8cb3c43ee0080d1e4f)
- [Ubuntu 24.04 日本語入力環境の整備（2025年度版）](https://www.aise.ics.saitama-u.ac.jp/~gotoh/InputMethodOnUbuntu2404In2025.html)
- [Ghostty 1.1.0 Release Notes](https://ghostty.org/docs/install/release-notes/1-1-0)
- [Setup Fcitx 5 - Fcitx Wiki（公式）](https://www.fcitx-im.org/wiki/Setup_Fcitx_5)
- [Ubuntu 24.04 LTS で Fcitx5 を自動起動するようにした](https://zakkannberg.blogspot.com/2025/11/ubuntu-2404-lts-fcitx5.html)
