# Contributing

## Core Principle

Improve engineering judgment, not documentation volume.

A change should answer:
- what decision does this improve?
- what failure does it prevent?
- what evidence supports it?
- which existing skill owns the decision?

## Skill Changes

Prefer:
- concise activation conditions
- decision trees
- failure modes
- verification checklists
- references for deeper material
- realistic examples

Avoid:
- framework-specific syntax unless unavoidable
- repeating another skill
- generic motivational prose
- arbitrary numeric rules without context
- claims of guaranteed security/performance

## Cross-Skill Changes

When changing one skill, check:
- `ARCHITECTURE.md`
- `SKILL-INTERACTION.md`
- related neighboring skills

Keep boundary ownership explicit.

## Source Quality

Prefer primary/current sources:
- official specifications
- vendor/platform documentation
- established security standards
- primary database documentation

Community agent skills can provide practical patterns, but do not copy them wholesale or treat them as authoritative.

## Review Standard

A good skill should make an agent:
- ask better questions
- choose safer defaults
- detect important failure modes
- verify its work
- avoid unnecessary complexity
