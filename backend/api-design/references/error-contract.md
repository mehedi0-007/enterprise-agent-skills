# Error Contract

Errors should be machine-readable, safe, stable, and diagnosable.

Example:

```json
{
  "code": "RESOURCE_CONFLICT",
  "message": "The requested state conflicts with the current resource state.",
  "details": [],
  "requestId": "..."
}
```

Use `code` for programmatic behavior and `message` for humans.
Never make clients parse prose.
Do not expose stack traces, SQL, secrets, or internal provider messages.
