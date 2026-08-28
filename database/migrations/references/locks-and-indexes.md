# Locks and Index Builds

Normal PostgreSQL index creation can block writes for the duration of the build. `CREATE INDEX CONCURRENTLY` permits normal writes but has additional restrictions and operational behavior.

Before choosing:
- table size
- traffic
- maintenance window
- migration transaction model
- replication
- disk capacity

Always verify the resulting index state after failure/recovery procedures where relevant.
