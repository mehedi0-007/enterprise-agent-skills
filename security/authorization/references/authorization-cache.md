# Authorization Cache

Caching decisions can reduce load but introduces stale permission risk.

Define:
- what is cached
- scope of key
- TTL
- invalidation trigger
- behavior after role removal
- behavior after tenant membership removal
- fail-open/closed policy

For sensitive operations, prefer fresh enforcement or a cache model with reliable invalidation.
