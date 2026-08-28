---
name: api-design
description: Design production-grade HTTP APIs with consistent resources, methods, status codes, validation, pagination, errors, idempotency, authorization, and compatibility. Use when creating, changing, reviewing, or documenting API endpoints.
---

# API Design

## Goal
Create APIs that are predictable for clients, semantically correct, secure, and maintainable.

## Resource Modeling
- Model stable business resources rather than implementation details.
- Prefer nouns for resource paths.
- Use nested resources only when the relationship is meaningful and bounded.
- Do not encode arbitrary database structure into the public API.

Examples:
- GET /users/{id}
- POST /orders
- PATCH /orders/{id}
- DELETE /sessions/{id}

## HTTP Semantics
Use HTTP methods according to their semantics. Use status codes consistently:
- 200 successful response
- 201 resource created
- 202 accepted for asynchronous processing
- 204 successful response with no content
- 400 malformed/invalid request
- 401 unauthenticated
- 403 authenticated but not allowed
- 404 resource not found
- 409 state/conflict condition
- 422 when the API convention uses semantic validation errors
- 429 rate limited
- 5xx server/dependency failure

Do not use 200 for every failure.

## Request Design
Validate at the boundary:
- syntax and types
- required fields
- allowed values
- size/range constraints
- cross-field constraints that are safe to validate without business state

Do not trust client-supplied identity, ownership, role, price, or other security-sensitive values.

## Response Design
- Keep response shapes consistent.
- Return only data the client is authorized to see.
- Avoid leaking internal database models.
- Define stable identifiers and timestamps.
- Avoid accidental serialization of secrets/internal fields.

## Pagination
Use pagination for potentially unbounded collections.
Offset pagination is acceptable for small/stable datasets and simple admin views.
Prefer cursor/keyset pagination when datasets are large, frequently changing, or require stable traversal.
Document ordering and cursor semantics.

## Filtering and Sorting
- Use explicit, allow-listed fields.
- Do not expose arbitrary SQL expressions.
- Define deterministic ordering for paginated results.
- Validate filter values and limits.

## Idempotency
For retryable state-changing operations such as payments, provisioning, or external side effects:
- define whether the operation is idempotent
- use an idempotency key where appropriate
- persist enough state to safely recognize retries
- ensure concurrent duplicate requests cannot produce duplicate side effects

## Errors
Use one consistent error envelope across the application.
Errors should provide a stable machine-readable code and safe human-readable message.
Do not expose stack traces, SQL, secrets, or internal service details.

## Authorization
Authorization is part of endpoint design, not an afterthought.
Check:
- authentication
- function-level permission
- object-level ownership/access
- property-level exposure where relevant

## Compatibility
Avoid breaking existing clients casually.
Consider:
- additive changes first
- field deprecation
- versioning only when necessary
- backward-compatible response/request evolution

## Verification
Before shipping an endpoint, check:
- method/path semantics
- validation
- authorization
- status codes
- response contract
- pagination/filtering behavior
- concurrency/idempotency
- error contract
- rate limiting
- observability
- API documentation
