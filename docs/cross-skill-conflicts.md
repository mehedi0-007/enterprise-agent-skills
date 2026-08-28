# Known Cross-Skill Conflict Tests

Use these as review cases during the v2 audit.

## 1. "Transaction makes it safe"
Correct interpretation:
- transaction gives atomicity/defined isolation
- concurrency analysis still required

Relevant:
`transactions` + `concurrency`

## 2. "Repository should authorize"
Correct interpretation:
- repository can enforce trusted tenant/object scope as a defense
- application/domain authorization still owns policy

Relevant:
`repository-pattern` + `authorization`

## 3. "Add an index because WHERE uses a column"
Correct interpretation:
- first measure/query-plan
- index only when workload evidence supports it

Relevant:
`query-optimization` + `indexing`

## 4. "Rollback the release"
Correct interpretation:
- only if old artifact is compatible with current schema/data
- external effects cannot be magically undone

Relevant:
`migrations` + `deployment`

## 5. "Disable the button"
Correct interpretation:
- UI prevents accidental duplicates
- backend still needs idempotency/concurrency controls when required

Relevant:
`async-ui-states` + `concurrency` + `api-design`

## 6. "Hide the menu item"
Correct interpretation:
- UX improvement only
- backend authorization remains mandatory

Relevant:
`navigation` + `authorization`

## 7. "JWT means authentication is solved"
Correct interpretation:
- token validation is one component of authentication/session design

Relevant:
`authentication` + `api-security`

## 8. "API is internal"
Correct interpretation:
- network location is not authorization

Relevant:
`api-security` + `authorization`

## 9. "200 means success"
Correct interpretation:
- API contract defines semantics; accepted/processing/conflict/validation are distinct

Relevant:
`api-design` + `async-ui-states`

## 10. "Green CI means production is healthy"
Correct interpretation:
- CI verifies build/tests
- deployment needs post-deploy health/business validation

Relevant:
`ci-cd` + `deployment` + `observability`
