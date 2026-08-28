---
name: api-design
description: Design, evolve, review, and verify production HTTP APIs. Use when creating or modifying endpoints, resource models, request/response contracts, pagination, filtering, sorting, idempotency, concurrency, errors, caching, webhooks, uploads, versioning, or API documentation.
---

# API Design — Production Playbook

## Mission
Design APIs that are understandable, secure, bounded, resilient to retries and partial failure, evolvable, observable, and testable.

Do not begin by writing controller code. Establish resource semantics, contracts, and failure behavior first.

## Activation
Use for:
- new endpoints/resources
- contract changes
- pagination/filtering/sorting
- retries/idempotency
- webhooks/uploads/async jobs
- error/status changes
- versioning/deprecation
- API security reviews

## Design Sequence
1. Understand the use case.
2. Identify resource/domain concept.
3. Identify actor and authorization boundary.
4. Define request/response contracts.
5. Choose HTTP semantics.
6. Define validation and limits.
7. Define collections/pagination.
8. Define errors.
9. Analyze retries/idempotency.
10. Analyze concurrency/consistency.
11. Consider caching/conditional requests.
12. Define observability.
13. Define tests and compatibility.
14. Review the complete contract before implementation.

## Resource Modeling
Model business resources, not database tables.

Prefer:
- /users
- /users/{userId}
- /orders/{orderId}
- /orders/{orderId}/items

Avoid verb-shaped CRUD paths such as /getUsers or /createUser.

Use nesting when the relationship is meaningful and bounded. Avoid deep nesting that makes authorization/discovery difficult.

For commands that are not naturally CRUD, use a clear action/command representation rather than artificial CRUD semantics.

## HTTP Semantics
Follow HTTP semantics rather than using methods as arbitrary verbs.

GET and HEAD are safe methods. PUT and DELETE are idempotent by HTTP semantics; POST is not inherently idempotent. Clients should not automatically retry non-idempotent operations unless application semantics make repetition safe. [RFC 9110]

Practical defaults:
- GET: retrieve
- POST: create or initiate processing/command where appropriate
- PUT: replace a known resource representation when replacement semantics fit
- PATCH: partial modification with explicitly defined semantics
- DELETE: remove/deactivate according to the domain contract

## Status Codes
Choose status from the actual outcome.

Typical success:
- 200 representation returned
- 201 resource created
- 202 accepted for asynchronous processing
- 204 success with no body

Typical failure:
- 400 malformed/invalid request
- 401 authentication required/invalid
- 403 authenticated but not permitted
- 404 resource unavailable under the API's chosen semantics
- 409 state/conflict
- 422 semantic validation when the API deliberately distinguishes it
- 429 rate/resource limit
- 5xx server/dependency failure

Do not return 200 for application failures.

Choose 403 vs 404 consistently; hiding existence may be appropriate for sensitive resources.

## Request Contracts
Define:
- required/optional fields
- types/formats
- length/range
- enums
- collection limits
- null vs omitted semantics
- cross-field rules

Never trust client-supplied identity, tenant, ownership, role, price, verification, or privilege state.

## Response Contracts
Responses are public contracts.
Use stable field names/types and deliberate representations.
Return only authorized data.
Do not serialize ORM/database entities blindly.

Never expose passwords, tokens, secrets, stack traces, SQL, or internal infrastructure details.

## Collections and Pagination
Every collection must answer:
1. Can it grow without bound?
2. What is the server maximum?
3. How does the client continue?
4. Is ordering deterministic?
5. What filters/sorts are supported?
6. What happens while data changes?

Server-side pagination should be considered from the beginning; Microsoft guidance notes that introducing it later can be breaking. [Microsoft REST API Guidelines]

Offset/page pagination is reasonable for small/stable or page-number-oriented views.
Consider cursor/keyset pagination for large, frequently changing datasets or deep traversal.

Paginated ordering must be deterministic. Use a stable tie-breaker when the main sort field is not unique.

Always enforce a server-side maximum page size.

## Filtering and Sorting
Allow-list filter and sort fields.
Do not expose arbitrary SQL, ORM expressions, or unrestricted operators.

Define:
- value types/ranges
- authorization scope
- index expectations when important
- pagination interaction
- default deterministic sort

## Idempotency
Ask:
- Can the client lose the response after the server succeeds?
- Can retry create harmful duplicate effects?
- Is there an external side effect?
- Can a unique business key deduplicate?
- Is an Idempotency-Key appropriate?
- How are concurrent duplicate requests handled?
- What does a retry receive?

