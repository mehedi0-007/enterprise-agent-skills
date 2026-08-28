---
name: tables
description: Design and review production data tables for SaaS, admin, reporting, billing, audit, and operational interfaces. Use when implementing sorting, filtering, pagination, row selection, bulk actions, inline editing, responsive behavior, large datasets, or table accessibility.
---

# Tables — Production Playbook

## 1. Mission

A table should optimize the user's actual task:

- scanning
- comparing
- finding
- filtering
- sorting
- acting
- reviewing status
- bulk processing

A table is not a place to display every field available in the database.

---

## 2. Activation

Use when:
- building/administering a list of records
- adding columns
- adding sorting/filtering/search
- adding pagination/cursors
- adding row selection
- adding bulk actions
- adding inline editing
- supporting large datasets
- making tables responsive
- reviewing table accessibility/performance

---

## 3. Start With the Job to Be Done

Ask:
1. What do users compare?
2. What do they scan for?
3. What identifies a row?
4. Which state/status matters?
5. Which action is most frequent?
6. Which information is secondary?
7. How many records can exist?
8. Is the table operational or analytical?

Use these answers to determine columns and interactions.

Do not start from:
```text
SELECT * FROM entity
```
and turn every field into a column.

---

## 4. Column Selection

Prioritize:
- identity
- essential context
- status
- high-value metrics
- common action targets

Move secondary information to:
- row details
- expanded content
- detail page
- drawer
- contextual menu

A table becomes difficult to scan when every possible field is visible.

---

## 5. Column Ordering

Common priority:
```text
identity → status/context → key metrics → secondary metadata → actions
```

But use the actual workflow.

Keep row actions consistently placed.

Do not move the identity column unpredictably between screens.

---

## 6. Width and Alignment

Use alignment that improves scanning:
- text generally left-aligned
- numbers generally aligned consistently
- dates/statuses use predictable formatting

Avoid arbitrary widths that create excessive empty space or wrap critical values.

Allow sensible column resizing only when the product actually benefits from it.

---

## 7. Formatting

Use consistent:
- date/time format
- timezone interpretation
- currency/number format
- empty value treatment
- status labels

Do not make users infer:
```text
— = null?
0 = none?
N/A = unavailable?
```

Define the product convention.

---

## 8. Sorting

Sorting should answer a real user question.

Examples:
- newest
- oldest
- highest amount
- status
- last updated

Define:
- allowed sort fields
- ascending/descending behavior
- default order
- deterministic tie-breaker

If pagination is present, stable ordering is critical.

Example:
```text
ORDER BY created_at DESC, id DESC
```

The unique tie-breaker prevents rows with equal primary sort values from moving unpredictably between pages.

---

## 9. Server vs Client Sorting

Use client-side sorting when:
- dataset is small
- all data is already loaded
- sort is inexpensive

Use server-side sorting when:
- dataset is large
- pagination is server-side
- only a subset is loaded
- sorting requires database/index support

Do not download 100,000 rows just to sort them in the browser.

---

## 10. Filtering

Filters should correspond to meaningful user tasks.

Good:
- status
- date range
- customer
- owner
- category

Avoid:
- exposing every database field
- dozens of rarely used filters by default

For advanced filters:
- use a dedicated filter drawer/panel
- show active filter state
- provide clear/reset behavior
- preserve filters across navigation when useful

---

## 11. Search

Search semantics must be explicit:
- which fields?
- exact vs partial?
- case sensitivity?
- tokenization?
- ranking?
- minimum query length?
- debounce?
- server-side or local?

Do not call a substring filter "search" when the dataset requires full-text or indexed search semantics.

---

## 12. Pagination

For large datasets:
- paginate on the server
- bound page size
- define default size
- define maximum size
- preserve deterministic order

Use offset/page pagination when page-number navigation is useful and dataset behavior permits it.

Consider cursor/keyset pagination when:
- dataset is large
- data changes frequently
- deep traversal matters

Coordinate with:
- `database/query-optimization`
- `database/indexing`
- `backend/api-design`

---

## 13. Empty States

Distinguish:

### No records
```text
No invoices yet.
Create an invoice to get started.
```

### No search/filter results
```text
No invoices match these filters.
Clear filters / adjust search.
```

