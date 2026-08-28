# Partial, Expression, and Covering Indexes

## Partial
Use a meaningful subset predicate to make a smaller/focused index.

## Expression
Use when the same deterministic expression is repeatedly queried.

## INCLUDE/Covering
Use included columns only when avoiding heap access materially benefits a hot query and index size remains reasonable.

All three require workload evidence; they are not automatic upgrades over ordinary B-tree indexes.
