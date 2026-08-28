#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

ROUTES = {
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

def route_section(text: str) -> str:
    m = re.search(
        r"^##\s+(?:\d+[\.\)]\s*)?Cross-Skill Routing\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        text, re.M | re.S
    )
    return m.group(1) if m else ""

problems = 0
for source, targets in ROUTES.items():
    p = ROOT / source / "SKILL.md"
    if not p.exists():
        continue
    section = route_section(p.read_text(encoding="utf-8", errors="replace"))
    for target in targets:
        if not re.search(rf"`{re.escape(target)}`|\b{re.escape(target)}\b", section):
            print(f"ROUTING: {source} -> {target}")
            problems += 1

# Only flag positive unsupported claims, not anti-pattern examples that explicitly reject them.
for p in sorted(ROOT.rglob("SKILL.md")):
    text = p.read_text(encoding="utf-8", errors="replace")
    for line_no, line in enumerate(text.splitlines(), 1):
        if re.search(r"\bOWASP compliant\b", line, re.I):
            if re.search(r"\b(do not|avoid|never|not|don't)\b", line, re.I):
                continue
            print(f"CLAIM: {p.relative_to(ROOT)}:{line_no}: unsupported 'OWASP compliant' claim")
            problems += 1

print()
if problems:
    print(f"Warning review: {problems} issue(s)")
    raise SystemExit(1)

print("Warning review: PASS")
