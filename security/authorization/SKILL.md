---
name: authorization
description: Design and review server-side authorization for users, services, organizations, resources, and individual fields. Use for RBAC, tenant isolation, ownership, ABAC/ReBAC policies, admin operations, permission changes, sharing, impersonation, and access-control reviews.
---

# Authorization — Production Playbook

## 1. Mission

Authorization answers:

> "Is this principal allowed to perform this specific operation on this specific resource, in this specific context?"

A correct authorization design must account for:
- identity
- operation
- target resource
- tenant/organization
- relationship/ownership
- role/permission
- resource state
- sensitive fields
- service-to-service identity

Do not reduce authorization to:

```text
user.role === "admin"
```

---

## 2. Activation

Use when:
- protecting an endpoint
- introducing RBAC/permissions
- adding organizations/tenants
- adding sharing/delegation
- creating admin functions
- changing roles
- exposing new fields
- implementing impersonation
- adding service-to-service access
- reviewing privilege escalation risks

---

## 3. Separate the Concepts

### Authentication
Who is the principal?

### Authorization
What may the principal do?

### Tenant/Resource Scope
Which organization/resource may the principal access?

### Data Exposure
Which properties of the resource may the principal see/change?

A principal can be:
- authenticated
- a valid member of the organization
- allowed to read the resource
- but forbidden from changing a particular field

Treat these as separate decisions.

---

## 4. Authorization Decision Model

For every protected operation identify:

```text
Principal
   +
Action
   +
Resource
   +
Context
   ↓
Authorization decision
```

Context can include:
- tenant
- ownership
- resource state
- IP/network
- authentication strength
- time
- delegated relationship
- service identity

Example:

```text
Can Alice approve invoice 123?
```

is not merely:

```text
Does Alice have invoice:approve?
```

It may also require:
- Alice belongs to invoice tenant
- invoice is pending
- Alice is not the requester
- invoice amount is within Alice's authority
- required MFA/step-up is present

---

## 5. Deny by Default

If the system cannot establish permission, deny.

Do not interpret:
- missing role
- unknown permission
- malformed authorization context
- failed permission lookup

as success.

OWASP recommends deny-by-default, least privilege, and authorization checks on every request. citeturn931872search0

---

## 6. Every Request Means Every Request

Do not rely on:
- frontend hiding a button
- route structure
- "the UI never exposes this"
- a guard on only one route when alternate routes can reach the same resource
- previous authorization decisions cached forever

Authorization must exist at the actual server-side enforcement boundary.

---

## 7. Object-Level Authorization

Classic failure:

```text
GET /users/123/orders/456
```

The server checks:
```text
user is authenticated
```

but not:
```text
order 456 belongs to user/tenant
```

This creates IDOR/BOLA risk.

For every object reference ask:

```text
Does this principal have access to THIS object?
```

OWASP's API Security Top 10 identifies Broken Object Level Authorization as a major API risk. citeturn931872search2

---

## 8. Tenant Isolation

For multi-tenant applications, tenant boundary is a security boundary.

Prefer trusted context:

```text
authenticatedPrincipal.tenantId
```

over blindly trusting:

```text
request.body.tenantId
request.query.tenantId
```

Data access should enforce tenant scope where appropriate.

Example conceptual query:

```sql
SELECT *
FROM invoices
WHERE id = :invoiceId
  AND tenant_id = :trustedTenantId;
```

Do not fetch by ID first and "remember" to compare tenant afterward if the data-access boundary can safely enforce the scope directly.

---

## 9. Tenant Context Must Be Trusted

Never treat a client-selected tenant ID as proof of membership.

The system should derive/verify:
- current tenant
- membership
- role
- delegation

from authenticated identity and trusted server-side state.

When a user can switch organizations, treat the selected tenant as a requested context that must be authorized, not as a fact.

---

## 10. RBAC

Role-Based Access Control maps roles to permissions.

Example:

```text
Owner
  ├── billing:read
  ├── billing:write
  ├── members:manage
  └── settings:write

Member
  ├── billing:read
  └── data:write
```

Advantages:
- understandable
- easy to audit
- useful for stable organizational roles

Problems:
- role explosion
- exceptions
- resource-specific rules

Do not encode every business condition into roles.

---

## 11. ABAC

Attribute-Based Access Control evaluates attributes of:
- principal
- resource
- environment/action

Example:

```text
manager can approve expenses
IF
expense.tenantId == manager.tenantId
AND
expense.amount <= manager.approvalLimit
AND
expense.status == PENDING
```

ABAC is useful when access depends heavily on context rather than static roles.

