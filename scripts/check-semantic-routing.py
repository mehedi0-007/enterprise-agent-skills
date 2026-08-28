#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
skills = sorted(ROOT.rglob("SKILL.md"))
names = {p.parent.name for p in skills}

EXPECTED = {
    "indexing": ["query-optimization"],
    "postgresql": ["query-optimization", "indexing", "migrations"],
    "ux-design": ["api-design", "concurrency", "transactions", "async-ui-states"],
    "async-ui-states": ["api-design", "concurrency"],
    "deployment": ["migrations", "observability", "ci-cd", "docker"],
    "ci-cd": ["docker", "secrets-management"],
    "api-security": ["authentication", "authorization", "owasp"],
    "owasp": ["authentication", "authorization", "api-security", "secrets-management"],
}

print(f"Checking semantic routing under {ROOT}")
problems = []

for skill_name, expected in EXPECTED.items():
    path = next((p for p in skills if p.parent.name == skill_name), None)
    if not path:
        continue

    text = path.read_text(encoding="utf-8", errors="replace")

    for target in expected:
        if target not in names:
            continue
        # Explicit mention in backticks is preferred for unambiguous routing.
        if not re.search(rf"`{re.escape(target)}`", text):
            problems.append(
                f"{path.relative_to(ROOT)} should explicitly route to `{target}` "
                f"when that boundary is relevant."
            )

if problems:
    for p in problems:
        print("ROUTING:", p)
    print(f"\nRouting review: {len(problems)} issue(s)")
    sys.exit(1)

print("Routing review: PASS")
