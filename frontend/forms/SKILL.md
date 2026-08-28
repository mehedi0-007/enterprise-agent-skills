---
name: forms
description: Design, implement, and review production web forms and data-entry workflows. Use for authentication, create/edit screens, settings, checkout, search/filter forms, multi-step workflows, uploads, autosave, validation, and server error handling.
---

# Forms — Production Playbook

## 1. Mission

A good form minimizes the effort required to enter correct information and makes errors easy to understand and recover from.

A production form must define:
- what the user needs to enter
- what is required
- what is optional
- what format is expected
- when validation occurs
- what happens during submission
- what happens on server failure
- whether work is preserved
- how accessibility works
- whether duplicate submission is possible
- whether sensitive data needs special treatment

Do not treat forms as a collection of inputs. Treat them as a user workflow.

---

## 2. Activation

Use when:
- creating or modifying forms
- adding fields
- changing validation
- connecting a form to an API
- implementing login/signup/recovery
- implementing create/edit workflows
- building multi-step forms
- adding autosave/drafts
- implementing uploads
- handling server validation/errors
- reviewing accessibility

---

## 3. Start With the Data Contract

Before designing the UI, identify:
- field name
- type
- required/optional
- format
- allowed range
- dependencies on other fields
- server-side validation
- default value
- null vs omitted semantics
- sensitivity
- persistence behavior

A form should reflect the actual backend contract rather than inventing independent rules.

---

## 4. Required vs Optional

Ask whether the system truly requires a field.

Prefer asking only for information necessary for:
- current task
- security
- legal/compliance requirement
- meaningful personalization

Do not make a field required merely because it is convenient for the database.

Clearly distinguish:
- required
- optional
- conditionally required

Do not use a visual asterisk without ensuring its meaning is communicated accessibly.

---

## 5. Field Labels

Every field needs a visible, meaningful label.

Good:
```text
Work email
[________________]
```

Bad:
```text
[Enter your email here]
```

with no persistent label.

Do not rely on placeholder text as the label.

Placeholders should provide example/format help, not replace field identification.

---

## 6. Input Types

Use the input mechanism that matches the data.

Examples:
- `email` for email
- `tel` for telephone
- `url` for URLs
- `number` when numeric semantics actually apply
- `date` for dates when appropriate
- password controls for passwords
- file input for uploads

Use autocomplete attributes where appropriate so browsers/password managers can help.

Do not use a generic text input when a more appropriate native control improves validation, keyboard, or accessibility.

---

## 7. Choice Controls

Choose based on number and mutual exclusivity.

### Radio
Small set; exactly one choice.

### Checkbox
Independent boolean or multiple-selection options.

### Select
A bounded set of options where a menu is appropriate.

### Combobox/search
Large/searchable sets.

### Segmented control/tabs
Closely related views or modes—not arbitrary form fields.

Do not use a dropdown for two choices merely because it looks compact.

---

## 8. Field Grouping

Group fields when users naturally understand them together.

Examples:
```text
Personal information
  Name
  Email
  Phone

Billing address
  Street
  City
  Postal code
```

Grouping can reduce cognitive load.

Avoid excessive sectioning for short forms.

---

## 9. Ordering Fields

Ask:
1. Which information is known first?
2. Which field depends on a previous answer?
3. Which fields are cognitively related?
4. Which fields are most important?
5. Can defaults/autocomplete reduce effort?

Do not force arbitrary database column order onto users.

---

## 10. Dependent Fields

Example:

```text
Country
   ↓
State/Region options
   ↓
Postal code
```

When one choice changes available fields:
- update dependent state clearly
- reset invalid dependent values
- do not silently preserve a value that is no longer valid
- explain why a field changed when the transition is surprising

Review race conditions if dependent data is fetched asynchronously.

---

## 11. Validation Strategy

Validation has three roles:

### Client validation
Fast feedback and UX.

### Server validation
Authoritative correctness/security boundary.

### Domain validation
Business rules involving current state/policy.

Never rely on client validation for security or data integrity.

---

## 12. Validation Timing

Choose timing based on the error type.

### Immediate
Useful for:
- character limits
- simple format corrections
- password feedback

Avoid noisy validation while the user is still typing an intermediate value.

