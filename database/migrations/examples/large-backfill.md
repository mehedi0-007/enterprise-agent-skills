# Large Backfill

Requirement:
populate `normalized_email` for 100M users.

Avoid one unbounded update.

Plan:
- add nullable column
- deploy compatible writes
- process bounded primary-key ranges
- commit each batch
- record progress
- throttle when database/replication load rises
- validate count + correctness
- switch reads
- add final constraint/index only after data is ready
- remove temporary code later
