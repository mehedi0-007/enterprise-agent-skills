# Transactions and External Side Effects

A database transaction can atomically coordinate database changes, but not an external side effect.

For an order:
1. persist order state + outbox record in one transaction
2. commit
3. worker reads outbox
4. sends external notification/payment command
5. records result/retry state
6. reconciles failures

The exact design depends on whether the external provider has an idempotency mechanism and on business requirements.
