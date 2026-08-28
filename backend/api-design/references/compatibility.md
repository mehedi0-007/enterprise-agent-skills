# API Compatibility

Prefer additive changes.

Potentially breaking:
- field removal/rename/type changes
- requiredness/nullability changes
- semantic changes
- error/status changes
- pagination changes
- material performance/rate-limit/concurrency changes

For rolling deployments, assume old and new versions can overlap unless guaranteed otherwise.

Use deprecation guidance and a removal policy for breaking changes.
