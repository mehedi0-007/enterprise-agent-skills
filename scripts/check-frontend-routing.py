#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

REQUIRED_ROUTES = {
    "frontend/forms": ["async-ui-states", "api-design", "accessibility"],
    "frontend/tables": ["responsive-design", "accessibility", "authorization", "query-optimization"],
    "frontend/navigation": ["accessibility", "responsive-design", "authorization"],
    "frontend/ui-design": ["ux-design", "accessibility", "responsive-design"],
    "frontend/ux-design": ["async-ui-states", "accessibility"],
    "frontend/async-ui-states": ["api-design", "concurrency"],
    "frontend/responsive-design": ["accessibility", "ui-design"],
    "frontend/accessibility": ["ui-design", "forms", "navigation"],
}

def section(text, title):
    m = re.search(
        rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        text, re.M | re.S
    )
    return m.group(1) if m else ""

failures = 0

print(f"Checking frontend semantic routing under {ROOT}")
for source_dir, targets in REQUIRED_ROUTES.items():
    p = ROOT / source_dir / "SKILL.md"
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    route = section(text, "Cross-Skill Routing")
    if not route:
        print(f"MISSING ROUTING SECTION: {source_dir}")
        failures += 1
        continue
    for target in targets:
        if not re.search(rf"`{re.escape(target)}`|\b{re.escape(target)}\b", route):
            print(f"ROUTING: {source_dir}/SKILL.md -> {target}")
            failures += 1

print()
print("Frontend routing review:", "FAIL" if failures else "PASS")
if failures:
    print(f"Issues: {failures}")
    sys.exit(1)