### Permission-limited
Do not falsely claim that no data exists if the real condition is insufficient access.

---

## 14. Loading States

Use:
- skeleton rows for initial table load when helpful
- local loading for refresh/filter/sort
- row-level progress for row-specific actions

Do not blank the entire table for every small refresh.

Preserve column structure during loading to avoid layout shifts.

---

## 15. Errors

Table errors should preserve useful context.

Examples:
- initial load failed → clear retry state
- filter request failed → preserve existing rows + indicate refresh failure where safe
- row mutation failed → show row-level error/retry
- permission changed → reflect new access state

Do not replace useful existing data with a generic full-page "Something went wrong" for a refresh failure when stale data can still help and the product permits it.

---

## 16. Row Selection

Selection should be explicit.

Define:
- selecting one row
- selecting page
- selecting all matching records
- deselecting
- selection persistence across pages
- selection after filtering/sorting
- selection after row mutation/deletion

Do not imply "select all" means all dataset rows if it only means current page rows.

---

## 17. Bulk Actions

Bulk actions have amplified impact.

For every bulk action define:
- max selection
- authorization per item
- atomic vs best-effort behavior
- duplicate rows
- partial failures
- progress
- retry
- destructive confirmation
- audit requirements

Example:

```text
25 selected
[Archive] [Export] [Delete]
```

The UI should make the scope visible.

Never allow the UI to authorize a bulk action; the backend must enforce per-resource permissions.

---

## 18. Bulk Failure Semantics

If 100 records are selected and 7 fail:

Choose intentionally:
- all-or-nothing
- partial success
- retry failed only

Communicate:
- succeeded count
- failed count
- reasons where safe
- next action

Do not report:
```text
Success
```
when only part of the operation succeeded.

---

## 19. Row Actions

Actions should be:
- discoverable
- consistent
- properly scoped to the row

For a small number of common actions:
```text
Edit | View
```

For many secondary actions:
```text
More ▾
```

Destructive actions should not be accidentally adjacent to routine actions without enough separation.

---

## 20. Inline Editing

Use inline editing when:
- value is simple
- change is low-risk
- users edit many rows
- context should remain visible

Prefer a detail form/page when:
- many fields
- complex validation
- dependent fields
- significant side effects
- difficult error recovery

Inline editing should define:
- save trigger
- cancel
- loading state
- validation
- concurrency/stale data behavior

---

## 21. Concurrency in Tables

Tables often expose stale state.

Example:
```text
Row says PENDING
another user approves it
current user clicks Cancel
```

Backend should enforce the state transition.

UI should respond to conflict:
- refresh
- conflict message
- update row state

Do not trust the displayed row state as authorization/correctness.

Use `backend/concurrency` and `backend/transactions` for server behavior.

---

## 22. Responsive Tables

Choose deliberately:

### Horizontal scroll
Good when column comparison is important.

### Priority columns + details
Good when scanning is more important than full comparison.

### Expandable row
Good for secondary information.

### Card transformation
Good when record-level mobile scanning is the primary task.

Do not shrink all columns until text becomes unreadable.

Use `frontend/responsive-design`.

---

## 23. Mobile Table Actions

On touch:
- maintain useful target sizes
- avoid hover-only actions
- keep row action access discoverable
- avoid placing destructive controls where accidental taps are likely

Long-press interactions should not be the only way to access an action.

---

## 24. Accessibility

Use real table semantics when content is tabular.

Review:
- column headers
- row headers where appropriate
- table caption/label where needed
- focus behavior for interactive cells
- checkbox labeling
- sort state
- selected state
- bulk selection announcements

A sortable column header should communicate its current sort state accessibly.

Do not create an enormous ARIA grid when a semantic table with buttons/links is sufficient.

Use `frontend/accessibility` for detailed semantic/focus rules.

---

## 25. Performance

For large tables consider:
- server-side pagination
- server-side filtering/sorting
- bounded result size
- selective projections
- indexed query paths
- virtualization only when necessary
- avoiding repeated row-level queries

Coordinate backend/database skills.

Do not add virtualization automatically. It can make:
- keyboard navigation
- browser search
- screen readers
- selection
- measurement
more complex.

Use virtualization only when actual rendering volume is a bottleneck.

---

