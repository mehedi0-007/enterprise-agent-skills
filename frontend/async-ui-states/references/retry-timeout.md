# Retry and Timeout

Timeout means the client stopped waiting; it does not prove server failure.

For safe reads, retry can be straightforward.

For non-idempotent writes:
- use idempotency
- query status
- inspect current resource state
- reconcile

Automatic retry needs bounded attempts, backoff/jitter, and permanent-error detection.
