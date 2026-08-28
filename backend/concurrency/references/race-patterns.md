# Race Patterns

## Check Then Insert
Two actors can both observe "missing" and both insert.
Use a unique constraint and handle the conflict.

## Read Then Write
Two actors can read the same value and overwrite each other's calculation.
Use atomic update, version check, or lock.

## Check State Then Transition
Use conditional state transition such as:
`UPDATE ... WHERE status = 'PENDING'`.

## Duplicate Processing
Two workers may process the same logical job.
Use durable identity/idempotency and a concurrency-safe claim/transition.
