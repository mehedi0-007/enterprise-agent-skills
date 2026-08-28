---
name: accessibility
description: Design, implement, and review accessible web interfaces using semantic HTML, keyboard interaction, focus management, accessible names, form semantics, dynamic state communication, zoom/reflow, and appropriate ARIA patterns. Use for every interactive UI feature and during accessibility reviews.
---

# Accessibility — Production Playbook

## 1. Mission

Accessibility is part of functional correctness.

A feature is incomplete when a user:
- cannot operate it with a keyboard
- cannot understand it with assistive technology
- loses focus or context unexpectedly
- cannot complete the flow at common zoom/reflow settings
- cannot perceive state/error changes

Use native platform semantics first and add ARIA only when native semantics are insufficient. MDN and WAI guidance both emphasize semantic HTML, correct names/roles/states, and keyboard accessibility. citeturn814403search8turn814403search25

---

## 2. Activation

Use when:
- adding buttons/links/forms
- creating custom widgets
- implementing dialogs/menus/tabs
- adding loading/error/status behavior
- changing navigation
- building tables
- adding drag/drop or pointer-only interaction
- reviewing accessibility
- modifying focus behavior
- handling responsive/reflow requirements

Do not postpone accessibility until after visual implementation.

---

## 3. Semantic HTML First

Choose native elements by meaning:

- navigation → `<nav>`
- main content → `<main>`
- headings → `<h1>`–`<h6>`
- list → `<ul>/<ol>`
- link → `<a href>`
- action → `<button>`
- form field → `<input>/<select>/<textarea>`
- form → `<form>`
- table → semantic table elements
- disclosure → appropriate native element/pattern where possible

A semantic element gives browsers and assistive technologies useful built-in behavior.

Avoid:
```html
<div onclick="...">Save</div>
```

Prefer:
```html
<button type="button">Save</button>
```

Do not use ARIA to recreate semantics that HTML already provides.

---

## 4. Link vs Button

Use:
- link when navigation occurs
- button when an action occurs

A clickable `<div>` or `<span>` should generally be rejected unless there is an exceptional, well-understood reason.

A button naturally supports keyboard activation and semantic role.

---

## 5. Accessible Names

Every interactive control needs an accessible name.

Good:
```html
<button aria-label="Close settings">X</button>
```

Better when visible text can be used:
```html
<button>Close</button>
```

For icon-only controls, ensure:
- accessible name
- visible/familiar icon
- tooltip only as supplemental help

Do not use placeholder text as the only label.

---

## 6. Accessible Description vs Name

Do not overload `aria-label` when visible text can provide the control's name.

Use accessible descriptions for supplemental context when needed.

For example:
```text
Name: Delete project
Description: This permanently removes all project data.
```

The user should not have to infer the action from a cryptic icon.

---

## 7. Keyboard Operability

A complete interaction must be usable without a mouse.

Check:
- Tab sequence
- Enter/Space activation
- Escape dismissal where expected
- arrow-key behavior for composite widgets
- focus movement
- focus visibility
- no keyboard trap

Do not create custom keyboard behavior unless the interaction pattern actually requires it.

For complex patterns, follow the relevant WAI-ARIA Authoring Practices pattern rather than inventing key bindings. citeturn814403search25

---

## 8. Focus Visibility

Focus must remain visually apparent.

Do not write:

```css
outline: none;
```

without a strong, visible replacement.

W3C identifies obscuring/removing the focus indicator as an accessibility failure. citeturn814403search25

Use `:focus-visible` where appropriate to preserve strong keyboard focus without adding unnecessary focus styling for every pointer interaction.

Also check that fixed/sticky headers do not cover the focused element.

---

## 9. Focus Management

Focus should move deliberately after significant UI transitions.

### Dialog open
Move focus into the dialog according to the dialog pattern.

### Dialog close
Restore focus to the invoking control when practical.

### Navigation
Focus behavior should make the new context understandable, particularly for SPA route changes.

### Validation error
Move or direct focus appropriately so the user can find the problem.

Do not randomly call `.focus()` from many components and create unpredictable focus jumps.

---

## 10. Dialogs and Modals

A modal dialog needs:
- accessible name
- appropriate role/semantics
- focus entry
- managed focus while open
- keyboard dismissal where appropriate
- background interaction blocked when truly modal
- focus restoration on close

Prefer a robust accessible dialog component/library when available.

Do not create a modal from a generic `<div>` and assume `role="dialog"` alone makes it accessible.

---

## 11. Menus

