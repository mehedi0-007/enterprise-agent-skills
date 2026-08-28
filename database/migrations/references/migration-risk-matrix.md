# Migration Risk Matrix

| Change | Typical risk |
|---|---|
| New nullable column | Low/Medium |
| New table | Low/Medium |
| Small additive index | Medium |
| Large index build | Medium/High |
| Large backfill | High |
| New unique constraint on dirty data | High |
| Type conversion | Medium/High |
| Rename | High under rolling deploys |
| Drop column/table | High |
| Destructive data transform | Critical |

Risk depends on workload, table size, traffic, dependencies, and deployment strategy.
