---
name: error-handling
description: Build safe, consistent, diagnosable backend failure handling. Use for API errors, exceptions, validation, database conflicts, external dependencies, retries, and logging.
---

# Error Handling

## Error Categories
Distinguish:
- validation
- authentication
- authorization
- not found
- conflict
- rate limit
- dependency failure
- internal failure

Map known application failures consistently.

## Boundary Rule
Translate an error when the current layer has enough context to give it stable meaning.

Do not catch errors just to rethrow the same error.

## External Dependencies
For network calls define:
- timeout
- retryability
- retry count
- backoff
- idempotency
- fallback
- observability

Never retry blindly, indefinitely, or across non-idempotent side effects.

## Database Errors
Translate known constraint/conflict failures into application semantics. Keep database details in logs/diagnostics, not API responses.

## Logging
Log operation, correlation ID, safe identifiers, error class/code, and useful timing/context.
Never log passwords, OTPs, tokens, API keys, or secrets.

## Client Contract
Return a stable error code and safe message. Validation errors may include field-level details.

## Verification
Test expected errors, conflicts, dependency timeouts, retries, unexpected exceptions, serialization, and information leakage.
