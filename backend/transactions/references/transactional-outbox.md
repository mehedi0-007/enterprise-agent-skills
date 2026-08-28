# Transactional Outbox

Use when a database state change must reliably trigger a message/event.

Atomic transaction:
1. update business state
2. insert outbox event
3. commit

Async publisher:
1. read committed outbox rows
2. publish
3. mark delivered/delete
4. retry failures

Consumers must tolerate duplicate delivery through idempotent processing or deduplication.

The outbox does not provide magical exactly-once delivery across all systems.