A menu is not simply:
```text
a list of buttons inside a div
```

If implementing a true menu pattern, follow the appropriate ARIA interaction model:
- keyboard navigation
- focus behavior
- menuitem semantics
- escape behavior

If the UI is really just a list of ordinary actions, a simpler popover/list pattern may be more appropriate.

Do not use the ARIA `menu` role just because a UI visually looks like a dropdown.

---

## 12. Tabs

Tabs should only be used for genuinely related peer views.

A true tab pattern needs:
- tablist
- tab
- associated tabpanel
- selected state
- keyboard behavior appropriate to the chosen pattern
- focus handling

If the items navigate to independent pages, ordinary links may be more correct.

Semantic accuracy comes before visual resemblance.

---

## 13. Disclosure / Accordion

Use a disclosure pattern when content expands/collapses without changing the user's broader context.

The control should communicate:
- expanded/collapsed state
- accessible relationship to the controlled content

Prefer native semantics or a well-tested component pattern.

---

## 14. Forms

Every form field needs:
- accessible label/name
- clear required/optional semantics
- meaningful input type
- error association
- help text association when needed

Validation errors should be programmatically associated with the relevant input.

Use `frontend/forms` for broader form UX decisions.

---

## 15. Error Messages

Do not communicate errors using only:
- red color
- border color
- icon

Provide textual information.

For field errors:
```text
Email
[input]
Error: Enter a valid email address.
```

The error should be programmatically related to the field.

W3C guidance emphasizes that error identification and suggestions must be perceivable and understandable rather than solely visual. citeturn814403search24

---

## 16. Status Messages

Dynamic changes should be perceivable without requiring the user to notice a visual animation.

Examples:
- "Saved"
- "Uploading 3 files"
- "5 results found"
- "Payment failed"

Use appropriate live/status semantics when needed, but do not make every DOM change a live announcement.

MDN documents status messages and programmatic state communication as part of accessible dynamic interfaces. citeturn814403search5

---

## 17. Loading States

Loading state should be communicated accessibly.

For local actions:
- communicate button busy state appropriately
- do not destroy the accessible name

For content:
- preserve context
- avoid replacing the entire interface with an inaccessible spinner

For long operations:
- expose processing/progress state

Do not use animation as the only indicator.

---

## 18. Disabled vs aria-disabled

Native disabled controls behave differently from merely visually disabled controls.

A native disabled form control:
- is generally not focusable
- is removed from normal form submission behavior
- cannot be activated

MDN documents these semantics. citeturn814403search0

Use `aria-disabled="true"` when the control needs to remain discoverable/focusable and the application intentionally implements the disabled interaction model. `aria-disabled` does not automatically prevent activation. citeturn814403search1

Never add `aria-disabled` and forget to actually prevent the action.

---

## 19. Hidden vs Removed vs Inert

Understand the difference.

- `display:none` removes content from normal rendering/accessibility exposure.
- `hidden` similarly hides the content.
- `aria-hidden="true"` hides from assistive technologies but does not necessarily prevent keyboard interaction.
- `inert` is appropriate when content should not be interacted with while it remains present visually in supported environments.

Do not use `aria-hidden="true"` on a container that contains focusable controls that users can still reach.

---

## 20. Color and Contrast

Do not use color as the only way to convey:
- error
- success
- warning
- selection
- required state
- disabled state

Combine color with:
- text
- icon
- shape
- position
- pattern

Validate contrast against the applicable WCAG target for the product.

Do not pick colors first and "check accessibility later."

---

## 21. Reflow and Zoom

A web interface must remain usable when text is enlarged or the viewport is narrow.

Review:
- no critical content disappears
- no unavoidable two-dimensional scrolling for ordinary content
- controls remain reachable
- dialogs remain usable
- navigation remains understandable
- content order remains logical

Do not solve zoom problems by permanently shrinking text.

---

## 22. Responsive Accessibility

Responsive transformations must preserve semantics.

Example:
desktop table → mobile cards

If the content is no longer represented as a table, ensure:
- labels remain understandable
- reading order is logical
- actions are still accessible
- critical relationships are not lost

Do not visually hide essential information during responsive changes.

Use `frontend/responsive-design` for layout behavior and this skill for the accessibility implications.

---

## 23. Motion

Respect `prefers-reduced-motion`.

Non-essential animations should be reduced or removed when the user requests reduced motion.

Do not use motion to communicate the only meaning of an interaction.

---

## 24. Images and Icons

Meaningful images need appropriate alternative text.

Decorative images should not create unnecessary screen-reader noise.

