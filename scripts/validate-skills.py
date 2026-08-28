#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

skill_files = sorted(ROOT.rglob("SKILL.md"))

if not skill_files:
    errors.append("No SKILL.md files found.")

names = {}
for path in skill_files:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        errors.append(f"{rel}: missing YAML frontmatter")
        continue
    match = re.search(r"^name:\s*(.+)$", text, re.M)
    desc = re.search(r"^description:\s*(.+)$", text, re.M)
    if not match:
        errors.append(f"{rel}: missing name")
    else:
        name = match.group(1).strip()
        if name in names:
            errors.append(f"{rel}: duplicate skill name '{name}' (also {names[name]})")
        names[name] = str(rel)
    if not desc:
        errors.append(f"{rel}: missing description")
    if len(text.splitlines()) < 20:
        warnings.append(f"{rel}: unusually short SKILL.md")
    if "Verification" not in text and "verification" not in text:
        warnings.append(f"{rel}: no obvious verification section")

# Check references mentioned by SKILL.md.
for path in skill_files:
    text = path.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"`([^`]+\.md)`", text):
        ref = m.group(1)
        if ref.startswith(("references/", "examples/")):
            candidate = path.parent / ref
            if not candidate.exists():
                warnings.append(f"{path.relative_to(ROOT)}: missing referenced file {ref}")

print(f"Skills found: {len(skill_files)}")
print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")

for item in errors:
    print(f"ERROR: {item}")
for item in warnings:
    print(f"WARNING: {item}")

sys.exit(1 if errors else 0)
