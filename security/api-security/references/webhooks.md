# Webhook Security

Verify provider authenticity before privileged processing.

Then:
- validate schema
- identify event ID
- enforce replay window/deduplication
- process idempotently
- acknowledge within provider expectations
- move long work async when appropriate
- monitor failures/retries
- reconcile missing/duplicate events
