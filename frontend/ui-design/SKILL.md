---
name: ui-design
description: Design and review production web interfaces, component hierarchy, action placement, visual priority, feedback states, and interaction affordances. Use when deciding where a feature belongs, what UI pattern to use, which action is primary, or whether a screen communicates state and priority clearly.
---

# UI Design — Production Playbook

## 1. Mission

UI design is the translation of product intent into visible hierarchy and actionable controls.

The objective is not to make screens decorative.

A good interface lets a user quickly understand:
1. where they are
2. what matters
3. what they can do
4. what happened
5. what they should do next

Use semantic HTML and established interaction patterns before inventing custom components. Vercel's Web Interface Guidelines and MDN both emphasize semantic controls, clear interaction behavior, visible focus, and predictable states. citeturn194089search0turn814403search8

---

## 2. Activation

Use when:
- adding a feature to an existing screen
- deciding where an action belongs
- selecting button/menu/modal/drawer/page patterns
- designing dashboards/admin screens
- reviewing visual hierarchy
- adding destructive actions
- designing loading/empty/error states
- improving mobile interaction
- reviewing accessibility of custom UI

---

## 3. Start With the User Task

Before selecting a component, identify:

- user goal
- task frequency
- task urgency
- object/context
- action consequence
- whether action is reversible
- whether user needs persistent visibility
- whether action affects current object or entire page

Do not start with:
> "Should this be a modal or drawer?"

Start with:
> "What does the user need to accomplish?"

---

## 4. Feature Placement

Use the scope of the action to guide placement.

### Page-level action
Use page header/toolbar when the action applies to the current page/resource collection.

Examples:
- Create project
- Export report
- Manage settings

### Object-level action
Place near the object:
- table row actions
- card actions
- detail header

Examples:
- Edit invoice
- Archive document
- Assign project

### Secondary action
Use a context menu when:
- action is infrequent
- there are several secondary actions
- always-visible controls would clutter the UI

Do not hide high-frequency or critical actions in menus.

### Navigation
If something takes the user to another destination, use a link rather than a button.

### Action
If something changes state or performs work, use a button.

This distinction should remain consistent across the product.

---

## 5. Pattern Selection

### Button
Use for actions:
- save
- submit
- retry
- delete
- add

### Link
Use for navigation.

### Menu
Use for a compact set of secondary actions.

### Dialog
Use when a focused decision or short contextual interaction needs temporary attention.

Good:
- confirm destructive action
- short one-step confirmation
- focused small form

Poor:
- long multi-step workflow
- large data-entry process
- content users may need to bookmark/revisit

### Drawer/Sheet
Use when contextual work benefits from keeping the underlying page visible.

Good:
- filter controls
- quick edit
- details panel

### Full Page
Use when the workflow is:
- complex
- multi-step
- information-dense
- likely to be revisited/bookmarked
- important enough to deserve navigation history

### Tooltip
Use only for supplemental explanation.
Never hide essential instructions solely in a tooltip.

---

## 6. Primary vs Secondary Actions

Each screen should have a clear visual hierarchy.

Ask:
- what is the main successful outcome?
- which action most directly achieves it?
- what actions are secondary?
- which actions are dangerous?

Use stronger visual emphasis for the primary task.

Avoid:
- several equally prominent primary buttons
- multiple destructive actions styled identically to routine actions
- large "Cancel" beside the true primary action unless the task warrants it

The UI should communicate priority without requiring the user to read everything.

---

## 7. Action Ordering

For two-button decisions, place and label actions according to the product's established interaction convention.

More important than left/right placement:
- labels are explicit
- primary action is visually clear
- destructive action is recognizable
- keyboard/focus order is logical
- behavior is consistent across the product

Never use ambiguous labels such as:
- Continue
- Proceed
- Okay

when the real consequence can be named.

Prefer:
- Delete account
- Publish changes
- Send invitation

---

## 8. Destructive Actions

The more irreversible or costly the action, the more deliberate the interaction should be.

Consider:

```text
ordinary reversible action
    ↓
direct activation is often appropriate

important but recoverable action
    ↓
clear feedback / undo may be enough

irreversible or high-impact action
    ↓
explicit confirmation + consequence + deliberate action
```

