#!/usr/bin/env python3
from pathlib import Path
import re
import sys
from collections import defaultdict

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
skills = sorted(ROOT.rglob("SKILL.md"))

if not skills:
    print("No SKILL.md files found.")
    raise SystemExit(1)

print(f"Auditing {len(skills)} skill files under {ROOT}")
print()

required_sections = [
    "Activation",
    "Review Procedure",
    "Verification Checklist",
]

missing = defaultdict(list)
for p in skills:
    text = p.read_text(encoding="utf-8", errors="replace")
    for section in required_sections:
        if section.lower() not in text.lower():
            missing[section].append(str(p.relative_to(ROOT)))

if missing:
    for section, paths in missing.items():
        print(f"Missing '{section}' in:")
        for path in paths:
            print(f"  - {path}")
        print()
else:
    print("Core section check: PASS")

# Detect references to sibling skill names and report missing targets.
all_dirs = {p.parent.name for p in skills}
refs = defaultdict(list)
for p in skills:
    text = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"`([^`]+)`", text):
        candidate = m.group(1)
        if candidate in all_dirs:
            refs[p].append(candidate)

print("Cross-skill references found:")
for p, items in refs.items():
    unique = sorted(set(items))
    print(f"  {p.relative_to(ROOT)} -> {', '.join(unique)}")

# Flag obvious generic anti-patterns; these are review prompts, not automatic failures.
patterns = {
    "transaction makes everything safe": re.compile(r"transaction.*safe|safe.*transaction", re.I),
    "repository owns authorization": re.compile(r"repository.*authoriz|authoriz.*repository", re.I),
    "frontend hides security": re.compile(r"hide.*authorization|authorization.*hide", re.I),
    "index every where/filter column": re.compile(r"index.*every|every.*where.*index", re.I),
}

print()
print("Potential boundary-review phrases:")
for label, pattern in patterns.items():
    hits = []
    for p in skills:
        if pattern.search(p.read_text(encoding="utf-8", errors="replace")):
            hits.append(str(p.relative_to(ROOT)))
    if hits:
        print(f"  {label}:")
        for h in hits:
            print(f"    - {h}")

print()
print("Audit complete. Human review is still required for semantic conflicts.")
