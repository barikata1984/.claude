#!/usr/bin/env python3
"""check_proposal.py — research-theme-proposal の決定論的品質ゲート。

Claude Code の hook (TaskCompleted / Stop) から呼ばれる想定。
output/proposals/P*.md のうち status が screened のものだけを検証し、
違反があれば exit 2 + stderr にフィードバック(Claude に差し戻される)。
draft (作成中) / accepted (テーマ確定後の作業フェーズ) / rejected (落選) は
検証対象外 — 確定済みの提案が以降の全セッションで毎ターン差し戻される粘着を防ぐ。

注意: hook の入力 JSON スキーマは Claude Code のバージョンで変わり得るため、
本スクリプトは stdin に依存せず、常にファイルシステムを直接検証する
(stdin は読み捨てる)。settings.json 側の配線は README 参照。
"""

import re
import sys
from pathlib import Path

PROPOSAL_DIR = Path("output/proposals")

REQUIRED_FRONTMATTER = [
    "proposal_id", "title", "mechanism", "survey_slug", "gap_refs", "status",
    "iteration", "novelty_log", "novelty_verdict", "baselines_verified",
    "citations_total", "citations_recent_18mo", "kill_criterion_quantified",
    "human_approved",
]

REQUIRED_SECTIONS = [
    "## Heilmeier Answers",
    "## Gap Grounding",
    "## Approach Sketch",
    "## Required Components & Readiness",
    "## Mini Experiment Plan",
    "## Red-team Record",
    "## Rubric Scores",
    "## References",
]

REQUIRED_SKETCH_FIELDS = [
    "**構成要素と動作原理**", "**要素間の依存関係**", "**統合方針**",
    "**対抗系統と比較方針**", "**未確定事項**",
]

REQUIRED_PLAN_FIELDS = [
    "**Task & embodiment**", "**Sim / Real**", "**Baselines**",
    "**Metrics & trials**", "**Data / compute budget**",
    "**De-risking experiment", "**Kill criterion**", "**Expected failure modes**",
]

VALID_MECHANISMS = {
    "enabler-driven", "cross-domain-transfer",
    "benchmark-definition", "assumption-busting",
}
VALID_VERDICTS = {"distinct", "incremental", "duplicate"}

# kill criterion の非数値表現(日本語/英語の代表例)
VAGUE_KILL = re.compile(
    r"(うまくいかな|有望でな|十分な性能|期待した結果|"
    r"if it (doesn't|does not) work|promising|insufficient performance)",
    re.IGNORECASE,
)
HAS_NUMBER = re.compile(r"\d")


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.split("#")[0].strip().strip('"')
    return fm


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if not fm:
        return [f"{path.name}: YAML frontmatter が無い"]

    status = fm.get("status", "")
    # 検証するのは screened (ゲート通過を主張する状態) のみ。
    # draft / accepted / rejected は対象外: 確定後の提案が後続作業の
    # 全ターンで差し戻される粘着を防ぐ (accepted = テーマ確定後の作業フェーズ)。
    if status != "screened":
        return []

    for key in REQUIRED_FRONTMATTER:
        if key not in fm or fm[key] == "":
            errors.append(f"{path.name}: frontmatter `{key}` が欠落")

    if fm.get("mechanism") not in VALID_MECHANISMS:
        errors.append(f"{path.name}: mechanism が不正: {fm.get('mechanism')}")
    if fm.get("novelty_verdict") not in VALID_VERDICTS:
        errors.append(f"{path.name}: novelty_verdict が不正")
    if fm.get("novelty_verdict") == "duplicate" and status == "screened":
        errors.append(f"{path.name}: duplicate 判定の候補が screened になっている")
    # human_approved は検証対象外: 人間が true に変更した後のセッションで
    # hook が落ちる自己矛盾を防ぐため (ISSUES.md 2026-06-11 記録)

    nl = fm.get("novelty_log", "")
    if nl and not Path(nl).exists():
        errors.append(f"{path.name}: novelty_log が存在しない: {nl}")

    try:
        total = int(fm.get("citations_total", "0"))
        recent = int(fm.get("citations_recent_18mo", "0"))
        if total < 8:
            errors.append(f"{path.name}: 引用 {total} 本 (< 8)")
        if recent < 3:
            errors.append(f"{path.name}: 直近 18 ヶ月の引用 {recent} 本 (< 3)")
    except ValueError:
        errors.append(f"{path.name}: citations_* が整数でない")

    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            errors.append(f"{path.name}: セクション欠落: {sec}")
        else:  # 非空チェック: 見出しの後に 30 文字以上の本文
            after = text.split(sec, 1)[1]
            body = after.split("\n## ", 1)[0]
            if len(re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()) < 30:
                errors.append(f"{path.name}: セクションが実質空: {sec}")

    for field in REQUIRED_PLAN_FIELDS:
        if field not in text:
            errors.append(f"{path.name}: Mini Experiment Plan フィールド欠落: {field}")

    for field in REQUIRED_SKETCH_FIELDS:
        if field not in text:
            errors.append(f"{path.name}: Approach Sketch フィールド欠落: {field}")

    # kill criterion の定量性
    m = re.search(r"\*\*Kill criterion\*\*:\s*(.+)", text)
    if m:
        kc = m.group(1)
        if VAGUE_KILL.search(kc) or not HAS_NUMBER.search(kc):
            errors.append(
                f"{path.name}: kill criterion が非定量 (数値を含む撤退基準に書き直す): {kc[:60]}"
            )

    return errors


def main() -> int:
    try:
        sys.stdin.read()  # hook 入力は読み捨て(スキーマ非依存)
    except Exception:
        pass

    if not PROPOSAL_DIR.exists():
        return 0  # まだ提案が無い段階では通す

    files = sorted(PROPOSAL_DIR.glob("P*.md"))
    if not files:
        return 0

    all_errors: list[str] = []
    screened = 0
    for f in files:
        errs = check_file(f)
        all_errors.extend(errs)
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        if fm.get("status") == "screened" and not errs:
            screened += 1

    if all_errors:
        print("check_proposal.py: FAIL", file=sys.stderr)
        for e in all_errors[:20]:
            print(f"  - {e}", file=sys.stderr)
        print(
            f"  ({len(all_errors)} 件。proposal_template.md に従って修正すること)",
            file=sys.stderr,
        )
        return 2

    print(f"check_proposal.py: PASS ({screened} screened proposals)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