Do not implement a complex policy engine when a few explicit domain rules are enough.

---

## 12. Relationship-Based Access

Some systems are naturally relationship-oriented:

```text
user → team
user → project
project → organization
document → project
```

Access might depend on those relationships.

Example:

```text
User is editor of Project
AND
Document belongs to Project
→ edit allowed
```

This can be more expressive than trying to put every relationship into roles.

Choose relationship-based modeling when relationships are core to the product, not because it is fashionable.

---

## 13. Role vs Permission

Avoid checking roles throughout business code:

```text
if role == "admin"
```

Prefer meaningful permissions/capabilities when possible:

```text
can("invoice.approve")
```

Why:
- roles can change
- multiple roles may grant the same permission
- permissions express capability more clearly

However, a role check can be valid when the business rule explicitly depends on a role rather than a capability.

---

## 14. Permission Composition

Define how permissions combine.

Clarify:
- any-of vs all-of
- role inheritance
- explicit denies
- resource ownership
- tenant restrictions
- feature flags
- time/state restrictions

Avoid implicit precedence rules that are difficult to audit.

If explicit deny exists, define exactly when it overrides grants.

---

## 15. Resource Ownership

Ownership checks are often the simplest correct policy.

Example:

```text
user owns document
→ read/write allowed
```

But be careful:
- transferred ownership
- delegated access
- shared resources
- team access
- admin overrides

Do not equate "createdBy" with permanent ownership without domain confirmation.

---

## 16. Field-Level Authorization

Resource access does not imply unrestricted field access.

Example:

```text
User can read employee profile
BUT
cannot read:
  salary
  internal_notes
  security flags
```

Likewise:

```text
User may update profile name
BUT
cannot update:
  role
  tenantId
  verified
  billingStatus
```

Use explicit field allow-lists for sensitive mutation surfaces.

---

## 17. Mass Assignment

Dangerous:

```json
{
  "name": "Alice",
  "role": "ADMIN",
  "tenantId": "other-tenant"
}
```

with generic object assignment.

Prefer mapping permitted fields explicitly:

```text
name
phone
avatar
```

and derive protected properties server-side.

OWASP's API Security guidance explicitly calls out broken object property-level authorization as a major API risk. citeturn931872search2

---

## 18. Function-Level Authorization

A user may be able to access a resource but not perform every function.

Examples:
- read invoice
- edit invoice
- approve invoice
- refund invoice
- export organization data
- manage members

Each privileged function requires explicit authorization.

Do not assume:
```text
canRead(invoice) → canApprove(invoice)
```

---

## 19. State-Dependent Authorization

Permission can depend on resource state.

Example:

```text
canRefund(order)
IF
  role allows refund
  AND order.status == PAID
  AND payment.provider allows refund
```

Be deliberate about where each rule belongs:
- permission system for capability
- domain policy for state/business constraints

Do not encode dynamic state conditions as static role assignments.

---

## 20. Separation of Duties

Some operations should require different principals.

Example:
- creator cannot approve own expense
- requester cannot approve own payout

This is not merely RBAC.

It is a business authorization rule:

```text
actor.id != resource.requesterId
```

Test these explicitly.

---

## 21. Admin / Superuser Boundaries

"Admin" must not automatically mean "bypass every security control."

Define:
- which resources admin can access
- whether cross-tenant access is allowed
- whether sensitive fields require extra permission
- whether admin actions are audited
- whether support impersonation is limited

For powerful operations consider:
- step-up authentication
- explicit reason
- audit trail
- time-limited access

---

## 22. Impersonation / Support Access

Impersonation is high-risk.

If supported, define:
- who can impersonate
- target restrictions
- scope
- duration
- visible impersonation state
- audit events
- ability to exit safely
- whether sensitive operations remain prohibited

Never let impersonation silently erase the original actor identity.

Audit:

```text
real_actor
→ impersonated_principal
→ action
→ resource
→ time
```

---

## 23. Service-to-Service Authorization

Machine identity needs authorization too.

Define:
- calling service identity
- allowed operations
- audience
- scopes/permissions
- tenant/resource boundaries

Do not treat:
```text
request came from internal network
```
as sufficient authorization.

---

## 24. Authorization in Database Queries

Where a scope is stable and directly tied to data ownership, enforcing it in the query can reduce accidental leaks.

Example:

```text
findInvoice(tenantId, invoiceId)
```

instead of:
```text
findInvoice(invoiceId)
```

then relying on every caller to remember tenant checks.

But query-level scoping does not replace business authorization.

The application may still need:
- role/permission
- state-dependent policy
- separation of duties

