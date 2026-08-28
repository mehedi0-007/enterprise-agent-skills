#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

ROUTES = {
"frontend/ux-design/SKILL.md": """For network/server lifecycle behavior, defer to `frontend/async-ui-states`.
For API contract semantics, coordinate with `backend/api-design`.
For forms and tables, use the specialized frontend skills rather than duplicating their detailed interaction rules.""",

"frontend/async-ui-states/SKILL.md": """For API status/error/idempotency contracts, coordinate with `backend/api-design`.
For duplicate requests, shared-state races, and backend correctness, coordinate with `backend/concurrency`.
For user workflow/recovery decisions, coordinate with `frontend/ux-design`.""",

"production/deployment/SKILL.md": """For schema/data rollout compatibility, coordinate with `database/migrations`.
For rollout health signals and post-deploy diagnosis, coordinate with `production/observability`.
For build, artifact, and promotion mechanics, coordinate with `production/ci-cd`.
For container image/runtime concerns, coordinate with `production/docker`.""",

"production/ci-cd/SKILL.md": """For container build/runtime details, coordinate with `production/docker`.
For credential lifecycle and workflow secret exposure, coordinate with `security/secrets-management`.
For live rollout and post-deploy behavior, coordinate with `production/deployment`.""",

"security/api-security/SKILL.md": """For identity, session, token, and recovery lifecycle, coordinate with `security/authentication`.
For object, tenant, function, and property authorization, coordinate with `security/authorization`.
For OWASP-oriented review orchestration, coordinate with `security/owasp`.
For credentials/keys used by the API or integrations, coordinate with `security/secrets-management`.""",

"security/owasp/SKILL.md": """Route identity/session issues to `security/authentication`.
Route access-control issues to `security/authorization`.
Route API attack-surface/abuse issues to `security/api-security`.
Route credential/key lifecycle issues to `security/secrets-management`.
This skill orchestrates review; the specialized skill owns implementation details.""",
}

def has_routing(text: str) -> bool:
    return re.search(r"^##\s+(?:\d+[\.\)]\s*)?Cross-Skill Routing\s*$", text, re.M) is not None

changed = 0
for rel, body in ROUTES.items():
    path = ROOT / rel
    if not path.exists():
        print(f"ERROR: missing {rel}")
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")
    if not has_routing(text):
        text = text.rstrip() + "\n\n## Cross-Skill Routing\n" + body.strip() + "\n"
        path.write_text(text, encoding="utf-8")
        print(f"FIXED: {rel}")
        changed += 1
    else:
        print(f"OK: {rel}")

print(f"Changed files: {changed}")
