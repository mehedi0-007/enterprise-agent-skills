# N+1 Example

Bad:
1. query 100 users
2. loop users
3. query orders for each user

Potential result: 101 queries.

Better options:
- one join
- one batched query
- data loader
- read model

Choose based on the shape of the returned data and whether a join would multiply rows.
