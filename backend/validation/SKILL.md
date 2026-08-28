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
