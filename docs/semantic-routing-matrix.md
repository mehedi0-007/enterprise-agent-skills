# V2 Semantic Routing Matrix

This is the canonical routing model for the engineering skill library.

## Backend / Database

| Situation | Primary | Also consider |
|---|---|---|
| endpoint contract | api-design | validation, authorization, error-handling |
| request validation | validation | api-design, api-security |
| use-case orchestration | service-layer | transactions, concurrency |
| persistence access | repository-pattern | postgresql, query-optimization |
| atomic DB workflow | transactions | concurrency, repository-pattern |
| race/lost update | concurrency | transactions, postgresql |
| PostgreSQL-specific behavior | postgresql | transactions, indexing, migrations |
| slow query | query-optimization | repository-pattern, indexing, performance |
| new index | indexing | query-optimization, migrations |
| schema/data change | migrations | postgresql, deployment |
| API failure semantics | error-handling | api-design, async-ui-states |

### Canonical rule

A skill should route to an adjacent skill when the concern crosses its boundary.

Example:

```text
"Add pagination to GET /orders"
    ↓
api-design
    ↓
repository-pattern
    ↓
query-optimization
    ↓
indexing
```

Do not put all pagination implementation guidance into every one of those skills.

---

## Security

| Situation | Primary | Also consider |
|---|---|---|
| identity/session/token | authentication | api-security, secrets-management |
| resource permission | authorization | api-security |
| endpoint threat model | api-security | authentication, authorization, owasp |
| OWASP review | owasp | specialized security skills |
| credential/key lifecycle | secrets-management | authentication, ci-cd |

### Canonical rule

```text
authentication
→ proves principal

authorization
→ decides access

api-security
→ protects the API attack surface/abuse model

owasp
→ orchestrates security review

secrets-management
→ protects credential lifecycle
```

Do not let `owasp` become a duplicate implementation guide.

---

## Frontend

| Situation | Primary | Also consider |
|---|---|---|
| control placement/hierarchy | ui-design | ux-design, accessibility |
| user flow/recovery | ux-design | async-ui-states, forms |
| layout adaptation | responsive-design | accessibility, ui-design |
| semantic/keyboard access | accessibility | every interactive UI skill |
| data entry | forms | accessibility, async-ui-states |
| data collection/table | tables | responsive-design, accessibility, api-design |
| routes/information architecture | navigation | accessibility, responsive-design |
| network/server lifecycle | async-ui-states | ux-design, api-design |

### Canonical rule

```text
ui-design
→ what the interface looks/feels like

ux-design
→ how the user's task behaves

accessibility
→ whether the interaction is perceivable/operable/understandable

responsive-design
→ how it adapts to constraints

async-ui-states
→ how server/network state is represented
```

Do not move backend correctness rules into frontend skills.

---

## Production

| Situation | Primary | Also consider |
|---|---|---|
| container artifact/runtime | docker | security, deployment |
| build/test/promotion | ci-cd | docker, secrets-management |
| live release | deployment | migrations, observability |
| diagnosis/telemetry | observability | performance, deployment |
| measured optimization | performance | query-optimization, frontend |
