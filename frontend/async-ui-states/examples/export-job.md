# Export Job

1. POST creates durable export job.
2. UI shows queued.
3. Job becomes processing.
4. UI polls or receives completion notification.
5. Completed → download.
6. Failed → retry/recovery.

If POST times out, do not blindly create another export. Use idempotency or status reconciliation.
