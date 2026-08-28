#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

ROUTES = {
"production/docker": """For pipeline/build promotion behavior, coordinate with `ci-cd`.
For live rollout/runtime health and recovery, coordinate with `deployment`.""",

"production/ci-cd": """For container image/runtime construction, coordinate with `docker`.
For live rollout and post-deploy validation, coordinate with `deployment`.
For credential/workflow secret lifecycle, coordinate with `secrets-management`.""",

"production/deployment": """For build/artifact promotion, coordinate with `ci-cd`.
For container runtime/image behavior, coordinate with `docker`.
For health gates and rollout diagnosis, coordinate with `observability`.
For schema/data compatibility, coordinate with `migrations`.""",

"production/observability": """For release/rollout correlation and health gates, coordinate with `deployment`.
For performance diagnosis and optimization, coordinate with `performance`.""",

"production/performance": """For telemetry and measured performance evidence, coordinate with `observability`.
For slow database access paths, coordinate with `query-optimization`.""",
}

def has_section(text, title):
    return re.search(rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$", text, re.M)

changed = 0
for rel, body in ROUTES.items():
    p = ROOT / rel / "SKILL.md"
    if not p.exists():
        print(f"ERROR: missing {rel}")
        raise SystemExit(1)
    text = p.read_text(encoding="utf-8")
    if not has_section(text, "Cross-Skill Routing"):
        p.write_text(text.rstrip() + "\n\n## Cross-Skill Routing\n" + body.strip() + "\n", encoding="utf-8")
        print(f"FIXED: {rel}")
        changed += 1
    else:
        print(f"OK: {rel}")

print(f"Changed files: {changed}")
