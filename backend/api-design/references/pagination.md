# Pagination

## Offset
Example: `/orders?page=4&limit=50`
Good for direct page navigation and modest/stable datasets.
Risks include deep offset work and shifts caused by inserts/deletes.

## Cursor/Keyset
Example: `/orders?limit=50&cursor=...`
Good for large/high-churn datasets and continuous traversal.
The cursor should be opaque to clients and encode enough ordering state.

## Ordering
Use deterministic ordering and a unique tie-breaker when necessary.

## Limits
Always enforce a server maximum.
Do not permit unbounded collection responses.

## Traversal
Document whether filter/sort choices remain fixed throughout a cursor traversal.
