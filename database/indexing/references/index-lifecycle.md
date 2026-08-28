# Index Lifecycle

For each non-trivial index record:
- query/workload it supports
- expected benefit
- important predicates/order
- write/storage tradeoff
- migration/build strategy

Periodically review:
- size
- usage
- write overhead
- workload changes
- redundant indexes

An index should have an owner/understood reason, especially on critical tables.
