# Tenant Orders

Query:
```sql
SELECT id, status, created_at
FROM orders
WHERE tenant_id = $1
  AND status = 'OPEN'
ORDER BY created_at DESC, id DESC
LIMIT 50;
```

Review:
1. Is this a hot query?
2. How large is an average tenant?
3. How many rows are OPEN?
4. Is deterministic ordering required?
5. Does an existing index already support it?
6. Would `(tenant_id, status, created_at, id)` materially improve the plan?
7. What is the write cost?

Do not add the index until the query plan/workload justifies it.
