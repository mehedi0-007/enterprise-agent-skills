# V2 Frontend Conflict Rules

## 1. Hidden vs Forbidden

Hiding a control can improve UX. It is never authorization.

## 2. Loading vs Processing

A request being accepted is not the same as work being completed.

HTTP/API semantics come from `backend/api-design`; representation comes from `async-ui-states`.

## 3. Optimistic UI

Optimistic state is a prediction, not canonical state.

The UI must reconcile with confirmed server state.

## 4. Disabled Controls

A disabled button is a UX state, not a concurrency or authorization guarantee.

## 5. Tables and Performance

Do not solve a million-row backend problem by rendering a million rows and adding virtualization.

Bound data server-side first; then optimize browser rendering if needed.

## 6. Responsive vs Accessibility

A mobile transformation must preserve semantic relationships, focusability, and keyboard/screen-reader behavior.

## 7. URL vs UI State

Shareable/reloadable application state may belong in the URL.
Transient visual state usually belongs locally.

Do not put secrets or sensitive credentials in URLs.

## 8. Errors

Frontend should map stable backend error semantics to UX behavior. Do not branch on human-readable messages.

## 9. Retry

The UI should not blindly retry non-idempotent mutations after an ambiguous timeout.

Use backend idempotency/status reconciliation when required.

## 10. Confirmation

Confirmation should be risk-based. Do not add modal friction simply because an action is destructive in name; consider actual reversibility and impact.
