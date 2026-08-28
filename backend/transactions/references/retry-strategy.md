# Transaction Retry Strategy

## Retryable
Often includes transient serialization/deadlock/concurrency failures.

## Usually Not Retryable
- validation
- authentication/authorization
- business conflict
- permanent constraint violation
- malformed request

## Requirements
- bounded attempts
- exponential backoff/jitter
- retry the correct transaction unit
- no nested uncontrolled retry loops
- operation must be safe to repeat
- log retry-causing failures

Do not use retries to hide a deterministic bug.