### On blur
Useful for:
- email format
- required fields
- many individual field constraints

### On submit
Required as final authoritative validation.

Do not make users discover every possible error before they can attempt submission if doing so creates unnecessary friction.

---

## 13. Cross-Field Validation

Some rules depend on multiple fields:

```text
startDate < endDate
password == confirmPassword
minPrice <= maxPrice
```

Validate related fields together and clearly identify what must change.

Do not duplicate complex business policy across many client validators without a reliable source of truth.

---

## 14. Server-Side Validation Errors

The backend is authoritative.

A useful API validation error should identify:
- stable error code
- field/path
- problem category
- safe human guidance

The UI should map server errors to the corresponding field/state.

Example:

```json
{
  "code": "VALIDATION_FAILED",
  "details": [
    {
      "field": "email",
      "code": "EMAIL_ALREADY_USED"
    }
  ]
}
```

Do not parse human-readable backend messages to determine behavior.

Coordinate with `backend/api-design` and `backend/error-handling`.

---

## 15. Error Presentation

Field errors should appear close to the affected field.

For multiple errors, an error summary can help users find them quickly.

An error message should explain:
- what is wrong
- how to fix it when possible

Bad:
```text
Invalid input
```

Better:
```text
Enter a valid work email, such as name@company.com.
```

Do not reveal security-sensitive details unnecessarily.

---

## 16. Error Focus

After a failed submission:
- move/direct focus to an appropriate error summary or first invalid field
- preserve the rest of the form
- ensure the error is announced/accessibly associated

Do not steal focus for minor background validation while the user is typing.

---

## 17. Submission State

At submission:

```text
idle
 ↓
submitting
 ↓
success
or
error
```

For asynchronous long work:

```text
submitting
 ↓
queued
 ↓
processing
 ↓
completed / failed
```

The submit control should communicate progress.

Prevent duplicate submission when duplicate execution would be harmful.

The backend remains the authority for idempotency.

---

## 18. Submit Button Design

Do not blindly disable a submit button until "all fields are valid" if the user then has no clue what to fix.

Possible approaches:
- enable and validate on submit
- disable only while request is executing
- provide explicit prerequisite messaging

Use a disabled state when the action is genuinely unavailable, not merely because the form has not yet been successfully completed.

---

## 19. Preserve User Input

When the server rejects a form:
- retain valid fields
- retain recoverable invalid fields when safe
- show errors in context
- avoid resetting the entire form

After network timeout, users should generally not lose a carefully completed form.

Never discard user data merely because a request failed.

---

## 20. Duplicate Submission

Possible duplicate causes:
- double click
- keyboard activation
- browser retry
- network/client retry
- user opening multiple tabs

UI:
- show submitting state
- prevent accidental duplicate activation

Backend:
- use idempotency/constraints/concurrency protection where required

Do not rely on disabling the button as the only protection.

---

## 21. Dirty State / Unsaved Changes

For forms with meaningful unsaved work, determine:
- when the form becomes dirty
- when it is considered saved
- what happens on navigation
- what happens on refresh
- whether to warn
- whether draft persistence exists

Do not show "unsaved changes" after every focus interaction.

---

## 22. Autosave

For autosave:
- define save trigger
- debounce/throttle appropriately
- show saving/saved/error state
- preserve local work
- handle concurrent saves
- handle out-of-order responses

Do not show "Saved" until the intended persistence point is actually confirmed.

For collaborative edits, define conflict behavior.

---

## 23. Drafts

A draft flow needs:
- draft identity
- persistence semantics
- save state
- recovery
- expiration/cleanup policy where relevant
- conflict behavior
- authorization

Do not assume browser local storage is appropriate for sensitive information.

---

## 24. Multi-Step Forms

Use multiple steps when:
- there is meaningful cognitive grouping
- the workflow is genuinely long
- validation can happen progressively
- progress/return behavior benefits the user

Avoid splitting a simple 5-field form into 5 pages.

For multi-step flows:
- preserve entered values
- provide progress
- permit backward navigation safely
- define which validation blocks progression
- define save/resume if the workflow can be interrupted

---

## 25. Conditional Fields

