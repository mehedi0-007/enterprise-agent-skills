# Isolation and Locking

PostgreSQL isolation determines what a transaction can observe and when conflicts surface.

## Read Committed
Default PostgreSQL isolation.
Each command gets a snapshot at command start. Two commands in one transaction can therefore see different committed states.

Use when the application can safely tolerate that behavior.

## Repeatable Read / Serializable
Stronger guarantees can prevent certain anomalies but may surface serialization failures.

If the application uses stronger isolation for correctness, define how it detects and retries transaction failures.

## Row Locks
`FOR UPDATE` can serialize changes to selected rows. Keep the lock scope short.

## Rule
Choose isolation and locks from the invariant, not from a generic "stronger is better" instinct.
