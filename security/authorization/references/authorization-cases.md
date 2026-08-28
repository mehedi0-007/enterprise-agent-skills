# Authorization Cases

## Horizontal Escalation
User A accesses User B's resource.

Controls:
object-level authorization and tenant/ownership checks.

## Vertical Escalation
Normal user invokes an admin operation.

Controls:
explicit function-level permission.

## Cross-Tenant Access
User in tenant A accesses tenant B data.

Controls:
derive tenant context from authenticated identity and enforce tenant scope in data access.

## Property Escalation
Client submits `role=admin` or `ownerId=otherUser`.

Controls:
explicit mutation allow-list and server-side authorization.
