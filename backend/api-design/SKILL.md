---
name: api-design
description: Design and review production HTTP APIs. Use when creating or modifying endpoints, resource contracts, pagination, filtering, errors, idempotency, webhooks, uploads, caching, or compatibility behavior.
---

# API Design

## Mission
Make APIs predictable, secure, evolvable, and semantically correct.

## Before Designing
Determine:
- resource/domain concept
- actor and authorization
- operation semantics
- mutability
- retryability
- expected cardinality
- consistency requirements
- external side effects
- compatibility requirements

## Resource Modeling
Model business resources, not tables or implementation details.
Use nouns and stable identifiers.
Use nesting only when the relationship is meaningful and bounded.

## Method/Status Matrix

| Operation | Typical method | Typical success |
|---|---|---|
| Fetch | GET | 200 |
| Create | POST | 201 |
| Replace | PUT | 200/204 |
| Partial update | PATCH | 200/204 |
| Delete | DELETE | 204 |
| Accepted async work | POST/other | 202 |

Use status codes that communicate semantics. Keep the project's error contract consistent.

## Collection Design
Potentially unbounded collections need:
- pagination
- deterministic ordering
- explicit maximum page size
- bounded filters
- safe allow-listed sort fields

Use offset pagination for simple/small cases. Consider cursor/keyset pagination for large or high-churn datasets.

## Idempotency Decision

Ask:
1. Can a client/network retry?
2. Can duplicate execution cause harm?
3. Does the operation create an external side effect?
4. Can a unique business key enforce deduplication?
5. Is an idempotency key appropriate?
6. Where is idempotency state stored?
7. What does a duplicate request return?

Do not claim POST is safe merely because the handler "usually" creates one object.

## Error Contract
Use stable machine-readable error codes and safe messages.
Include field errors where useful.
Never expose SQL, stack traces, secrets, or internal infrastructure.

## Authorization
Check:
- authentication
- function-level permission
- object-level access
- tenant scope
- property-level exposure

Client-side controls never replace server-side authorization.

## Compatibility
Prefer additive evolution. Consider old clients and rolling deployments. Deprecate before removing when practical.

## Caching
Only add caching after defining:
- cache key
- freshness
- invalidation
- authorization interaction
- stale behavior
- failure fallback

## Webhooks
Define signature verification, replay handling, idempotent processing, timeout/retry semantics, and delivery observability.

## Anti-patterns
- `/getUsers`
- arbitrary SQL exposed through query parameters
- unbounded list endpoints
- 200 responses for application failures
- returning ORM entities blindly
- silently changing response semantics
- trusting client tenant/user IDs

## Verification
Review request/response schemas, status codes, authorization, limits, retries, idempotency, compatibility, documentation, and tests.
