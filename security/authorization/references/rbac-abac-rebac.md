# RBAC vs ABAC vs Relationship-Based Access

## RBAC
Use when stable roles map cleanly to capabilities.

## ABAC
Use when decisions depend on principal/resource/environment attributes.

## Relationship-Based
Use when access naturally follows graph-like relationships such as user→team→project→document.

Many real systems combine them:
permission from role + tenant membership + resource relationship + state rule.

Do not force one model to express everything.
