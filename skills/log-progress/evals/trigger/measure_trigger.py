#!/usr/bin/env python3
"""Full 18-query trigger measurement for log-progress (patched harness).

Measures the REAL installed skill in the REAL user environment.
Usage: patched_trigger_eval_full.py [model] [runs_per_query]
Reads queries+labels from trigger-eval.json next to this script.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PREAMBLE = (
    "(状況: このセッションではさっきまで実作業をしていた。データローダのバグを調査し、"
    "原因を特定して修正し、テストが通ることまで確認済みである。その上での依頼:) "
)


def run_query(query: str, model: str) -> tuple[bool, str]:
    cmd = [
        "claude", "-p", PREAMBLE + query,
        "--output-format", "stream-json", "--verbose",
        "--include-partial-messages", "--max-turns", "2",
        "--model", model,
    ]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, env=env,
                           cwd="/home/atsushi", timeout=180)
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    tools = []
    for line in r.stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "assistant":
            for c in e.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    name = c.get("name", "")
                    inp = json.dumps(c.get("input", {}), ensure_ascii=False)
                    tools.append(f"{name}:{inp[:60]}")
                    if name in ("Skill", "Read") and "log-progress" in inp:
                        return True, " | ".join(tools)
    return False, " | ".join(tools) if tools else "no tools"


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "claude-sonnet-5"
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    here = Path(__file__).parent
    items = json.load(open(here / "trigger-eval.json"))

    def job(item):
        results = [run_query(item["query"], model) for _ in range(runs)]
        rate = sum(ok for ok, _ in results) / runs
        return item, rate, results[-1][1]

    with ThreadPoolExecutor(max_workers=3) as ex:
        rows = list(ex.map(job, items))

    tp = fn = tn = fp = 0
    for item, rate, detail in rows:
        expected = item["should_trigger"]
        fired = rate >= 0.5
        ok = fired == expected
        if expected:
            tp += ok
            fn += (not ok)
        else:
            tn += ok
            fp += (not ok)
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] expect={'T' if expected else 'F'} rate={rate:.2f}  {item['query'][:44]}")
        if not ok:
            print(f"       tools: {detail[:110]}")
    n_t, n_f = tp + fn, tn + fp
    print(f"\nrecall: {tp}/{n_t}   precision-side pass: {tn}/{n_f}   accuracy: {(tp+tn)}/{n_t+n_f}")


if __name__ == "__main__":
    main()
