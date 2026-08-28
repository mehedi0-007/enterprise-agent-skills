# Production Index Builds

Large index creation can affect production traffic and deployment timing.

Before choosing standard vs concurrent creation, assess:
- table size
- lock behavior
- maintenance window
- replication
- migration tooling
- failure/retry plan

`CREATE INDEX CONCURRENTLY` has different operational behavior and transaction restrictions. Use it deliberately, not automatically.
