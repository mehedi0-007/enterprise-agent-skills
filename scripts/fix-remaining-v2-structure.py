#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# These are the only structural gaps reported by the corrected audit.
FIXES = {
    "engineering/production-readiness/SKILL.md": {
        "Activation": """Use when deciding whether a feature, service, or release is ready for production, especially when security, reliability, migrations, observability, or recovery risks are involved."""
    },
    "frontend/async-ui-states/SKILL.md": {
        "Activation": """Use when UI behavior depends on network/server work such as fetching, mutations, uploads, polling, retries, cancellation, optimistic updates, or background jobs."""
    },
    "production/ci-cd/SKILL.md": {
        "Review Procedure": """1. Identify every trigger and trust boundary.
2. Inspect job permissions and secret access.
3. Verify tests/build/security gates are meaningful.
4. Verify artifact identity and promotion behavior.
5. Review migration/environment/deployment compatibility.
6. Review concurrency, runner trust, and third-party action risks.
7. Verify post-deploy validation and recovery paths."""
    },
}

def has_section(text: str, title: str) -> bool:
    pattern = rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$"
    return re.search(pattern, text, re.M) is not None

changed = 0
for rel, additions in FIXES.items():
    path = ROOT / rel
    if not path.exists():
        print(f"ERROR: missing {rel}")
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")
    original = text

    for title, body in additions.items():
        if not has_section(text, title):
            text = text.rstrip() + f"\n\n## {title}\n\n{body.strip()}\n"

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"FIXED: {rel}")
        changed += 1
    else:
        print(f"OK: {rel}")

print(f"Changed files: {changed}")
