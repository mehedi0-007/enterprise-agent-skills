#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

ROUTES = {
"frontend/forms": """For network/server lifecycle behavior, coordinate with `async-ui-states`.
For API request/response semantics, coordinate with `api-design`.
For labels, focus, and error accessibility, coordinate with `accessibility`.""",

"frontend/tables": """For responsive table behavior, coordinate with `responsive-design`.
For semantic/keyboard behavior, coordinate with `accessibility`.
For access-control decisions, coordinate with `authorization`.
For large-data/query performance, coordinate with `query-optimization`.""",

"frontend/navigation": """For keyboard/focus semantics, coordinate with `accessibility`.
For mobile layout/adaptation, coordinate with `responsive-design`.
For actual access control, coordinate with `authorization`.""",

"frontend/ui-design": """For task-flow and recovery behavior, coordinate with `ux-design`.
For accessible semantics and interaction, coordinate with `accessibility`.
For viewport/layout adaptation, coordinate with `responsive-design`.""",

"frontend/ux-design": """For network/server lifecycle behavior, coordinate with `async-ui-states`.
For API contract semantics, coordinate with `api-design`.
For accessible interaction behavior, coordinate with `accessibility`.""",

"frontend/responsive-design": """For accessible responsive behavior, coordinate with `accessibility`.
For visual hierarchy/control placement, coordinate with `ui-design`.""",

"frontend/accessibility": """Apply these constraints across `ui-design`, `forms`, and `navigation`.
Coordinate responsive semantic transformations with `responsive-design`.""",
}

def has_h2(text, title):
    return re.search(rf"^##\s+(?:\d+[\.\)]\s*)?{re.escape(title)}\s*$", text, re.M)

changed = 0
for rel, body in ROUTES.items():
    path = ROOT / rel / "SKILL.md"
    if not path.exists():
        print(f"ERROR: missing {path.relative_to(ROOT)}")
        raise SystemExit(1)

    text = path.read_text(encoding="utf-8")
    if not has_h2(text, "Cross-Skill Routing"):
        text = text.rstrip() + "\n\n## Cross-Skill Routing\n" + body.strip() + "\n"
        path.write_text(text, encoding="utf-8")
        print(f"FIXED: {rel}")
        changed += 1
    else:
        print(f"OK: {rel}")

print(f"Changed files: {changed}")
