---
name: service-layer
description: Design and review application-service boundaries, business logic placement, transaction ownership, orchestration, side effects, dependencies, and use-case execution. Use when implementing or refactoring controllers, services, domain logic, repositories, integrations, or multi-step backend workflows.
---

# Service Layer — Production Playbook

## 1. Mission

The service/application layer coordinates a meaningful application use case.

Its job is not to be "the place where all code goes."

A good service layer:
- exposes application operations
- coordinates domain behavior
- coordinates persistence/infrastructure
- owns use-case-level transaction boundaries when appropriate
- translates application outcomes for callers
- keeps transport and infrastructure details from spreading unnecessarily

Martin Fowler describes Service Layer as an application boundary defining available operations and coordinating each operation, including transaction control. citeturn341892search6

---

## 2. Activation

Use this skill when:
- adding a backend use case
- deciding where business logic belongs
- a controller is becoming complex
- a service is becoming a "god service"
- multiple repositories/integrations must be coordinated
- a workflow needs a transaction
- external side effects occur after state changes
- refactoring module boundaries
- deciding whether domain objects should own behavior

---

## 3. Start With the Use Case

Before creating a service method, write the use case in business terms.

Example:

`CreateSubscription(accountId, planId, paymentMethodId)`

Then identify:
- actor
- authorization
- input
- required state
- business decisions
- writes
- external effects
- transaction boundary
- retry/idempotency behavior
- result
- failure modes

Do not begin with:
"Which service should this method go in?"

Start with:
"What application operation are we implementing?"

---

## 4. Responsibility Map

### Controller / Transport

Own:
- routing
- protocol parsing
- transport-level validation
- authentication context
- protocol status/headers
- mapping request into an application operation
- mapping result/error into transport representation

Should usually NOT own:
- multi-step business workflows
- direct orchestration across repositories
- payment/email/queue workflows
- business state transitions

NestJS explicitly describes controllers as handling incoming requests/responses and recommends delegating more complex tasks to providers. citeturn341892search11turn341892search7

### Application Service

Own:
- application/use-case orchestration
- coordination across domain components
- transaction boundary when needed
- authorization coordination where the policy belongs at application level
- external side-effect coordination
- application-level error translation

### Domain Model

Own business rules that belong to the domain itself:
- invariants
- calculations
- state transitions
- policies
- behavior that should remain valid regardless of HTTP, queue, CLI, or scheduled entry point

Fowler distinguishes domain logic from presentation/persistence concerns and warns that moving all behavior into services can produce an anemic domain model. citeturn341892search4

### Repository / Data Access

Own:
- persistence queries
- persistence mapping
- query-specific data retrieval
- database-specific concerns

Do NOT hide application policy in the repository.

### Infrastructure

Own:
- email provider
- object storage
- payments
- queues
- external HTTP APIs
- cache
- technical adapters

---

## 5. Decision Tree: Where Does Logic Belong?

Ask in order:

### Question 1
Is it about HTTP/protocol behavior?

→ Controller/transport.

### Question 2
Is it a business invariant/calculation/state transition?

→ Domain logic when a domain concept naturally owns it.

### Question 3
Is it coordinating multiple domain objects/resources/infrastructure dependencies for one use case?

→ Application service.

### Question 4
Is it primarily a database query/persistence operation?

→ Repository/data-access.

### Question 5
Is it technical integration behavior?

→ Infrastructure adapter.

### Important
Do not force every statement into a distinct class. The goal is clear responsibility, not maximal layering.

---

## 6. Thin vs Thick Services

"Thin service" does NOT mean "service contains no logic."

It means the service primarily coordinates a use case rather than becoming the home for every business rule.

Healthy:

```text
Service
  ├── load account
  ├── ask domain object to validate transition
  ├── persist changes
  └── publish/outbox side effect
```

Suspicious:

```text
Service
  ├── calculate pricing
  ├── calculate taxes
  ├── decide eligibility
  ├── validate every invariant
  ├── manipulate domain state
  ├── build SQL
  ├── call payment API
  └── format HTTP response
```

