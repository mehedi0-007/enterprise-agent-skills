# API Idempotency

A request can succeed on the server even when the client never receives the response. A retry can therefore duplicate side effects.

When an idempotency key is appropriate:
1. Scope it to the principal and logical operation.
2. Persist state durably.
3. Protect the key with a uniqueness/concurrency mechanism.
4. Make concurrent duplicates safe.
5. Define behavior for a reused key with a different payload.
6. Return a deterministic result/conflict.

For external side effects, coordinate application/database idempotency with the provider's own idempotency mechanism or an outbox/reconciliation strategy.

An idempotency key without concurrency protection is incomplete.
