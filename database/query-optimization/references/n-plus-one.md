# N+1 Query Pattern

## Pattern
One query loads N parent records, followed by one query per parent.

Example:
1 query for users + N queries for each user's orders.

## Why It Matters
The database may execute hundreds/thousands of round trips even though the application appears to perform one logical operation.

## Fix Options
Choose based on data shape:
- join
- batched `IN` query
- ORM eager loading
- explicit data loader
- precomputed/read model

Do not blindly join everything; large joins can multiply rows and create over-fetching.

## Verification
Measure query count and latency before/after.
