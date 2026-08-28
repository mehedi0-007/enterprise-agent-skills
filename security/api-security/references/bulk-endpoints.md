# Bulk Endpoint Review

Bulk APIs amplify risk.

Review:
- batch size
- per-item authorization
- duplicate items
- partial success vs atomicity
- transaction scope
- concurrency
- rate/quota cost
- audit volume

Never apply one authorization check to an entire batch when each item has independent access policy.
