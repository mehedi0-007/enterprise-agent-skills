# Composite Index Design

Start from real query shapes.

Example workload:
```sql
WHERE tenant_id = ?
  AND status = ?
ORDER BY created_at DESC
LIMIT 50
```

Potential index:
`(tenant_id, status, created_at DESC)`

But validate:
- how often status is omitted
- whether status is selective
- other dominant query patterns
- write cost
- whether a separate index is necessary

Do not apply a universal "most selective first" rule without considering equality, range, ordering, and actual workload.
