# Quality Gates

Every substantial feature should pass the gates relevant to its risk.

## Gate 1 — Requirement
- goal clear
- scope bounded
- acceptance criteria testable
- edge cases identified

## Gate 2 — Design
- boundaries explicit
- dependencies justified
- failure behavior defined
- security/data implications reviewed

## Gate 3 — Implementation
- layer responsibilities respected
- no unnecessary abstraction
- correctness invariants explicit

## Gate 4 — Verification
- tests appropriate to risk
- negative/security cases included
- integration behavior verified
- performance measured when relevant

## Gate 5 — Production
- observability sufficient
- migration compatibility verified
- deployment/recovery plan defined
- secrets/configuration safe

## Evidence Rule

Do not claim:
- tested
- optimized
- secure
- production-ready
- rollback-safe

unless the relevant evidence exists.

## Risk Rule

Spend more verification effort on:
- money
- permissions
- data integrity
- destructive operations
- concurrency
- external side effects
- tenant boundaries
- irreversible changes
