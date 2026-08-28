# Testing Async UI

Test:
- delayed responses
- out-of-order responses
- cancellation
- timeout after server completion
- duplicate activation
- retry/backoff
- rate limit
- optimistic rollback
- partial success
- background completion

Use controlled timing/network fixtures rather than hoping real-world timing exposes races.
