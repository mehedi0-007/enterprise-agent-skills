---
name: validation
description: Design input validation at API and application boundaries. Use for request DTOs, query parameters, path parameters, file uploads, domain validation, and security-sensitive input handling.
---

# Validation

## Purpose
Reject malformed or unacceptable input early while keeping business rules in the correct layer.

## Boundary Validation
Validate untrusted input at the transport boundary:
- type/shape
- required fields
- length/range
- format
- enum values
- collection limits
- file size/type constraints where relevant

Treat all client input as untrusted.

## Validation vs Business Rules
Transport validation answers:
"Is this input structurally valid?"

Business validation answers:
"Is this operation allowed given current business state?"

Examples:
- email has valid syntax -> boundary validation
- user is allowed to change this email -> business/authorization logic
- start date is before end date -> may belong to boundary validation
- start date is permitted by the booking policy -> domain/application logic

Do not put database-dependent business logic inside DTO validators merely because it is convenient.

## Canonicalization
Normalize input where the domain requires it:
- whitespace
- case where identifiers are case-insensitive
- Unicode/format normalization where applicable

Do not silently alter user data when the semantic effect is uncertain.

## Security
Never treat validation as the only security control.
Also apply:
- authorization
- output filtering
- parameterized queries
- rate limits
- size limits
- safe parsing
- content-type verification for uploads

## Partial Updates
PATCH-like operations should distinguish:
- omitted field
- explicit null
- empty string/collection
according to the API contract.

Do not invent semantics.

## Verification
Test valid, invalid, boundary, missing, null, oversized, unexpected, and malicious-looking inputs.
Verify rejected input never reaches sensitive operations.
