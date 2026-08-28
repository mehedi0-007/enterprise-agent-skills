# Async State Matrix

| Situation | Minimum UI treatment |
|---|---|
| Fast local action | button pressed/loading state if duplicate activation is risky |
| Normal API fetch | local loading indicator or stable skeleton |
| Long-running job | queued/processing state + progress if meaningful |
| Recoverable error | clear error + retry/recovery |
| Validation error | field-level guidance |
| Permission error | explain lack of access + next step |
| Empty dataset | explain what empty means + useful next action |
| No search results | distinguish from no data + help adjust filters |
| Timeout | explain retry and preserve state |

The exact treatment depends on task criticality and duration.