---

## 25. Authorization and Caching

Authorization results can become stale.

If permissions change:
- cached permission decisions may remain active
- resource caches may expose data
- long-lived sessions may retain old privileges

Define:
- cache TTL
- invalidation
- permission-change propagation
- whether sensitive operations require fresh authorization

Do not cache authorization decisions indefinitely.

---

## 26. Authorization and Transactions

For security-sensitive state changes, authorization and the protected mutation must be coordinated carefully.

Example:

```text
Check permission
↓
state changes before mutation
↓
perform action
```

If the relevant authorization depends on mutable state, make sure another transaction cannot change the state between the check and protected write in a way that invalidates the decision.

This can require:
- transaction
- row lock
- conditional update
- version check
depending on the domain.

---

## 27. Authorization and Async Jobs

Do not assume a job is authorized forever because it was queued by an authorized user.

Define whether:
- authorization is checked at enqueue time
- again at execution time
- based on original actor
- based on current resource state

For long-delayed jobs, rechecking current authorization/state may be necessary.

---

## 28. Fail Closed vs Fail Open

For protected operations:
- missing policy → deny
- authorization service unavailable → usually fail closed for sensitive operations
- incomplete resource context → deny

For low-risk analytics/UX features, a different fallback may be acceptable.

Make the choice explicit rather than accidental.

---

## 29. Testing Strategy

Test authorization negatively.

Minimum matrix:

| Principal | Resource | Expected |
|---|---|---|
| owner | own object | allow |
| user | another user's object | deny |
| tenant A | tenant B object | deny |
| member | admin action | deny |
| admin | allowed admin action | allow |
| requester | own approval | deny when separation required |
| authorized | protected field | according to policy |
| unauthorized | protected field | deny/hide |

Also test:
- guessed IDs
- alternate endpoints
- bulk endpoints
- exports
- background jobs
- webhooks
- cached responses
- stale permissions

---

## 30. Review Procedure

For each protected operation ask:

1. Who is the principal?
2. How was identity verified?
3. What exact action is being attempted?
4. What exact resource is targeted?
5. Which tenant does it belong to?
6. What permission grants the action?
7. What relationship/ownership applies?
8. What resource state applies?
9. Are individual fields more restricted?
10. Is this a privileged/admin path?
11. Can concurrent state changes invalidate the decision?
12. Is any permission decision cached?
13. Can the operation run asynchronously?
14. Is it audited?
15. What happens if authorization dependencies fail?

---

## 31. Common Attack Patterns

### IDOR / BOLA
Changing an ID to access someone else's resource.

### Mass Assignment
Submitting protected properties not intended for the update.

### Role Tampering
Changing client-controlled role/permission fields.

### Tenant Escape
Changing tenant IDs in query/body/path.

### Privilege Escalation
Normal user reaching admin functionality.

### Confused Deputy
A privileged service performs an operation on behalf of a caller without enforcing caller scope.

### Stale Authorization
Cached/long-lived permission remains after revocation.

### Bulk Endpoint Bypass
Single-object endpoint is protected, but bulk endpoint lacks equivalent checks.

### Async Authorization Gap
Request was authorized when queued but executes after resource permission/state changes.

---

## 32. Anti-Patterns

### Frontend-Only Authorization
Buttons hidden, server endpoint unprotected.

### Admin Means Everything
No explicit high-risk controls/audit.

### Tenant ID From Client
Trusting body/query tenant ID without deriving authorized context.

### Check Once, Use Everywhere
One route/guard assumed to protect all access paths.

### Role Explosion
Hundreds of narrowly encoded roles for business rules.

### Generic `isAdmin`
One boolean bypasses every policy.

### Authorization Inside Generic ORM Helper
A hidden policy makes reuse unsafe and difficult to reason about.

### Fail Open
Missing policy or service outage results in access.

### Cache Forever
Permission changes do not take effect predictably.

---

## 33. Verification Checklist

- [ ] every protected operation has a server-side decision
- [ ] object-level authorization enforced
- [ ] tenant scope trusted and enforced
- [ ] function-level permissions explicit
- [ ] sensitive fields protected
- [ ] mass assignment prevented
- [ ] admin/superuser scope defined
- [ ] separation-of-duties rules enforced
- [ ] async jobs reviewed
- [ ] cache staleness reviewed
- [ ] concurrency/state races reviewed
- [ ] failure behavior is explicit
- [ ] high-risk actions audited
- [ ] negative tests exist
- [ ] alternate/bulk endpoints reviewed

## Cross-Skill Routing
- For `api-security` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
