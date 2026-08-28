# Rate-Limit Design

Choose limits from operation cost/risk.

Dimensions may include:
- IP
- authenticated principal
- tenant
- API key/client
- endpoint
- business action

For expensive actions, combine:
- rate limits
- concurrency limits
- payload limits
- quotas

Do not use a single number for all endpoints without understanding cost.
