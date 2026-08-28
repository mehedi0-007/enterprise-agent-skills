# Cardinality and Statistics

PostgreSQL estimates how many rows each part of a query returns and uses those estimates to calculate plan costs.

When estimates are badly wrong, investigate:
- stale statistics
- skewed distributions
- correlated columns
- complex predicates
- insufficient statistics detail

`ANALYZE` refreshes statistics. PostgreSQL also supports multivariate statistics for relationships that single-column statistics cannot represent.

Do not blindly raise statistics targets or force a plan; prove that estimation error is causing the performance issue.
