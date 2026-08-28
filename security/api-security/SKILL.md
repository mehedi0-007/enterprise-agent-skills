---
name: api-security
description: Threat-model, design, implement, and review secure APIs and API-facing workflows. Use for new or modified endpoints, webhooks, file uploads, external integrations, sensitive business actions, bulk operations, and API abuse/security reviews.
---

# API Security — Production Playbook

## 1. Mission

An API is an untrusted boundary.

For every endpoint, assume:
- inputs can be malicious
- requests can be repeated
- requests can be concurrent
- clients can skip the UI
- object identifiers can be guessed/modified
- payloads can be oversized
- dependencies can fail
- callers can automate requests at high volume

The goal is to preserve:
- confidentiality
- integrity
- availability
- authorization boundaries
- predictable resource usage

---

## 2. Activation

Use when:
- creating/modifying an endpoint
- exposing a new resource
- implementing bulk actions
- adding file uploads
- receiving webhooks
- fetching caller-provided URLs
- consuming external APIs
- adding expensive business operations
- changing API authentication/authorization
- reviewing abuse/security risk

---

## 3. Threat Model Before Code

For each endpoint identify:

### Principal
Who is calling?
- anonymous
- user
- admin
- service
- webhook provider

### Asset
What could be exposed/changed?
- PII
- credentials
- money
- permissions
- tenant data
- files
- internal metadata

### Action
What can the endpoint do?
- read
- create
- mutate
- delete
- trigger external side effect
- start expensive computation

### Trust Boundary
What input is attacker-controlled?
- body
- query
- path
- headers
- URL
- file
- webhook payload

### Abuse
Can the endpoint be:
- enumerated
- replayed
- brute-forced
- scraped
- amplified
- used for SSRF
- used for privilege escalation
- used to consume excessive resources?

---

## 4. OWASP API Security Top 10

Review every important API against the OWASP API Security Top 10 (2023):

1. Broken Object Level Authorization
2. Broken Authentication
3. Broken Object Property Level Authorization
4. Unrestricted Resource Consumption
5. Broken Function Level Authorization
6. Unrestricted Access to Sensitive Business Flows
7. Server-Side Request Forgery
8. Security Misconfiguration
9. Improper Inventory Management
10. Unsafe Consumption of APIs

OWASP's API guidance emphasizes that authorization failures are a recurring source of API compromise and that security controls must be enforced server-side. citeturn977525search2turn977525search0

Do not treat this list as a substitute for application-specific threat modeling.

---

## 5. Object-Level Authorization

If the request contains:

```text
/resource/{id}
```

the endpoint must establish access to that specific object.

Bad:

```text
authenticate(user)
load(id)
return object
```

Better:

```text
authenticate(user)
load object within trusted scope
verify object access
return authorized representation
```

For multi-tenant systems, prefer enforcing trusted tenant scope in the query where practical.

Test:
- own object
- another user's object
- another tenant's object
- guessed/sequential IDs
- bulk object lists

---

## 6. Property-Level Authorization

Do not let generic request mapping update protected properties.

Suspicious fields:
- role
- tenantId
- ownerId
- accountStatus
- verified
- permissions
- price
- approval state

Prefer explicit writable field mapping.

For responses, filter sensitive fields according to principal permissions.

---

## 7. Function-Level Authorization

Every privileged function needs explicit authorization.

Examples:
- refund
- export
- delete organization
- promote member
- change billing owner
- generate API credentials
- impersonate user

Do not assume:
```text
canRead(resource) → canDelete(resource)
```

---

## 8. Resource Consumption

Every endpoint needs resource bounds.

Review:
- request body size
- file size
- array/batch size
- pagination size
- query complexity
- sorting/filtering
- export size
- expensive computations
- authentication attempts
- webhook processing
- polling frequency

OWASP lists unrestricted resource consumption as a major API risk. citeturn977525search2

Use:
- maximum sizes
- pagination
- quotas
- rate limits
- concurrency limits
- timeouts
- job queues for expensive work

Do not rely on infrastructure rate limiting alone if the application needs user/tenant-specific quotas.

---

## 9. Rate Limiting Strategy

Rate limits should reflect abuse potential.

Different operations may need different policies:

### Login/OTP
Very strict.

### Normal reads
Moderate.

### Search
Bounded request rate + query cost limits.

### Export/report
Strict concurrency and long-job controls.

### Password reset
Strict per-account/per-network limits.

### Payment
Very strict + idempotency + business safeguards.

Consider dimensions:
- IP/network
- account/user
- tenant
- API key/client
- endpoint
- business operation

Do not rely on IP alone; attackers can distribute requests.

Do not use a single universal limit for every endpoint.

---

## 10. Sensitive Business Flows

Some endpoints are technically valid but easy to abuse at the business level.

Examples:
- resend OTP
- send invitations
- generate discounts
- vote/like
- referral creation
- password reset
- create free trials
- expensive search/export

