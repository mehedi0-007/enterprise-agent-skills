#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
skills = sorted(ROOT.rglob("SKILL.md"))

if not skills:
    print("No SKILL.md files found.")
    raise SystemExit(1)

print(f"Auditing {len(skills)} skill files under {ROOT}")
print()

def has_section(text: str, title: str) -> bool:
    # Accept both:
    # ## Activation
    # ## 2. Activation
    # ## 2) Activation
    pattern = rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$"
    return re.search(pattern, text, re.M) is not None

required = ["Activation", "Review Procedure", "Verification Checklist"]
failed = False

for p in skills:
    text = p.read_text(encoding="utf-8", errors="replace")
    missing = [s for s in required if not has_section(text, s)]
    if missing:
        failed = True
        print(f"{p.relative_to(ROOT)}: missing {', '.join(missing)}")

# Only explicit backtick references count as cross-skill references.
skill_names = sorted({p.parent.name for p in skills})
print("\nCross-skill references:")
for p in skills:
    text = p.read_text(encoding="utf-8", errors="replace")
    refs = sorted({
        name for name in skill_names
        if re.search(rf"`{re.escape(name)}`", text)
    })
    if refs:
        print(f"  {p.relative_to(ROOT)} -> {', '.join(refs)}")

print()
print("Core contract:", "FAIL" if failed else "PASS")
raise SystemExit(1 if failed else 0)
