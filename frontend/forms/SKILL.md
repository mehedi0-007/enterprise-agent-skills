---
name: forms
description: Design usable, accessible, resilient web forms. Use when building create/edit flows, authentication, settings, checkout, search filters, or any multi-field user input.
---

# Forms

## Mission
Make entering, correcting, and submitting information predictable and efficient.

## Structure
Use:
- clear labels
- logical grouping
- consistent field order
- helpful descriptions only when needed
- appropriate input types and autocomplete metadata
- explicit required/optional semantics

## Validation Timing
Prefer validation that helps users recover without being noisy.
Use:
- immediate validation for simple constraints when helpful
- validation on blur for many fields
- full validation on submit

Do not prevent users from entering intermediate values required to construct a valid value.

## Error Messages
Errors should:
- identify the field
- describe what is wrong
- explain how to fix it when possible
- remain associated with the field
- not rely solely on color

W3C guidance emphasizes that errors should be specific and programmatically perceivable, not merely indicated by a visual marker. citeturn814403search24

## Submission
On submit:
- prevent accidental duplicate submission
- show progress
- preserve entered data on recoverable failure
- surface server-side validation errors
- focus/announce the relevant error summary appropriately

Do not permanently disable the submit button merely because one optional field is incomplete unless the disabled reason is discoverable and the design remains usable.

## Server Validation
Client validation improves UX; server validation remains authoritative.

## Sensitive Inputs
Use appropriate:
- password controls
- autocomplete behavior
- input type
- privacy/masking
- rate limits for auth/recovery forms

## Verification
Test keyboard, screen readers, invalid values, long text, slow network, server errors, duplicate clicks, refresh/navigation, and mobile keyboards.