For icons:
- informative icon → accessible text/label
- decorative icon adjacent to visible text → hide from assistive tech where appropriate
- icon-only action → accessible name required

Do not add meaningless `aria-label` to every decorative SVG.

---

## 25. Tables

Use semantic table markup for tabular data.

Ensure:
- header relationships
- meaningful captions/labels where appropriate
- row/column context
- keyboard navigation for interactive cells
- responsive transformation does not destroy meaning

Do not turn a simple table into a grid widget without needing grid behavior.

---

## 26. Custom Widgets

Before building a custom widget ask:

1. Is there a native HTML element?
2. Is there an established ARIA pattern?
3. Does the product really need custom behavior?
4. Can keyboard behavior be tested?
5. Can focus be managed?
6. Can screen-reader semantics be verified?

If the answer to #4–6 is no, the custom widget is not ready.

---

## 27. SPA Navigation

Single-page applications can change content without a full browser navigation.

When changing route/context:
- update the document title appropriately
- expose the new page/context to assistive technology
- manage focus deliberately
- keep URL/history semantics correct

Do not assume a visible screen change is enough for a screen-reader user to understand navigation.

---

## 28. Accessibility Tree Thinking

When reviewing a component, reason about:

```text
Name
Role
State
Value
Relationship
Keyboard behavior
```

Ask:
- what will assistive technology perceive?
- is the control's role correct?
- is its current state exposed?
- is it associated with the correct label/content?
- can it be operated?

Do not stop at visual inspection.

---

## 29. Testing Strategy

### Keyboard
Complete the entire workflow using only:
- Tab
- Shift+Tab
- Enter
- Space
- Escape
- relevant arrow keys

### Screen Reader
For important flows verify:
- headings
- landmarks
- control names
- state changes
- errors
- dialogs
- navigation

### Zoom/Reflow
Test enlarged text/zoom and narrow viewports.

### Automated
Use automated tools to catch common issues:
- missing labels
- contrast problems
- invalid ARIA
- missing names

Automation is a supplement, not proof of accessibility.

---

## 30. Review Procedure

For each interactive component ask:

1. What is the semantic HTML element?
2. Does native HTML solve it?
3. What is the accessible name?
4. What is the role?
5. What states/values change?
6. Can it be operated by keyboard?
7. Is focus visible?
8. Where does focus go after activation?
9. Are errors/status changes perceivable?
10. Does zoom/reflow preserve the task?
11. Does responsive transformation preserve meaning?
12. Is ARIA actually required?
13. What happens if assistive technology does not support a custom behavior exactly as intended?

---

## 31. Anti-Patterns

### Div Button
`<div onClick>` used for ordinary actions.

### ARIA as Decoration
Adding `aria-label` without understanding accessible naming.

### aria-hidden Focus Trap
Hiding a container from assistive tech while its controls remain focusable.

### Focus Removed
`outline: none` with no visible replacement.

### Color-Only State
Red border = error, with no text.

### Tooltip Labels
Critical instructions exist only on hover tooltip.

### Modal Without Focus
Dialog opens but focus stays behind it.

### Custom Menu Without Keyboard Model
Looks right, keyboard behavior missing.

### Disabled Mystery
`aria-disabled` added but action still executes.

### Automated-Test Theater
Passing an automated checker treated as complete accessibility proof.

### Accessibility After Styling
Semantics/focus are patched after the component is already built around incorrect DOM structure.

---

## 32. Verification Checklist

- [ ] semantic HTML used first
- [ ] interactive controls have accessible names
- [ ] link/button semantics correct
- [ ] keyboard operation complete
- [ ] focus visible
- [ ] focus entry/return handled
- [ ] dialogs/menus/tabs follow appropriate patterns
- [ ] errors programmatically associated
- [ ] dynamic status communicated appropriately
- [ ] disabled state semantics correct
- [ ] `aria-hidden` used safely
- [ ] color not sole state indicator
- [ ] zoom/reflow tested
- [ ] responsive transformation preserves meaning
- [ ] reduced motion considered
- [ ] images/icons have correct alternative treatment
- [ ] tables retain semantics
- [ ] automated accessibility checks run
- [ ] important flows manually tested

## References
- `references/native-semantics.md`
- `references/focus-and-dialogs.md`
- `references/forms-and-errors.md`
- `references/aria-decision.md`
- `references/verification.md`

## Cross-Skill Routing
Apply these constraints across `ui-design`, `forms`, and `navigation`.
Coordinate responsive semantic transformations with `responsive-design`.
