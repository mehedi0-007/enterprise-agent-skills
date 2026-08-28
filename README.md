# Enterprise Agent Skills

A reusable, framework-agnostic skill library for AI coding agents building and reviewing production-grade software.

The goal is simple:

> Give an AI coding agent the engineering judgment, checklists, tradeoffs, and failure-mode awareness needed to build serious software—not just generate code that compiles.

These skills are designed to work with agentic coding environments such as Antigravity and other tools that support the Agent Skills convention.

---

## What This Repository Provides

This repository contains **34 engineering skills** covering the full software lifecycle:

```text
requirements
    ↓
architecture
    ↓
API / backend / database / security / frontend
    ↓
testing
    ↓
observability
    ↓
deployment
    ↓
production operation
```

The skills are intentionally **framework-agnostic**.

They focus on engineering decisions such as:

- How should an API endpoint be designed?
- Where should business logic live?
- When should a transaction be used?
- When is a race condition possible?
- When is an index actually justified?
- How should tenant isolation work?
- How should a destructive UI action behave?
- When should an operation be optimistic?
- How should a long-running job be represented?
- How should a release be rolled out safely?
- What telemetry is actually useful during an incident?

The repository is not intended to replace framework or platform documentation. It provides the engineering reasoning layer that should sit above those technologies.

---

# Skill Map

## Engineering

Core engineering process and cross-layer reasoning.

```text
engineering/
├── requirements-analysis
├── planning
├── architecture
├── cross-layer-review
├── testing-quality
└── production-readiness
```

Use these when the task involves understanding the problem, planning work, making architectural decisions, validating behavior, or determining production readiness.

---

## Backend

Application and API design.

```text
backend/
├── api-design
├── service-layer
├── repository-pattern
├── error-handling
├── validation
├── transactions
└── concurrency
```

These skills cover the application request path:

```text
API contract
    ↓
validation
    ↓
authentication / authorization
    ↓
service / use case
    ↓
transaction / concurrency
    ↓
repository
```

---

## Database

PostgreSQL and database engineering.

```text
database/
├── postgresql
├── query-optimization
├── indexing
└── migrations
```

The database skills focus on evidence-driven decisions instead of rules like "add an index whenever a column appears in a WHERE clause."

```text
slow query
    ↓
measure
    ↓
inspect execution plan
    ↓
identify bottleneck
    ↓
optimize query / access path
    ↓
measure again
```

---

## Security

Application and API security.

```text
security/
├── authentication
├── authorization
├── api-security
├── owasp
└── secrets-management
```

The responsibilities are intentionally separated:

```text
authentication
    → Who is this principal?

authorization
    → Are they allowed to perform this action?

api-security
    → How can the API be attacked or abused?

owasp
    → Which security review areas apply?

secrets-management
    → How are credentials protected through their lifecycle?
```

---

## Frontend

Production web UI/UX.

```text
frontend/
├── ui-design
├── ux-design
├── responsive-design
├── accessibility
├── forms
├── tables
├── navigation
└── async-ui-states
```

The skills cover both appearance and behavior:

```text
UI design
    ↓
UX / user flow
    ↓
forms / tables / navigation
    ↓
async server state
    ↓
responsive behavior
    ↓
accessibility
```

The objective is not simply to make an interface look good. The skills also cover loading, empty, error, retry, permission, mobile, keyboard, and recovery states.

---

## Production

Operational and delivery engineering.

```text
production/
├── docker
├── ci-cd
├── observability
├── performance
└── deployment
```

The production flow is:

```text
build
  ↓
test
  ↓
secure
  ↓
create immutable artifact
  ↓
promote
  ↓
deploy
  ↓
observe
  ↓
verify
  ↓
recover if necessary
```

---

# How the Skills Work Together

The most important feature of this repository is not the number of skills.

It is the **routing between them**.

A realistic feature may cross multiple domains.

For example:

### "Export all invoices"

An agent may need to reason about:

```text
requirements-analysis
        ↓
architecture
        ↓
api-design
        ↓
authorization
        ↓
service-layer
        ↓
query-optimization
        ↓
api-security
        ↓
async-ui-states
        ↓
tables / ui-design / ux-design
        ↓
observability
        ↓
deployment
```

Each skill owns a specific concern rather than trying to solve everything itself.

This keeps the skill library:

- modular
- maintainable
- easier for agents to navigate
- less repetitive
- easier to improve from real-world failures

---

# Installation

The simplest approach is to place the repository in the project's agent skills directory.

From your project:

```bash
git clone git@github.com:mehedi0-007/enterprise-agent-skills.git .agents/skills
```

Then your project can look like:

```text
my-project/
├── .agents/
│   └── skills/
│       ├── engineering/
│       ├── backend/
│       ├── database/
│       ├── security/
│       ├── frontend/
│       └── production/
├── src/
├── tests/
└── ...
```

Using SSH is recommended if your GitHub environment is already configured for SSH.

To update the skills later:

```bash
cd .agents/skills
git pull
```

Because the skill repository is separate from the application repository, the same engineering guidance can be reused across multiple projects.

---

# Using the Skills with an Agent

You generally do not need to manually tell the agent which skill to use for every task.

A well-designed agent should be able to select relevant skills from the task.

For example:

```text
"Add a multi-tenant invoice export feature."
```

Relevant concerns may include:

```text
requirements
architecture
api-design
authorization
api-security
service-layer
query-optimization
async-ui-states
ui-design
tables
observability
deployment
```

