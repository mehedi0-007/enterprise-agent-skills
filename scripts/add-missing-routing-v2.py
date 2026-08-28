#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

ROUTES = {
"backend/api-design": [
    "validation", "authorization", "service-layer", "error-handling"
],
"backend/service-layer": [
    "repository-pattern", "transactions", "concurrency"
],
"backend/repository-pattern": [
    "query-optimization", "postgresql", "authorization"
],
"backend/transactions": [
    "concurrency", "repository-pattern"
],
"backend/concurrency": [
    "transactions", "postgresql"
],
"backend/error-handling": [
    "api-design"
],
"backend/validation": [
    "api-design", "api-security"
],
"database/query-optimization": [
    "indexing", "performance"
],
"database/indexing": [
    "query-optimization", "migrations"
],
"database/migrations": [
    "postgresql", "deployment"
],
"security/authentication": [
    "api-security", "secrets-management"
],
"security/authorization": [
    "api-security"
],
"security/secrets-management": [
    "ci-cd"
],
}

def has_h2(text: str, title: str) -> bool:
    return re.search(
        rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$",
        text, re.M
    ) is not None

def routing_section(text: str) -> str:
    m = re.search(
        r"^##\s+(?:\d+[\.\)]\s*)?Cross-Skill Routing\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        text, re.M | re.S
    )
    return m.group(1) if m else ""

changed = 0

for source, targets in ROUTES.items():
    path = ROOT / source / "SKILL.md"
    if not path.exists():
        print(f"ERROR: missing {source}/SKILL.md")
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")
    original = text

    if not has_h2(text, "Cross-Skill Routing"):
        lines = []
        for target in targets:
            lines.append(
                f"- For `{target}` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance."
            )
        text = (
            text.rstrip()
            + "\n\n## Cross-Skill Routing\n"
            + "\n".join(lines)
            + "\n"
        )
    else:
        section = routing_section(text)
        missing = [
            target for target in targets
            if not re.search(rf"`{re.escape(target)}`|\b{re.escape(target)}\b", section)
        ]
        if missing:
            additions = [
                f"- For `{target}` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance."
                for target in missing
            ]
            # Insert before next H2/end of file.
            marker = re.search(r"^##\s+", text[re.search(r"^##\s+(?:\d+[\.\)]\s*)?Cross-Skill Routing\s*$", text, re.M).end():], re.M)
            if marker:
                pos = re.search(r"^##\s+(?:\d+[\.\)]\s*)?Cross-Skill Routing\s*$", text, re.M).end() + marker.start()
                text = text[:pos].rstrip() + "\n" + "\n".join(additions) + "\n\n" + text[pos:]
            else:
                text = text.rstrip() + "\n" + "\n".join(additions) + "\n"

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"FIXED: {source}")
        changed += 1
    else:
        print(f"OK: {source}")

print(f"Changed files: {changed}")