For sensitive business flows ask:
- can automation cause financial/reputational damage?
- can a user repeat the action at scale?
- is there a per-user/tenant quota?
- does it require CAPTCHA/step-up/verification?
- does it need idempotency?
- should it have a daily or concurrency limit?

OWASP explicitly identifies unrestricted access to sensitive business flows as an API risk. citeturn977525search2

---

## 11. Input Validation

Validate:
- body
- path
- query
- headers when used as structured input
- file metadata
- webhook payload schema

Set:
- length limits
- numeric bounds
- enum allow-lists
- nested object depth/size limits where relevant

Validation prevents malformed input but is not authorization.

---

## 12. Injection

Protect database and other interpreters by using:
- parameterized SQL
- ORM parameterization
- safe command construction
- output encoding appropriate to the target context

Never concatenate attacker-controlled strings into:
- SQL
- shell commands
- template expressions
- code
- browser-executable output

Do not assume "the ORM makes us safe" if raw-query escape hatches exist.

---

## 13. SSRF

If an API accepts a URL and the server fetches it, treat it as high risk.

Threats include:
- internal service access
- cloud metadata access
- localhost/admin endpoint access
- credential theft
- network pivoting

Controls should be layered:
1. allow only required schemes
2. prefer allow-listed destination domains when product semantics permit
3. resolve and validate destination safely
4. block private/link-local/loopback ranges as appropriate
5. control redirects
6. restrict outbound network egress
7. set strict timeouts/body limits

OWASP identifies SSRF as a major API category. citeturn977525search2

Do not rely on a naive string check such as:
```text
startsWith("https://")
```

---

## 14. Webhooks

A webhook endpoint is an untrusted input boundary until authenticity is established.

Review:
- signature verification
- timestamp/replay controls
- event ID
- duplicate delivery
- ordering
- schema validation
- tenant mapping
- processing timeout
- acknowledgement timing
- retry behavior
- reconciliation

Never let an unauthenticated webhook directly execute a privileged operation.

---

## 15. Webhook Replay

Even a valid signed webhook can be captured and replayed.

Use provider-supported:
- event IDs
- timestamps
- replay windows
- idempotency/deduplication

The handler should be safe if the same event arrives multiple times.

---

## 16. Unsafe External API Consumption

When consuming another API:
- validate its response
- set timeouts
- enforce response size limits
- handle malformed data
- do not blindly trust fields
- consider SSRF when URLs are returned
- validate certificates/TLS normally
- define retry/backoff behavior

OWASP's "Unsafe Consumption of APIs" category exists because your service inherits risks from data/services it blindly trusts. citeturn977525search2

Treat third-party data as external input.

---

## 17. File Uploads

For upload endpoints:
- enforce authorization
- cap size
- validate type
- inspect content where security policy requires
- generate server-side storage names
- avoid serving uploaded content from a privileged executable origin
- control download authorization
- apply retention/lifecycle policy

Do not trust:
- filename
- extension
- client MIME type

as the sole security check.

---

## 18. Bulk Endpoints

Bulk operations multiply both performance and security impact.

Review:
- maximum batch size
- per-item authorization
- partial success semantics
- atomic vs best-effort behavior
- duplicate entries
- rate limits
- audit events

Do not authorize a bulk request because the caller is allowed to access only one item in the batch.

---

## 19. API Enumeration and Inventory

Maintain awareness of:
- public endpoints
- admin endpoints
- internal endpoints
- deprecated versions
- debug/test routes
- webhooks
- undocumented operational routes

OWASP includes improper inventory management because forgotten/deprecated endpoints can remain exposed without equivalent security controls. citeturn977525search2

Do not treat `/v1` and `/v2` as safe merely because one is deprecated.

---

## 20. Error Responses

Security-sensitive APIs should avoid leaking:
- whether secrets are correct
- whether sensitive objects exist
- stack traces
- SQL
- internal topology
- dependency credentials

Keep a stable machine-readable error contract.

However, do not hide every error behind generic 500 responses; clients need stable semantics.

---

## 21. Authentication Dependencies

Do not assume middleware alone makes an endpoint safe.

Review:
- token/session validation
- issuer/audience
- token lifetime
- CSRF where cookie-based
- service identity
- API keys
- key rotation

Use the `security/authentication` skill for detailed credential lifecycle design.

---

## 22. Authorization Dependencies

Use `security/authorization` for:
- RBAC
- tenant isolation
- object-level authorization
- field-level authorization
- admin boundaries
- delegation

This skill focuses on the API threat boundary and abuse behavior.

---

## 23. Idempotency

For operations that may be retried:
- define a logical operation identity
- use idempotency keys where appropriate
- protect concurrent duplicates
- define reuse-with-different-payload behavior
- coordinate external provider idempotency

Do not add idempotency to every POST automatically.

Prioritize operations where duplicate execution can cause material harm.

---

## 24. Timeouts and Resource Limits

Every network boundary should have a bounded timeout.