Fowler notes that excessive service logic can become transaction-script-like and weaken the domain model. citeturn341892search4

However, do NOT introduce domain entities/value objects solely to avoid a long service. The architecture should match the complexity of the business domain.

---

## 7. Transaction Ownership

A transaction should normally belong to the application operation that requires atomicity.

Example:

```text
CreateOrder
  BEGIN
    create order
    create order items
    reserve inventory
  COMMIT
```

Do not silently make every repository call open its own independent transaction.

### Why?

Because this is dangerous:

```text
Service
  repo.createOrder()       // tx A
  repo.createItems()       // tx B
  repo.reserveInventory()  // tx C
```

The use case can partially succeed.

Instead, the application boundary should make atomicity visible and deliberate.

---

## 8. Transaction vs External Side Effect

A database transaction cannot automatically roll back:

- email
- payment request
- webhook delivery
- external HTTP call
- queue message sent to another system

Therefore:

```text
DB commit
   ≠
external side effect completed
```

For important workflows consider:
- transactional outbox
- post-commit dispatch
- provider idempotency
- reconciliation
- durable workflow state

Do not hold a database transaction open while waiting on an unrelated slow network operation unless there is a strong, explicit reason.

---

## 9. Authorization Placement

Authorization can involve several layers.

### Transport guard/middleware
Good for:
- authentication
- coarse/global permissions

### Application service
Good for:
- use-case authorization
- checking whether this operation is allowed

### Domain
Good for:
- invariant/policy rules intrinsic to the domain

### Repository
Good for:
- enforcing tenant/object scoping at query level when appropriate

Do not make the repository the sole source of authorization policy unless the architecture deliberately makes it the enforcement boundary.

The important property is:
**authorization is enforced server-side at every protected operation.**

---

## 10. Dependency Direction

Prefer:

```text
Controller
   ↓
Application
   ↓
Domain
   ↑
Infrastructure adapters
```

Conceptually, business/application behavior should not become coupled to:
- HTTP request objects
- ORM implementation details
- specific payment SDKs
- email vendor objects

When infrastructure changes, business behavior should not require widespread edits.

That does not mean every dependency requires an interface. Introduce abstractions where they protect a meaningful boundary.

---

## 11. Service-to-Service Calls

A service calling another service is not automatically wrong.

Ask:
- Is this actually another use case?
- Is the dependency creating a cycle?
- Can the shared business rule live in a domain abstraction instead?
- Are transaction semantics crossing boundaries?
- Is one service becoming a facade for everything else?

Red flag:

```text
AService
 → BService
   → CService
     → AService
```

Circular orchestration makes behavior and transactions difficult to reason about.

Prefer explicit use-case orchestration or shared domain/application components where appropriate.

---

## 12. Idempotency and Retries

For operations that can be retried:
- identify the logical command
- determine whether duplicate execution is harmful
- persist deduplication state when required
- use unique constraints or idempotency keys
- make external effects retry-safe

The service is often responsible for orchestrating this behavior, while persistence enforces durable uniqueness/state.

---

## 13. Read vs Write Use Cases

Do not automatically give reads and writes identical abstractions.

A read-heavy use case may benefit from:
- direct optimized query
- projection/read model
- pagination
- aggregate query

A write use case may require:
- domain rules
- transaction
- invariants
- side effects

Trying to force both through one generic repository/service abstraction can obscure important differences.

---

## 14. Service Size and God Services

A large service is a signal, not an automatic defect.

Investigate whether it contains:
- unrelated use cases
- multiple business subdomains
- too many integrations
- data-access details
- policy logic
- notification logic
- billing logic
- authorization logic

Refactor around cohesive responsibility, not arbitrary line count.

### Refactoring sequence

1. Group methods by business capability.
2. Identify shared invariants.
3. Separate infrastructure adapters.
4. Separate distinct use cases where useful.
5. Preserve transaction/error semantics.
6. Add tests before/after major extraction.

---

## 15. Side-Effect Ordering

