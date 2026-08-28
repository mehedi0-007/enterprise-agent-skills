#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
skills = sorted(ROOT.rglob("SKILL.md"))

if not skills:
    print("No SKILL.md files found.")
    raise SystemExit(1)

EXPECTED = {
    "frontend/ux-design": ["frontend/async-ui-states"],
    "frontend/async-ui-states": ["backend/api-design", "backend/concurrency"],
    "production/deployment": [
        "database/migrations",
        "production/observability",
        "production/ci-cd",
        "production/docker",
    ],
    "production/ci-cd": [
        "production/docker",
        "security/secrets-management",
    ],
    "security/api-security": [
        "security/authentication",
        "security/authorization",
        "security/owasp",
    ],
    "security/owasp": [
        "security/authentication",
        "security/authorization",
        "security/api-security",
        "security/secrets-management",
    ],
}

path_by_dir = {
    p.parent.relative_to(ROOT).as_posix(): p
    for p in skills
}

print(f"Checking explicit routing sections under {ROOT}")

failures = 0
for source_dir, targets in EXPECTED.items():
    source = path_by_dir.get(source_dir)
    if not source:
        continue

    text = source.read_text(encoding="utf-8", errors="replace")

    # Only inspect the routing section when present. This avoids unrelated
    # mentions elsewhere from satisfying the test.
    match = re.search(
        r"^##\s+(?:\d+[\.\)]\s*)?Cross-Skill Routing\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        text,
        re.M | re.S,
    )
    section = match.group(1) if match else ""

    for target in targets:
        skill_name = target.rsplit("/", 1)[-1]
        if not section or not re.search(
            rf"`{re.escape(skill_name)}`|\b{re.escape(skill_name)}\b",
            section,
        ):
            print(
                f"ROUTING: {source_dir}/SKILL.md is missing explicit "
                f"routing to `{skill_name}`."
            )
            failures += 1

if failures:
    print(f"\nRouting review: FAIL ({failures} issue(s))")
    raise SystemExit(1)

print("\nRouting review: PASS")
