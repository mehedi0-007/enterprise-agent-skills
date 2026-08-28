---
name: error-handling
description: Design consistent and safe error handling across backend applications. Use when creating endpoints, services, integrations, validation, exception filters, retries, or reviewing failure behavior.
---

# Error Handling

## Purpose
Make failures predictable for clients, diagnosable for operators, and safe from information leakage.

## Error Taxonomy
Distinguish at least:
- input/validation failure
- authentication failure
- authorization failure
- resource not found
- conflict/state violation
- rate limit
- dependency failure
- internal/unexpected failure

Do not collapse every failure into HTTP 500.

## API Contract
Use a consistent error envelope. A useful contract contains:
- stable machine-readable error code
- safe message
- request/correlation identifier when available
- field-level validation details when applicable

Do not expose:
- stack traces
- SQL text
- internal hostnames
- secrets
- provider credentials
- sensitive object details

## Boundary Principle
Handle an error at the layer that has enough context to decide what it means.

Examples:
- repository detects unique-key violation -> translate to a meaningful persistence/application error
- service decides duplicate email means a business conflict
- controller maps the stable application error to HTTP 409

Do not add broad try/catch blocks that simply rethrow unchanged.

## External Dependencies
For network/API calls:
- set appropriate timeouts
- distinguish retryable from non-retryable failures
- use bounded retries with backoff when appropriate
- make retries safe through idempotency
- record dependency failures for observability

Never retry indefinitely or blindly retry non-idempotent operations.

## Logging
Log useful diagnostic context:
- operation
- correlation/request ID
- safe resource identifiers
- dependency
- error class/code
- timing where helpful

Never log passwords, OTP values, access tokens, refresh tokens, API keys, or full sensitive payloads.

## Unexpected Failures
Unexpected failures should be:
1. safely reported to the client
2. logged with diagnostic context
3. measurable/alertable
4. non-destructive where possible

Do not swallow exceptions because "the request can continue" unless that behavior is deliberate and documented.

## Verification
Test:
- expected client errors
- authorization failures
- duplicate/conflict behavior
- dependency timeouts
- retry behavior
- unexpected exception path
- safe error serialization
