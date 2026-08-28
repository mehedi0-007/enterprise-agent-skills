# API Idempotency

## Use When
Retries can cause duplicate business effects and the operation can be identified safely.

High-value examples:
- payment initiation
- provisioning
- order creation
- sending an expensive external command

## Design
1. Client generates idempotency key.
2. Server authenticates and scopes the key to the principal/operation.
3. Server records request/result state durably.
4. First request executes.
5. Repeated equivalent request returns the recorded result or a defined conflict.
6. Concurrent duplicates are serialized/deduplicated.

## Important
An idempotency key alone is not enough if the database cannot safely enforce concurrent uniqueness or the external side effect is not idempotent.
