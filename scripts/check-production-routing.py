#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

EXPECTED = {
    "production/docker": ["ci-cd", "deployment"],
    "production/ci-cd": ["docker", "deployment", "secrets-management"],
    "production/deployment": ["ci-cd", "docker", "observability", "migrations"],
    "production/observability": ["deployment", "performance"],
    "production/performance": ["observability", "query-optimization"],
}

def get_section(text, title):
    m = re.search(
        rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        text, re.M | re.S
    )
    return m.group(1) if m else ""

failures = 0
print(f"Checking production semantic routing under {ROOT}")

for source, targets in EXPECTED.items():
    p = ROOT / source / "SKILL.md"
    if not p.exists():
        continue

    text = p.read_text(encoding="utf-8", errors="replace")
    section = get_section(text, "Cross-Skill Routing")

    if not section:
        print(f"MISSING ROUTING SECTION: {source}")
        failures += 1
        continue

    for target in targets:
        name = target.rsplit("/", 1)[-1]
        if not re.search(rf"`{re.escape(name)}`|\b{re.escape(name)}\b", section):
            print(f"ROUTING: {source}/SKILL.md -> {name}")
            failures += 1

print()
print("Production routing review:", "FAIL" if failures else "PASS")
if failures:
    print(f"Issues: {failures}")
    raise SystemExit(1)
