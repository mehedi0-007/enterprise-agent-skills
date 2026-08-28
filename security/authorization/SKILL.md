---
name: authorization
description: Design and review server-side authorization and access-control decisions. Use for RBAC, ABAC, resource ownership, multi-tenancy, admin functions, object access, and permission changes.
---

# Authorization

## Goal
Ensure every protected operation is permitted for the authenticated principal in the current context.

OWASP recommends least privilege, deny-by-default, authorization checks on every request, and tests for authorization logic.

## Never Rely on the Client
Hidden buttons, disabled UI, route guards, and client-side role checks are UX controls, not security boundaries.
Authorization must be enforced server-side.

## Check the Right Object
Do not assume:
`GET /orders/123`
is safe because the user is authenticated.

Check whether the authenticated principal can access order 123.

Protect against IDOR/BOLA by enforcing ownership/relationship/permission checks.

## Function-Level Authorization
Administrative and privileged operations require explicit server-side authorization.

Examples:
- delete another user's account
- assign roles
- change billing ownership
- export organization data
- manage API keys

## Multi-Tenancy
Every tenant-scoped read/write should have an explicit tenant boundary.
Do not trust a tenant ID supplied by the client when the authenticated context already determines tenant membership.

Prefer queries that enforce tenant scope as part of the data-access operation.

## RBAC / ABAC / ReBAC
Use the simplest model that expresses the real policy.
- RBAC: roles map to permissions
- ABAC: decisions depend on attributes
- ReBAC: decisions depend on relationships

Do not force a complex policy model when simple ownership is enough.

## Deny by Default
Unknown role, missing permission, malformed context, or failed authorization lookup should fail closed.

## Sensitive Fields
Authorization can apply at property level, not only resource level.
A user may be allowed to view a profile but not private fields.

## Permission Changes
Consider existing sessions/caches when roles or permissions change. Define when permission changes take effect.

## Logging
Audit security-sensitive authorization changes and important denied/privileged operations without logging secrets.

## Verification
Test:
- anonymous access
- authenticated but unauthorized access
- owner vs non-owner
- cross-tenant access
- horizontal privilege escalation
- vertical privilege escalation
- guessed IDs
- admin functions
- stale permission/session behavior
