---
name: validation
description: Validate untrusted input at backend boundaries and keep business rules in the correct layer. Use for DTOs, query/path parameters, files, patch semantics, and security-sensitive inputs.
---

# Validation

## Boundary
Validate:
- type and shape
- required/optional semantics
- length/range
- formats
- enum values
- collection size
- file size/type

## Validation vs Business Rules
Structural validation:
"Is this request well formed?"

Business validation:
"Is this operation valid given current state and policy?"

Do not put database-dependent business policy into DTO validators merely for convenience.

## Canonicalization
Normalize only when domain semantics explicitly require it.

Be precise about:
- case sensitivity
- whitespace
- Unicode
- null vs omitted
- empty strings/collections

## Security
Validation is not authorization.
Also use:
- server-side access control
- parameterized queries
- output filtering
- rate limits
- resource limits

## Verification
Test valid, invalid, boundary, null, omitted, oversized, unexpected, and malicious-looking inputs. Verify rejected inputs cannot reach sensitive operations.

## Activation

Use when validating request bodies, query/path parameters, commands, imported data, or other untrusted input.

## Review Procedure

1. Identify the trust boundary and authoritative source of truth.
2. Validate shape/type/range/format.
3. Separate structural validation from business rules and authorization.
4. Define error mapping.
5. Check size/depth/resource bounds.
6. Verify server-side enforcement.

## Verification Checklist

- [ ] untrusted inputs identified
- [ ] structural validation defined
- [ ] business validation separated
- [ ] authorization not delegated to validation
- [ ] resource limits considered
- [ ] stable error mapping defined
- [ ] negative tests exist

## Cross-Skill Routing
- For `api-design` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
- For `api-security` concerns, coordinate with the specialized skill rather than duplicating its implementation guidance.
