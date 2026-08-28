#!/usr/bin/env python3
from pathlib import Path
import re
import sys
from collections import defaultdict

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
skills = sorted(ROOT.rglob("SKILL.md"))

if not skills:
    print("ERROR: no SKILL.md files found")
    raise SystemExit(1)

required = ["Activation", "Review Procedure", "Verification Checklist"]
errors = []
warnings = []

def has_section(text, title):
    return re.search(
        rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$",
        text, re.M
    ) is not None

def get_frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else None

def route_section(text):
    m = re.search(
        r"^##\s+(?:\d+[\.\)]\s*)?Cross-Skill Routing\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        text, re.M | re.S
    )
    return m.group(1) if m else ""

print("=" * 72)
print("ENTERPRISE AGENT SKILLS — V2 FINAL AUDIT")
print("=" * 72)
print(f"Root: {ROOT}")
print(f"Skills: {len(skills)}")
print()

names = defaultdict(list)

for p in skills:
    text = p.read_text(encoding="utf-8", errors="replace")
    rel = p.relative_to(ROOT)

    fm = get_frontmatter(text)
    if fm is None:
        errors.append(f"{rel}: missing/invalid frontmatter")
    else:
        nm = re.search(r"^name:\s*(.+)$", fm, re.M)
        desc = re.search(r"^description:\s*(.+)$", fm, re.M)
        if not nm:
            errors.append(f"{rel}: frontmatter missing name")
        else:
            names[nm.group(1).strip()].append(str(rel))
        if not desc:
            errors.append(f"{rel}: frontmatter missing description")

    for section in required:
        if not has_section(text, section):
            errors.append(f"{rel}: missing {section}")

for name, paths in {k:v for k,v in names.items() if len(v) > 1}.items():
    errors.append(f"duplicate skill name '{name}': {paths}")

print("1) STRUCTURE")
print(f"   Frontmatter/required sections: {'FAIL' if errors else 'PASS'}")
for e in errors:
    print(f"   ERROR: {e}")
print()

ref_problems = []
for p in skills:
    text = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"`([^`]+(?:\.md|\.py))`", text):
        ref = m.group(1)
        if ref.startswith(("references/", "examples/", "scripts/")):
            target = p.parent / ref
            if not target.exists():
                ref_problems.append(f"{p.relative_to(ROOT)} -> missing {ref}")
warnings.extend(ref_problems)

print("2) LOCAL REFERENCES")
print(f"   Reference check: {'PASS' if not ref_problems else 'WARN'}")
for w in ref_problems:
    print(f"   WARNING: {w}")
print()

expected = {
    "backend/api-design": ["validation", "authorization", "service-layer", "error-handling"],
    "backend/service-layer": ["repository-pattern", "transactions", "concurrency"],
    "backend/repository-pattern": ["query-optimization", "postgresql", "authorization"],
    "backend/transactions": ["concurrency", "repository-pattern"],
    "backend/concurrency": ["transactions", "postgresql"],
    "backend/error-handling": ["api-design"],
    "backend/validation": ["api-design", "api-security"],
    "database/query-optimization": ["indexing", "performance"],
    "database/indexing": ["query-optimization", "migrations"],
    "database/migrations": ["postgresql", "deployment"],
    "frontend/forms": ["async-ui-states", "api-design", "accessibility"],
    "frontend/tables": ["responsive-design", "accessibility", "authorization", "query-optimization"],
    "frontend/navigation": ["accessibility", "responsive-design", "authorization"],
    "frontend/ui-design": ["ux-design", "accessibility", "responsive-design"],
    "frontend/ux-design": ["async-ui-states", "accessibility"],
    "frontend/async-ui-states": ["api-design", "concurrency"],
    "frontend/responsive-design": ["accessibility", "ui-design"],
    "frontend/accessibility": ["ui-design", "forms", "navigation"],
    "production/docker": ["ci-cd", "deployment"],
    "production/ci-cd": ["docker", "deployment", "secrets-management"],
    "production/deployment": ["ci-cd", "docker", "observability", "migrations"],
    "production/observability": ["deployment", "performance"],
    "production/performance": ["observability", "query-optimization"],
    "security/authentication": ["api-security", "secrets-management"],
    "security/authorization": ["api-security"],
    "security/api-security": ["authentication", "authorization", "owasp"],
    "security/owasp": ["authentication", "authorization", "api-security", "secrets-management"],
    "security/secrets-management": ["ci-cd"],
}

route_issues = []
for source, targets in expected.items():
    p = ROOT / source / "SKILL.md"
    if not p.exists():
        continue
    section = route_section(p.read_text(encoding="utf-8", errors="replace"))
    for target in targets:
        name = target.rsplit("/",1)[-1]
        if not re.search(rf"`{re.escape(name)}`|\b{re.escape(name)}\b", section):
            route_issues.append(f"{source} -> {target}")

warnings.extend(route_issues)

print("3) SEMANTIC ROUTING")
print(f"   Routing check: {'PASS' if not route_issues else 'WARN'}")
for w in route_issues:
    print(f"   WARNING: missing handoff {w}")
print()

# Only detect positive claims. A line is ignored when it explicitly rejects
# the claim (do not/avoid/never/not) or appears inside a negative anti-pattern.
claim_hits = []
patterns = [
    re.compile(r"\bOWASP\s+compliant\b", re.I),
    re.compile(r"\bOWASP\s+certified\b", re.I),
    re.compile(r"\bformal\s+OWASP\s+certification\b", re.I),
]
negative = re.compile(
    r"\b(do not|don't|avoid|never|not|without|cannot|can't|should not)\b",
    re.I,
)

for p in skills:
    for line_no, line in enumerate(
        p.read_text(encoding="utf-8", errors="replace").splitlines(), 1
    ):
        if any(pattern.search(line) for pattern in patterns):
            if negative.search(line):
                continue
            # Quoted examples in an "anti-pattern" or "Do not say" block are not claims.
            window = line.lower()
            if "anti-pattern" in window or "do not say" in window:
                continue
            claim_hits.append(f"{p.relative_to(ROOT)}:{line_no}: possible unsupported OWASP compliance claim")

warnings.extend(claim_hits)

print("4) CLAIMS / DRIFT HEURISTICS")
print(f"   Heuristic check: {'PASS' if not claim_hits else 'WARN'}")
for w in claim_hits:
    print(f"   WARNING: {w}")
print()

print("5) INVENTORY")
groups = defaultdict(int)
for p in skills:
    parts = p.relative_to(ROOT).parts
    groups[parts[0] if parts else "."] += 1
for group in sorted(groups):
    print(f"   {group}: {groups[group]} skills")
print()

print("=" * 72)
print(f"FINAL RESULT: {'PASS' if not errors else 'FAIL'}")
print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")
print("=" * 72)

sys.exit(1 if errors else 0)
