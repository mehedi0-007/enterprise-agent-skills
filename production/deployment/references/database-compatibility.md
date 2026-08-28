# Database Compatibility

For rolling deploys, old and new app versions may coexist.

Use expand/contract:
1. add compatible schema
2. deploy compatible readers/writers
3. migrate/backfill
4. verify
5. switch
6. contract later

Do not drop/rename data structures while old consumers can still reference them.