The expected behavior is:

```text
understand the request
        ↓
identify relevant engineering boundaries
        ↓
load the appropriate skills
        ↓
design
        ↓
implement
        ↓
verify
```

The repository intentionally avoids framework-specific instructions wherever possible.

For example, there is no need for separate generic skills such as:

```text
nestjs/
react/
nextjs/
typeorm/
prisma/
```

unless repeated real-world experience shows that a technology has an important decision pattern that cannot be expressed well by the general skills.

---

# Skill Structure

Each skill is centered around a `SKILL.md`.

A typical skill may look like:

```text
skill-name/
├── SKILL.md
├── references/
│   ├── ...
└── examples/
    ├── ...
```

The main skill should provide:

```text
purpose
activation conditions
decision guidance
failure modes
anti-patterns
cross-skill routing
verification checklist
```

Detailed material can live in `references/` and concrete cases can live in `examples/`.

This keeps the primary instruction useful without turning every skill into an enormous document.

---

# Engineering Philosophy

These skills are designed around a few principles.

## 1. Measure Before Optimizing

Do not optimize because something "looks slow."

Prefer:

```text
baseline
    ↓
evidence
    ↓
hypothesis
    ↓
change
    ↓
measurement
```

---

## 2. Security Is a Boundary

Do not assume:

```text
authenticated = authorized
```

or:

```text
hidden UI = protected resource
```

or:

```text
internal network = trusted caller
```

Security decisions belong at the appropriate server-side boundary.

---

## 3. Transactions Do Not Automatically Solve Concurrency

A transaction provides transactional semantics.

It does not automatically prevent:

- lost updates
- race conditions
- duplicate operations
- invalid state transitions

Concurrency must be analyzed separately.

---

## 4. The Frontend Is a State Machine

A production UI is more than a successful screenshot.

Important states can include:

```text
loading
success
empty
no results
validation error
permission denied
conflict
processing
timeout
retrying
completed
failed
```

---

## 5. Rollback Is Not Always Possible

A deployment rollback may be unsafe after:

- irreversible database changes
- destructive data migrations
- external side effects
- incompatible schema changes

Sometimes the correct recovery is:

```text
feature disable
```

or:

```text
forward fix
```

rather than reverting code.

---

## 6. Evidence Over Confidence

The skills deliberately discourage claims such as:

```text
"this is definitely secure"
"this is guaranteed faster"
"rollback is safe"
```

unless there is evidence supporting the claim.

The agent should explain assumptions, tradeoffs, and verification.

---

# Cross-Skill Ownership

The repository uses explicit ownership to reduce duplicated guidance.

### Backend

```text
api-design
    → transport/API contract

validation
    → input correctness

service-layer
    → use-case orchestration

repository-pattern
    → persistence access

transactions
    → atomicity

concurrency
    → shared-state correctness

database skills
    → PostgreSQL/query/schema concerns
```

### Security

```text
authentication
    → identity/session/credential lifecycle

authorization
    → access decisions

api-security
    → API attack surface and abuse

owasp
    → review orchestration

secrets-management
    → credential lifecycle
```

### Frontend

```text
ui-design
    → hierarchy and controls

ux-design
    → task flow

forms
    → data entry

tables
    → collection interaction

navigation
    → information architecture

async-ui-states
    → server/network lifecycle

responsive-design
    → layout constraints

accessibility
    → semantic and assistive behavior
```

### Production

```text
docker
    → container/runtime artifact

ci-cd
    → build/test/promote

deployment
    → live rollout/recovery

observability
    → operational evidence

performance
    → measured optimization
```

---

# Repository Maintenance

The repository includes validation/audit tooling for maintaining consistency as the skills evolve.

Useful checks include:

```bash
python3 scripts/audit-skill-boundaries.py
python3 scripts/final-audit.py
```

These checks are intended to catch structural and routing problems.

They are **not** proof that the engineering guidance is correct.

Human review and real project usage remain important.

---

# How This Library Evolves

The preferred improvement loop is based on real agent behavior:

```text
real project
    ↓
agent makes questionable decision
    ↓
identify which skill failed
    ↓
capture the case
    ↓
improve the skill
    ↓
add a regression example
    ↓
commit
```

For example:

```text
Agent adds an index without inspecting the query plan
        ↓
improve database/indexing
        ↓
add a regression example
```

Or:

```text
Agent hides an admin action in the frontend
but forgets backend authorization
        ↓
improve navigation + authorization
        ↓
add a cross-layer example
```

This feedback loop is more valuable than continuously making every skill longer.

---

# Contributing

When improving a skill, prefer adding:

- a useful decision rule
- a failure mode
- a tradeoff
- a verification step
- a realistic example
- a precise cross-skill handoff

Avoid adding material simply to increase document length.

Framework-specific guidance should normally stay in the project unless it represents a reusable engineering principle.

When adding a new rule, ask:

> What bad decision does this prevent?

If the answer is unclear, the rule probably needs refinement.

---

# Status

**Current version: v2**

```text
34 skills
6 engineering domains
cross-skill routing
references/examples
consistency checks
production-oriented guidance
```

The repository is intended to be a living engineering knowledge base.

The next improvements should come primarily from **real project usage and observed agent failures**, rather than theoretical expansion.

---

# License

Add the repository license you want to use here.

---

## Repository

GitHub:

https://github.com/mehedi0-007/enterprise-agent-skills
