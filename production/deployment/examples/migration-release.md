# Migration + Rolling Release

Requirement: rename a production field.

Release sequence:
1. expand schema
2. deploy compatibility code
3. backfill
4. verify parity
5. deploy new-read-only path
6. drain old consumers
7. contract later

Do not combine schema rename and application cutover into one atomic deployment assumption.