For high-risk POST operations such as payments, provisioning, or order creation, define durable idempotency state and concurrency protection.

HTTP method idempotency and application-level idempotency are different concepts. [RFC 9110]

## Concurrency and Conditional Requests
For stale-write risk, consider:
- ETag/If-Match
- version columns
- atomic state transitions
- database constraints
- transactions/locks

Use the simplest control that protects the invariant.

## Authorization
Define:
- who may call the endpoint
- which object they may access
- which fields they may view/change
- tenant scope
- privileged actions

Authentication is not authorization.
Knowing an object ID does not prove access.

OWASP identifies authorization as a dominant API security concern. [OWASP API Security Top 10]

## Validation and Business Rules
Boundary validation checks structural validity.
Business/domain logic checks current state, eligibility, ownership, and policy.
Do not put database-dependent business policy in DTO validators merely because the framework makes it convenient.

## Error Contract
Treat errors as part of the public API contract.

Prefer:
- stable machine-readable code
- safe human-readable message
- correlation/request ID when useful
- field-level detail for validation

Clients should branch on codes, not message prose.

Never expose stack traces, SQL, secrets, provider errors, or internal topology.

## Retry and Timeout
For external dependencies define:
- client/server timeout expectations
- retryable vs non-retryable failures
- retry count and backoff
- idempotency
- partial failure behavior

Never recommend automatic retries for potentially non-idempotent side effects without a safety mechanism.

## Async Operations
If work may outlive a normal request:
- return 202 when appropriate
- expose job/status state
- define completion/failure states
- define cancellation if supported
- avoid holding HTTP connections open unnecessarily

## Caching
Before caching define:
- cacheability
- freshness
- invalidation
- authorization interaction
- stale behavior
- cache key
- content negotiation/Vary behavior

Do not accidentally cache private/authenticated data in shared caches.

Consider conditional requests for bandwidth optimization and optimistic concurrency.

## Webhooks
Define:
- authenticity/signature verification
- replay protection
- idempotent processing
- duplicate delivery
- ordering assumptions
- acknowledgement timing
- retry semantics
- reconciliation/dead-letter strategy

Treat webhook payloads as untrusted until authenticated.

## File Uploads
Define:
- maximum size
- accepted types
- authorization
- storage
- filename handling
- content/malware scanning where appropriate
- download authorization
- retention/lifecycle
- asynchronous processing if required

Never trust client filename/MIME alone.

## Versioning and Evolution
Prefer additive compatible changes where possible.

Potential breaking changes:
- remove/rename field
- type change
- nullability/requiredness change
- semantic change
- error/status contract change
- unexpected mandatory pagination
- material rate/latency/concurrency behavior changes

When breaking change is required:
- choose a strategy deliberately
- publish migration guidance
- define deprecation/sunset policy
- measure remaining consumers
- remove only under agreed criteria

## Performance
Review:
- payload size
- query count/N+1
- expensive filtering/sorting
- pagination
- serialization
- dependency fan-out
- caching

Do not add caching before identifying the actual bottleneck.

## Observability
Important endpoints should expose enough telemetry to answer:
- request volume
- latency
- errors
- dependency failures
- rate limiting
- important business outcomes

Never log secrets or sensitive payloads.

## Testing
Test important endpoints for:
- success
- malformed input
- validation
- authentication/authorization
- not found
- conflict
- rate limit
- dependency failure
- timeout
- retry/idempotency
- concurrency
- response contract

For collections, test page boundaries, empty/no-result behavior, deterministic ordering, invalid filters/sorts, and data changes while paging.

## Review Checklist
Before implementation:
- [ ] resource/operation semantics
- [ ] actor + authorization
- [ ] request contract
- [ ] response contract
- [ ] validation
- [ ] status codes
- [ ] pagination/limits
- [ ] error contract
- [ ] retry/idempotency
- [ ] concurrency
- [ ] caching/conditional requests
- [ ] external side effects
- [ ] security abuse cases
- [ ] observability
- [ ] compatibility
- [ ] tests

After implementation:
- [ ] implementation matches contract
- [ ] authorization enforced server-side
- [ ] limits enforced
- [ ] errors safe/stable
- [ ] tests pass
- [ ] docs updated
- [ ] telemetry exists
- [ ] performance measured where relevant

## References
Load when needed:
- references/idempotency.md
- references/pagination.md
- references/compatibility.md
- references/error-contract.md
