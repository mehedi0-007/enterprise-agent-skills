# Enterprise Agent Skills

A curated, production-oriented skill library for AI coding agents.

The goal is not to teach framework syntax. The goal is to encode engineering judgment:
- how to reason about requirements
- how to design APIs and service boundaries
- when to use transactions, indexes, caching, retries, and locks
- how to review security and authorization
- how to design usable, accessible interfaces
- how to test and operate software in production

Designed to complement workflow-oriented systems such as Superpowers.

## Structure

```text
engineering/
backend/
database/
security/
frontend/
production/
```

Each skill is a folder containing `SKILL.md`. Skills may also contain `references/` for deeper material.

## Philosophy

1. Measure before optimizing.
2. Prefer simple designs over speculative complexity.
3. Enforce security server-side.
4. Treat data integrity and concurrency as first-class concerns.
5. Design error, loading, empty, and recovery states.
6. Verify behavior with evidence.
7. Keep framework knowledge separate from engineering judgment.

## Using With Antigravity

Clone this repository into a project's `.agents/skills` directory:

```bash
mkdir -p .agents
git clone git@github.com:mehedi0-007/enterprise-agent-skills.git .agents/skills
```

Update later with:

```bash
cd .agents/skills
git pull
```

## Superpowers

Superpowers provides the development workflow: brainstorming, planning, TDD, debugging, review, and verification.

This repository provides domain engineering guidance that Superpowers does not attempt to encode.

## Source Policy

See `SOURCES.md` for provenance. Upstream official documentation is preferred for correctness; community agent skills are used as comparative/practical input and are not copied wholesale.

## Scope

This repository is an engineering aid, not a guarantee of production safety, security, compliance, or correctness. Critical systems still require appropriate human review and operational controls.
