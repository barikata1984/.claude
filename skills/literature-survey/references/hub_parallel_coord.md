# Hub Deep Read: 並列実行の Wikilink Coordination

SKILL.md Phase 3 → Hub Deep Read で並列 dispatch を選んだ際の補正手順。

## 問題

並列で `/paper-summary` を起動した場合、各実行は Step 4「既存ノート読み込み」の
時点で他のハブノートがまだ存在しないため、**ハブ間の相互 wikilink が欠落**する。

## 戦略

### (i) 逐次実行

1 hub ずつ完了させる。遅いが coordination 不要で確実。

### (ii) 並列 + 補完 pass（推奨）

並列実行後、Phase 3 末尾で全 hub notes を 1 巡再 scan し、相互 wikilink を Edit で
補完する。各 note の Summary 本文中で他 hub 論文への言及があれば
`[[papers/{citekey}/{slug}|Author+ Year]]` 形式に置換する。

通常は (ii) が時間効率良い。

## 補正不要なパターン

非ハブ → ハブ方向の wikilink は対象 note が存在するため、逐次・並列いずれでも
問題なし。**問題はハブ ↔ ハブの相互参照のみ**。
