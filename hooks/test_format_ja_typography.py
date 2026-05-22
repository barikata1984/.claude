#!/usr/bin/env python3
"""Regression tests for format_ja_typography. Run: python3 test_format_ja_typography.py"""

from format_ja_typography import normalize, warnings

CASES = [
    # (name, input, expected)
    ("sentence period", "これはテスト。", "これはテスト."),
    ("comma", "A、B、C", "A, B, C"),
    ("bang/question", "本当！そう？", "本当! そう?"),
    ("mid-sentence period+space", "終わり。次の文。", "終わり. 次の文."),
    ("colon full-width", "注：重要", "注: 重要"),
    ("brackets", "彼は「了解」と言った（笑）。", '彼は"了解"と言った(笑).'),
    ("nested quotes", "「外『内』外」", "\"外'内'外\""),
    ("preserve wave/nakaguro", "範囲は3〜5、A・B。", "範囲は3〜5, A・B."),
    # ASCII is never touched -> decimals / abbreviations / versions stay intact.
    ("decimal safe", "値は3.14です。", "値は3.14です."),
    ("thousands safe", "総額1,000円。", "総額1,000円."),
    ("abbrev safe", "例えば e.g. これ。", "例えば e.g. これ."),
    ("version safe", "v1.2 を使う。", "v1.2 を使う."),
    # Protected spans: full-width inside them must survive untouched.
    ("inline code", "`コード。内、` を実行。", "`コード。内、` を実行."),
    ("fenced code", "```\nx = 1  # 日本語。コメント、\n```\n本文。",
                    "```\nx = 1  # 日本語。コメント、\n```\n本文."),
    ("front matter", "---\ntitle: テスト。\n---\n本文、です。",
                     "---\ntitle: テスト。\n---\n本文, です."),
    ("inline math", "式 $f(x, y) = 3.14$ は。", "式 $f(x, y) = 3.14$ は."),
    ("display math", "$$\na, b = 1, 2\n$$\n説明。", "$$\na, b = 1, 2\n$$\n説明."),
    ("latex cmd", r"\ref{fig:1} を見よ。", r"\ref{fig:1} を見よ."),
    ("link target", "[リンク。](https://ex.com/a,b) です。",
                    '[リンク.](https://ex.com/a,b) です.'),
    ("bare url", "参照 https://ex.com/x。次。", "参照 https://ex.com/x. 次."),
    ("autolink", "<https://ex.com/a。b> 終わり。", "<https://ex.com/a。b> 終わり."),
    # Spacing cleanup.
    ("collapse double space", "終わり。 次。", "終わり. 次."),
    ("strip trailing", "行末。\n次行、", "行末.\n次行,"),
    ("strip trailing eof", "最後。", "最後."),
]


def run() -> int:
    failed = 0
    for name, src, want in CASES:
        got = normalize(src)
        if got != want:
            failed += 1
            print(f"FAIL {name}\n  in : {src!r}\n  got: {got!r}\n  exp: {want!r}")
        # idempotency: applying twice must equal applying once
        twice = normalize(got)
        if twice != got:
            failed += 1
            print(f"FAIL {name} [idempotency]\n  once: {got!r}\n  twice: {twice!r}")
    # warning detection (no auto-fix)
    w = warnings("結果は — 意外にも — 保たれた。コードは `a—b`。")
    assert any("em dash" in x for x in w), f"expected em dash warning, got {w}"
    assert normalize("結果 — 保たれた。") == "結果 — 保たれた.", "em dash must NOT be auto-removed"
    # em dash inside code must not be warned
    assert not warnings("`a — b`"), f"em dash in code must not warn, got {warnings('`a — b`')}"

    if failed:
        print(f"\n{failed} failure(s)")
        return 1
    print(f"all {len(CASES)} cases + warnings/idempotency passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
