# N+1 and Data Transfer

A request can be expensive even when each individual query is fast.

Review:
- number of SQL statements per request
- repeated queries
- unnecessary columns
- large JSON/text fields
- unbounded row counts
- duplicated parent data from joins
- aggregation performed in application code

Optimize both database execution and data movement.