When a field appears/disappears based on another selection:
- make the relationship understandable
- do not retain invalid hidden values silently
- decide whether hidden values are cleared or preserved
- ensure hidden fields are not accidentally submitted

Do not create confusing forms where changing one option silently changes many unseen values.

---

## 26. Sensitive Fields

For:
- passwords
- API keys
- payment data
- recovery information
- secrets

review:
- masking
- reveal/hide control
- autocomplete
- clipboard behavior
- browser autofill
- logging
- screenshots/visibility
- server-side handling

Never log sensitive form values.

Coordinate with `security/authentication` and `security/secrets-management`.

---

## 27. File Upload Forms

Define:
- allowed type
- maximum size
- count
- upload progress
- cancellation
- retry
- failure
- server validation/scanning
- removal/replacement behavior

Show selected filenames and validation results.

Do not treat client file extension/MIME as authoritative security validation.

---

## 28. Accessibility

Use semantic form controls and labels.

Ensure:
- keyboard completion
- visible focus
- error association
- accessible names
- required/invalid state communication
- sensible focus after submit failure

Use `frontend/accessibility` for detailed accessibility review.

---

## 29. Mobile Forms

Review:
- input type/keyboard
- focus
- viewport/keyboard obstruction
- vertical spacing
- button reachability
- long labels/errors
- autofill
- orientation changes

Do not force complex horizontal field layouts on narrow screens when stacking improves usability.

---

## 30. API Contract Mismatch

Watch for:

```text
frontend considers phone optional
backend considers phone required
```

or:

```text
frontend sends empty string
backend expects null
```

or:

```text
frontend treats 422 as server failure
backend uses it for validation
```

Cross-layer contract must be explicit.

Use `engineering/cross-layer-review`.

---

## 31. Review Procedure

For a form ask:

1. What is the user's goal?
2. What information is truly required?
3. What is the source-of-truth data contract?
4. Are labels/controls semantic?
5. When should each validation occur?
6. What happens on server validation failure?
7. Is user input preserved?
8. Can submission duplicate?
9. Is idempotency needed?
10. What happens on timeout?
11. What happens on refresh/navigation?
12. Are there dirty/draft/autosave semantics?
13. Are sensitive fields handled safely?
14. Is the flow keyboard/mobile accessible?
15. Are client and server contracts aligned?

---

## 32. Anti-Patterns

### Placeholder as Label
Disappears while typing and harms context.

### Client Validation Only
Can be bypassed and is not authoritative.

### Validate on Every Keystroke
Noisy and disruptive for intermediate values.

### Disabled Until Perfect
User cannot discover why they cannot submit.

### Reset Entire Form on Error
Destroys user work.

### Double-Submit Protection Only in UI
Doesn't protect against retries/multiple clients.

### Giant Monolithic Form
Unstructured hundreds-field interface.

### Wizard for Five Fields
Adds unnecessary navigation.

### Hidden Conditional Values
Invisible fields continue sending stale values.

### Autosave Says Saved
UI claims persistence before server confirmation.

### Sensitive Value in Logs
Credentials/PII leak through debugging.

---

## 33. Verification Checklist

- [ ] goal and data contract clear
- [ ] required/optional semantics justified
- [ ] native controls used
- [ ] labels persistent and accessible
- [ ] input types/autocomplete appropriate
- [ ] validation timing intentional
- [ ] server validation authoritative
- [ ] field errors associated
- [ ] submit state visible
- [ ] duplicate submission handled
- [ ] user input preserved
- [ ] timeout/network recovery designed
- [ ] dirty/draft/autosave behavior explicit
- [ ] multi-step flow justified if used
- [ ] sensitive fields reviewed
- [ ] file uploads bounded/safe
- [ ] mobile keyboard/layout tested
- [ ] keyboard/accessibility tested
- [ ] API/UI contracts aligned

## References
- `references/validation-timing.md`
- `references/error-mapping.md`
- `references/drafts-and-autosave.md`
- `references/multi-step-forms.md`
- `references/sensitive-fields.md`

## Cross-Skill Routing
For network/server lifecycle behavior, coordinate with `async-ui-states`.
For API request/response semantics, coordinate with `api-design`.
For labels, focus, and error accessibility, coordinate with `accessibility`.
