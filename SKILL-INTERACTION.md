# Skill Interaction Map

## Typical Feature Loop

```text
Requirement
  ↓
Architecture
  ↓
API / UI contract
  ↓
Validation + Authorization
  ↓
Service / Use Case
  ↓
Transaction + Concurrency
  ↓
Repository / Database
  ↓
Tests
  ↓
Observability
  ↓
Deployment
  ↓
Post-deploy verification
```

## Example: Create Order

```text
requirements-analysis
→ architecture
→ api-design
→ validation
→ authorization
→ service-layer
→ transactions
→ concurrency
→ repository-pattern
→ postgresql
→ testing-quality
→ observability
→ deployment
```

## Example: SaaS Table

```text
ui-design
→ ux-design
→ tables
→ responsive-design
→ accessibility
→ navigation
→ api-design
→ query-optimization
→ indexing
→ async-ui-states
```

## Example: Password Reset

```text
authentication
→ api-design
→ api-security
→ authorization
→ secrets-management
→ testing-quality
→ observability
```

## Routing Rule

Use the narrowest relevant skill first, then load adjacent skills only when the task crosses that boundary.

Do not activate every skill for every task.

## Conflict Rule

When guidance appears to conflict:
1. follow explicit project requirements
2. follow actual framework/platform semantics
3. preserve security/data integrity
4. follow the more specific skill
5. use cross-layer-review to resolve remaining contract mismatches
