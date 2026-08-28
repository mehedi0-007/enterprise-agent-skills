# Canary Release

Risky pricing calculation change:
1. deploy immutable artifact
2. expose to internal/test tenant or small traffic slice
3. compare error/latency/business correctness to baseline
4. promote gradually
5. stop immediately if success criteria fail
6. disable flag or rollback/forward-fix based on data/schema state