For user-controlled expensive operations, also bound:
- execution time
- DB query complexity
- batch count
- response size
- worker concurrency

A timeout should fail safely and predictably.

Do not increase timeouts simply because the endpoint is slow; investigate the bottleneck.

---

## 25. API Security Headers / Transport

Security requirements depend on the transport/client architecture.

For browser-facing APIs review:
- HTTPS
- cookie flags
- CORS
- CSRF
- content type
- browser security headers where relevant

Do not use CORS as an authorization mechanism.

CORS controls browser cross-origin behavior; server-side authorization remains mandatory.

---

## 26. API Keys

If API keys are supported:
- hash/store safely where appropriate
- show only once when policy requires
- assign scopes
- define expiration/rotation/revocation
- associate with owner/tenant
- rate-limit
- audit creation/use/revocation
- never put keys in URLs unless unavoidable and explicitly reviewed

---

## 27. Auditability

For sensitive operations record safe audit events:
- actor/service identity
- operation
- resource
- tenant
- timestamp
- outcome
- request/correlation ID
- source context where appropriate

Do not log credentials, raw tokens, OTPs, or sensitive payloads.

Audit logging is not a substitute for authorization; it provides accountability/evidence.

---

## 28. Security Testing

For important endpoints test:
- unauthenticated access
- unauthorized object access
- cross-tenant access
- property injection
- privilege escalation
- malformed payloads
- oversized payloads
- rate limits
- brute force
- replay
- duplicate requests
- SSRF attempts
- malicious files
- webhook replay
- dependency timeout/failure

Security tests should include negative cases.

---

## 29. Review Decision Tree

```text
New/changed API
      ↓
Who is calling?
      ↓
What asset is protected?
      ↓
What action occurs?
      ↓
Object authorization?
      ↓
Property authorization?
      ↓
Tenant boundary?
      ↓
Can it be automated/abused?
      ↓
Resource/rate limits?
      ↓
Can it be replayed?
      ↓
Idempotency?
      ↓
Any URL/file/external input?
      ↓
SSRF/upload/external API risk?
      ↓
Any privileged business flow?
      ↓
Audit/observability?
      ↓
Negative security tests?
```

---

## 30. Anti-Patterns

### Authenticated = Safe
No object/function authorization.

### CORS = Security
CORS is not server authorization.

### IP Rate Limit Only
Fails against distributed abuse.

### Global Rate Limit
Does not account for operation risk/cost.

### URL Fetch Without SSRF Model
Classic server-side request forgery risk.

### Signed Webhook = Exactly Once
Authenticity does not prevent replay/duplicates.

### Generic DTO Assignment
Can enable property-level privilege escalation.

### Validate Only Body
Ignores path/query/header/file attack surfaces.

### Deprecated Means Safe
Forgotten API versions remain exposed.

### Internal Endpoint Trust
Internal network/service origin treated as authorization.

### Bulk Authorization Once
One authorized item makes the entire batch trusted.

---

## 31. Verification Checklist

- [ ] threat model documented
- [ ] authentication validated
- [ ] object-level authorization enforced
- [ ] function-level authorization enforced
- [ ] property-level input/output access controlled
- [ ] tenant boundary enforced
- [ ] inputs bounded/validated
- [ ] resource consumption bounded
- [ ] rate-limit strategy chosen per risk
- [ ] idempotency/replay behavior defined
- [ ] SSRF reviewed for server-side URL fetches
- [ ] file upload controls reviewed
- [ ] webhook authenticity/replay handled
- [ ] third-party API responses treated as untrusted
- [ ] deprecated/internal endpoints inventoried
- [ ] safe errors
- [ ] audit events for sensitive operations
- [ ] negative security tests
- [ ] failure/timeout behavior tested

## References
- `references/owasp-api-top10.md`
- `references/rate-limits.md`
- `references/ssrf.md`
- `references/webhooks.md`
- `references/bulk-endpoints.md`

## Review Procedure

1. Identify endpoint principal, asset, action, and trust boundaries.
2. Check applicable OWASP API risks.
3. Review authentication/authorization, object/property access, and tenant scope.
4. Review resource abuse, SSRF, uploads, webhooks, replay, and external APIs.
5. Review errors, auditability, and negative tests.
6. Route detailed controls to specialized security skills.

## Verification Checklist

- [ ] object/function/property authorization reviewed
- [ ] tenant isolation reviewed
- [ ] resource abuse/rate limits reviewed
- [ ] SSRF/upload/webhook risks reviewed where applicable
- [ ] replay/idempotency reviewed
- [ ] third-party responses treated as untrusted
- [ ] negative security tests exist

## Cross-Skill Routing
For identity, session, token, and recovery lifecycle, coordinate with `security/authentication`.
For object, tenant, function, and property authorization, coordinate with `security/authorization`.
For OWASP-oriented review orchestration, coordinate with `security/owasp`.
For credentials/keys used by the API or integrations, coordinate with `security/secrets-management`.
