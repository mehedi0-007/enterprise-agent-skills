# Large Table Example

Query:
`SELECT * FROM events WHERE tenant_id = ? ORDER BY created_at DESC LIMIT 50`

Review:
- tenant scope
- selected columns
- deterministic ordering
- expected tenant cardinality
- index matching tenant + ordering
- large payload columns
- pagination/cursor strategy

Do not assume the correct index until the plan and workload are inspected.
