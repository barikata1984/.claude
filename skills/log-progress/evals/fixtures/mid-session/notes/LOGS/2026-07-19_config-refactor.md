# 2026-07-19 config-refactor

## Topic

設定ローダの YAML 一本化リファクタ。JSON/YAML/env の 3 系統に散らばった設定の整合性回復が目的。

## History

設定が 3 系統に散らばり、優先順位が実装ごとに異なりバグの温床になっていた。まず影響範囲を grep で調べ、env 経由の設定は 2 箇所でしか使われておらず廃止コストが低いことを確認した。一本化先の検討では、JSON はコメントが書けず運用ノートを残せないため却下し、YAML 一本化を採用した (ユーザー確認済み)。src/config/loader.py を新設し、JSON ローダを削除した。

## Decisions

- YAML 一本化を採用 / 却下: JSON 一本化 — ユーザー確認済み

## Changes

- src/config/loader.py を新設、JSON ローダを削除

## Open Items

- ネスト階層の flatten を検討する
