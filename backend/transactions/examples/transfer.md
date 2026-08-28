# Internal Transfer

Invariant:
source debit and destination credit must commit together.

Review:
- transaction boundary covers both updates
- rows/accounts are locked consistently if needed
- lock ordering is deterministic
- insufficient balance is enforced atomically
- deadlock/serialization retry policy is bounded
- external notifications are emitted via outbox/post-commit flow if reliability matters