A destructive dialog should state:
- what will happen
- what object is affected
- whether it is reversible
- what the user should do to confirm

Do not make the confirm button say merely "Yes."

Example:

```text
Delete "Acme Workspace"?

All projects, members, and billing history will be inaccessible.

[Cancel] [Delete workspace]
```

If an undo/recovery mechanism is safer and practical, prefer it over unnecessary confirmation friction.

---

## 9. Visual Hierarchy

Hierarchy can be created through:
- placement
- spacing
- typography
- size
- contrast
- grouping
- alignment

Do not use color/decoration as the only mechanism.

A page should have an obvious reading/task order.

### Review questions
- Can the user identify the page/resource?
- Is the primary task discoverable?
- Are related controls grouped?
- Are secondary details visually subordinate?
- Are warnings/destructive states visually distinct?
- Does whitespace clarify grouping?

---

## 10. Density

Do not optimize for maximum information density by default.

Density should follow task:
- dashboards may be dense
- onboarding should be calmer
- data-entry screens need readable fields
- operational tables may need compact rows

Users often need to scan, compare, and act—not merely see more pixels of information.

---

## 11. Forms

A form should communicate:
- what information is required
- what is optional
- what format is expected
- what failed
- what was saved

Use visible labels and appropriate controls.

Do not use placeholders as the only labels.

For form-specific guidance use `frontend/forms`.

---

## 12. Tables and Data-Dense Views

Do not display every available database field.

Choose columns based on:
- task relevance
- scanning needs
- comparison needs
- action needs

Secondary information can move to:
- detail pages
- expandable rows
- contextual menus
- hover-only supplemental content only when it is truly optional
- responsive detail views

For table behavior use `frontend/tables`.

---

## 13. Empty States

An empty state should distinguish:

### No data exists
Explain what the feature is and how to create the first item.

### No search/filter results
Explain that the current criteria returned nothing and provide a way to adjust filters.

These are different product states.

Good empty state:
```text
No projects yet

Create your first project to start organizing work.

[Create project]
```

Bad:
```text
No data.
```

---

## 14. Error States

Errors should be visible, understandable, and recoverable.

Use:
- field errors for field problems
- local error for local component failure
- banner for persistent page-level issue
- global alert for system-wide issue

Provide a recovery path where possible:
- Retry
- Edit input
- Reload
- Contact support
- Go back

Do not make a transient toast the only place a critical failure is explained.

---

## 15. Loading States

Choose the treatment based on scope and duration.

### Button/local action
Show progress on the initiating control.

### Content fetch
Use stable skeleton or local loading state.

### Long-running job
Use progress/queued/processing state.

Avoid layout jumps.

Vercel's guidelines specifically recommend avoiding layout shift and using skeletons that mirror the final content structure. citeturn194089search0

---

## 16. State Completeness

Do not design only:

```text
happy populated screen
```

For meaningful screens, consider:

```text
loading
success/populated
empty
no-results
permission denied
validation error
server error
offline/timeout
partial data
stale data
processing
completed
```

A production UI is the union of its states, not its screenshot at 100% success.

---

## 17. Disabled vs Hidden

Hide something when the user should not discover/use it in the current context.

Disable something when:
- the action is relevant
- the user should understand it exists
- it is temporarily unavailable
- a specific prerequisite has not been met

If you disable a control, make the reason discoverable.

Do not disable primary actions merely because validation is incomplete if the user then cannot understand what needs fixing.

For accessibility implications, see `frontend/accessibility`.

---

## 18. Confirmation vs Undo

Confirmation is not automatically better.

Use confirmation when:
- action is destructive/high-impact
- consequences are significant
- recovery is difficult
- users commonly make accidental mistakes

Prefer undo when:
- action is reversible
- immediate feedback is possible
- users benefit from speed
- a safe recovery path exists

Excessive confirmation produces confirmation fatigue.

---

## 19. Modals and Focus

A modal should not be a styling decision only.

When using a dialog:
- move focus appropriately
- provide accessible name
- constrain interaction to the dialog when modal semantics are appropriate
- support keyboard dismissal when the pattern permits
- restore focus after close
- prevent background interaction

