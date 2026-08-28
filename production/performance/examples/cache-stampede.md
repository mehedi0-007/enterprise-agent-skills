# Cache Stampede

1000 requests miss the same expensive report simultaneously.

Bad:
all 1000 recompute.

Possible:
single-flight/coalescing + short jittered refresh + stale-while-revalidate where product semantics allow.

Verify:
- DB load
- latency
- freshness
- failure behavior