## 26. Virtualization

Consider when:
- thousands of DOM rows genuinely hurt rendering
- users need continuous scrolling
- dataset is already bounded/streamed appropriately

Before using it:
- measure actual browser rendering cost
- verify accessibility
- verify keyboard behavior
- verify row height stability
- verify selection/interaction

Do not use virtualization to compensate for unbounded server responses.

---

## 27. Refresh and Polling

If a table refreshes:
- indicate that data is updating when needed
- preserve current context
- avoid resetting filters/selection without reason
- handle concurrent edits
- avoid excessive polling

For real-time updates, define:
- update frequency
- ordering
- conflict behavior
- whether user edits can be overwritten

---

## 28. Data Freshness

For operational dashboards, communicate freshness when it matters.

Examples:
```text
Updated just now
Updated 2 minutes ago
Live
```

Do not imply real-time accuracy when data is cached/delayed.

---

## 29. Table + Permissions

Rows may be accessible while actions differ by permission.

Example:
- user can view invoice
- cannot approve invoice
- can export only if permission allows

The UI should reflect capability appropriately, but backend authorization remains authoritative.

For object/function/field rules use `security/authorization`.

---

## 30. Table + API Contract

A table consumes backend semantics.

Review:
- pagination fields
- cursor semantics
- stable sorting
- filter fields
- error codes
- 403/404 behavior
- rate limits
- partial bulk results

For large tables, UI and API pagination strategy must be designed together.

---

## 31. Testing Strategy

Test:
- empty dataset
- no-result filters
- large dataset
- slow initial load
- slow refresh
- sort/filter race
- selection across pages
- bulk partial failures
- row mutation failure
- concurrent updates
- permission changes
- responsive layout
- keyboard navigation
- screen reader semantics

---

## 32. Review Procedure

1. What task does the table support?
2. Which columns are essential?
3. What is the identity/context column?
4. Which sorting/filtering operations matter?
5. Is ordering deterministic?
6. Is pagination bounded?
7. Does the API support the interaction efficiently?
8. What happens when filters return nothing?
9. What happens when loading fails?
10. How does selection behave across pages?
11. What happens with partial bulk failure?
12. What happens when another user changes the row?
13. What happens on mobile?
14. Are semantics accessible?
15. Is rendering/data volume actually a performance issue?

---

## 33. Anti-Patterns

### Database Dump UI
Every DB column becomes a visible column.

### Client-Side Million-Row Table
Huge dataset downloaded to browser.

### Unstable Pagination
No deterministic ordering.

### Select All Ambiguity
"Select all" only means current page while UI suggests all results.

### Bulk Without Per-Item Authorization
One permission grants access to every item.

### Partial Success Hidden
Some actions fail but UI reports total success.

### Hover-Only Actions
Critical actions inaccessible to touch/keyboard.

### Virtualization First
Complexity added without measuring rendering bottleneck.

### Inline Edit Everything
Complex workflows forced into tiny cells.

### Full Table Reset on Error
A refresh failure destroys useful existing context.

### Stale State Treated as Truth
UI assumes displayed status is still valid.

### Arbitrary Sort
Clients can sort by any database field without cost/security review.

---

## 34. Verification Checklist

- [ ] table serves a defined user task
- [ ] columns prioritized
- [ ] identity and actions clear
- [ ] sorting meaningful
- [ ] deterministic ordering
- [ ] filters useful/allow-listed
- [ ] pagination bounded
- [ ] empty/no-result states distinct
- [ ] loading/error states appropriate
- [ ] selection semantics explicit
- [ ] bulk scope clear
- [ ] partial failure handled
- [ ] row concurrency considered
- [ ] permissions reflected
- [ ] responsive strategy chosen
- [ ] semantic accessibility verified
- [ ] rendering/data performance measured
- [ ] API/database contracts aligned

## References
- `references/pagination-selection.md`
- `references/bulk-actions.md`
- `references/responsive-tables.md`
- `references/accessibility.md`
- `references/large-data.md`

## Cross-Skill Routing
For responsive table behavior, coordinate with `responsive-design`.
For semantic/keyboard behavior, coordinate with `accessibility`.
For access-control decisions, coordinate with `authorization`.
For large-data/query performance, coordinate with `query-optimization`.
