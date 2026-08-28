# Idempotent Workers

Assume at-least-once delivery.

A robust worker:
1. identifies the logical operation
2. checks or atomically records processing state
3. performs safe work
4. records durable completion
5. can safely receive the same job again

External APIs should use provider idempotency where available.

Never use an in-memory "processed IDs" set as durable deduplication.
