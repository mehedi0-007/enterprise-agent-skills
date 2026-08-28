# Specialized Indexes

## GIN
Often useful for JSONB, arrays, and operator classes that benefit from inverted indexes.

## GiST
Useful for specialized operator families such as ranges/spatial workloads.

## BRIN
Useful for very large tables where column values correlate with physical row order, often append-heavy data.

Choose from operator/workload requirements, then verify with plans and measurements.