For a use case:

```text
save state
send email
publish event
```

ask:
- Which effects are mandatory?
- Which can be eventually consistent?
- What if email succeeds but DB commit fails?
- What if DB succeeds but publish fails?
- What happens on retry?

Never imply exactly-once behavior unless the design actually provides it.

---

## 16. Error Translation

Each layer should add meaning only when it has enough context.

Example:

```text
PostgreSQL unique violation
       ↓
repository/persistence error
       ↓
service: "email already registered"
       ↓
API: 409 USER_ALREADY_EXISTS
```

Avoid:
- leaking SQL errors to API clients
- catching everything and returning "Internal error"
- creating dozens of meaningless wrapper errors

---

## 17. Caching

The application/service layer may coordinate caching, but the source of truth remains explicit.

Before adding cache ask:
- what data is cached?
- why?
- freshness requirement?
- invalidation event?
- authorization scope?
- cache miss behavior?
- stale data risk?
- failure behavior?

Do not place business-critical correctness solely in an eventually consistent cache unless the domain explicitly allows it.

---

## 18. Background Jobs

Move work to a worker when:
- it is long-running
- user does not need immediate completion
- retries are required
- workload spikes need smoothing
- asynchronous processing is acceptable

The service/use-case should define the job's business semantics; the worker handles execution/retry mechanics.

Important:
- idempotency
- job state
- retry policy
- dead-letter/recovery
- observability

---

## 19. Testing Strategy

### Unit test domain logic
Use focused tests for:
- invariants
- calculations
- state transitions

### Application/service tests
Test:
- use-case orchestration
- authorization decisions
- transaction behavior at appropriate boundaries
- integration coordination
- failure semantics

### Integration tests
Test:
- actual persistence
- constraints
- transaction semantics
- external adapter contracts

Do not mock everything. A test that mocks the repository cannot prove a database constraint works.

---

## 20. Common Anti-Patterns

### Anemic Domain by Default
Every rule lives in `SomethingService`.

### Fat Controller
Controller performs business/database workflow.

### Generic Service
`BaseService<T>` contains universal CRUD and hides meaningful domain operations.

### Repository Policy Leak
Repository decides whether a user is entitled to perform business actions.

### Hidden Transactions
Individual repository calls silently create transactions that cannot compose.

### Network Inside Transaction
Database transaction waits for slow external HTTP call without strong reason.

### Service Chain
Long service-to-service call graph with unclear ownership.

### Over-Abstraction
Interfaces/factories/providers added with no changeability/testing boundary.

### Framework Leakage
Domain/application logic depends directly on HTTP decorators, ORM models, or vendor SDK objects.

---

## 21. Review Procedure

When reviewing a service implementation, inspect:

1. What exact use case does it represent?
2. Is its public interface expressed in business/application terms?
3. Are controllers thin?
4. Are business invariants located where they naturally belong?
5. Is transaction ownership visible?
6. Are external side effects coordinated safely?
7. Are retries/idempotency defined?
8. Are authorization checks present?
9. Are repositories limited to persistence?
10. Are infrastructure dependencies contained?
11. Are tests proving behavior at the right layer?
12. Is the service boundary helping or merely adding indirection?

---

## 22. Verification Checklist

- [ ] use case is explicit
- [ ] controller contains transport concerns only
- [ ] business invariants are not accidentally hidden in transport/persistence
- [ ] service coordinates rather than becoming a god object
- [ ] transaction boundary is deliberate
- [ ] external side effects have failure/retry semantics
- [ ] authorization is enforced
- [ ] persistence concerns stay in data-access code
- [ ] dependency direction is understandable
- [ ] no unnecessary abstraction was added
- [ ] important behavior has appropriate tests
- [ ] concurrency/idempotency risks were reviewed
- [ ] observability exists for important operations

## References

- `references/placement-examples.md`
- `references/transaction-side-effects.md`
- `references/service-smells.md`

## Cross-Skill Routing
- For `repository-pattern` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
- For `transactions` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
- For `concurrency` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