Do not build a custom dialog from generic `<div>` elements when a robust accessible dialog component exists.

---

## 20. Iconography

Icons should reinforce recognizable actions.

Good:
- trash for delete
- plus for add
- magnifying glass for search

Less clear:
- abstract icon whose meaning requires guessing

Icon-only controls need accessible names.

Do not sacrifice clarity to reduce visible text.

---

## 21. Notifications

Choose based on persistence and importance:

### Toast
Good for:
- transient confirmation
- low-risk status

### Inline
Good for:
- field/local issues
- persistent task guidance

### Banner
Good for:
- page-level system state

### Dialog
Good for:
- decisions requiring attention

### Full page
Good for:
- critical system state requiring dedicated action

Do not make every event a toast.

---

## 22. Responsive Behavior

Do not simply shrink desktop.

Decide what happens to:
- navigation
- tables
- action groups
- dialogs
- forms
- secondary information
- dense content

For responsive decisions use `frontend/responsive-design`.

---

## 23. Accessibility as a Design Requirement

Accessibility should be considered before implementation.

At minimum:
- native semantic elements
- visible keyboard focus
- accessible names
- keyboard operation
- error/status communication
- color is not the only signal

Use `frontend/accessibility` for detailed review.

---

## 24. Component Reuse

Reuse components when their semantics and behavior match.

Do not force unrelated interactions into one "universal component."

A shared component should have:
- consistent behavior
- predictable states
- clear API
- accessibility built in

Duplication is sometimes preferable to a misleading abstraction.

---

## 25. Design Consistency

Users learn product conventions.

Keep consistent:
- primary button treatment
- destructive action behavior
- form validation
- loading indicators
- modal behavior
- navigation patterns
- table actions
- error messages

Consistency should reduce cognitive load.

Do not force consistency when the task semantics genuinely differ.

---

## 26. Review Procedure

When reviewing a UI feature:

1. What user task does this support?
2. Where would users naturally look for it?
3. Is the action page-, object-, or navigation-level?
4. Is the control type semantically correct?
5. Is primary/secondary hierarchy clear?
6. What happens on activation?
7. What happens while processing?
8. What happens on success?
9. What happens on failure?
10. What happens with empty/no-result state?
11. Is there a recovery path?
12. Is the action destructive?
13. Is keyboard interaction correct?
14. Does mobile layout still work?
15. Are sensitive actions appropriately confirmed/audited?

---

## 27. Anti-Patterns

### Everything Is a Modal
Creates interruption and poor navigation.

### Everything Is a Button
Navigation should use links.

### Everything Is a Toast
Important state disappears.

### Ambiguous Actions
"Continue" instead of explicit consequences.

### Disabled Mystery
Button disabled with no explanation.

### Empty State = Error
No data is not the same as failure.

### Desktop Shrink
Desktop UI squeezed into mobile.

### Icon-Only Everywhere
Users must guess meaning.

### Color-Only State
Fails accessibility and comprehension.

### One Primary Button Everywhere
Destroys visual hierarchy.

### Confirm Everything
Creates confirmation fatigue.

### Generic Universal Component
One component tries to represent unrelated interaction semantics.

---

## 28. Verification Checklist

- [ ] user task is clear
- [ ] feature placement follows task scope
- [ ] semantic control type chosen
- [ ] primary/secondary hierarchy clear
- [ ] labels describe actual actions
- [ ] destructive behavior deliberate
- [ ] loading/success/error states designed
- [ ] empty/no-result states distinguishable
- [ ] recovery path exists
- [ ] keyboard/focus behavior considered
- [ ] mobile behavior considered
- [ ] no state relies only on color
- [ ] shared components retain consistent semantics
- [ ] unnecessary modal/confirmation friction avoided
- [ ] important interactions tested in realistic flows

## References
- `references/pattern-selection.md`
- `references/hierarchy.md`
- `references/states.md`
- `references/action-risk.md`

## Cross-Skill Routing
For task-flow and recovery behavior, coordinate with `ux-design`.
For accessible semantics and interaction, coordinate with `accessibility`.
For viewport/layout adaptation, coordinate with `responsive-design`.
