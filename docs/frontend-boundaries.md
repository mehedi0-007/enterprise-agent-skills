# V2 Frontend Semantic Boundaries

## Canonical Ownership

```text
ui-design
  → visual hierarchy, control placement, component choice

ux-design
  → task flow, interaction decisions, recovery

forms
  → data-entry behavior, validation UX, dirty/draft/save states

tables
  → collections, selection, filtering, sorting, bulk actions

navigation
  → information architecture, routes, URL/history

async-ui-states
  → network/server lifecycle, retries, stale responses, cancellation

responsive-design
  → adaptation to viewport/input constraints

accessibility
  → semantic/focus/keyboard/assistive behavior across all UI
```

## Cross-Cutting Rules

### Accessibility
`accessibility` is a constraint across all interactive skills. It does not own product UX decisions.

### Responsive Design
`responsive-design` changes layout/interaction under constraints. It does not replace `ui-design` or `ux-design`.

### Async UI
`async-ui-states` represents the actual server/network lifecycle. It does not define the backend contract; coordinate with `backend/api-design`.

### Forms
`forms` owns data-entry workflow. It should route complex async behavior to `async-ui-states` and API semantics to `backend/api-design`.

### Tables
`tables` owns collection interaction. It should route data-access performance to `database/query-optimization` and `database/indexing`, and authorization to `security/authorization`.

### Navigation
`navigation` owns information architecture and URL/history behavior. It should never be treated as the authorization boundary.

### UX/UI
`ui-design` chooses presentation; `ux-design` chooses task-flow behavior. Neither should invent backend semantics.

## Canonical Example

For "Export invoices":

```text
ui-design
  → where Export appears

ux-design
  → scope/confirmation/recovery flow

forms (if export options exist)
  → filter/date/file-format inputs

async-ui-states
  → queued/processing/completed/failed

tables
  → selection and current filter scope

navigation
  → whether export history has a dedicated route

accessibility
  → keyboard/focus/status semantics

responsive-design
  → mobile toolbar/dialog behavior

backend/api-design
  → request/status contract

security/api-security
  → resource limits/sensitive flow

authorization
  → who may export
```
