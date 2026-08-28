---
name: responsive-design
description: Design and review web interfaces that remain usable across mobile, tablet, laptop, and large screens. Use when layout, navigation, tables, forms, dialogs, action groups, or content density must adapt to viewport and input constraints.
---

# Responsive Design — Production Playbook

## 1. Mission

Responsive design is about preserving task completion, hierarchy, readability, and interaction quality as available space and input methods change.

Do not treat responsive work as:
```text
desktop CSS
→ add 3 media queries
→ call it responsive
```

Instead, design for changing constraints:
- viewport width/height
- touch vs pointer
- keyboard input
- text growth/localization
- dynamic data size
- device safe areas
- zoom/reflow

---

## 2. Activation

Use when:
- creating new layouts
- adding mobile support
- changing navigation
- building tables/admin panels
- adding dialogs/drawers
- designing forms
- adding sticky/fixed controls
- reviewing responsive regressions

---

## 3. Start With Content, Not Device Names

Do not begin with:
- iPhone breakpoint
- tablet breakpoint
- desktop breakpoint

Begin with:
- minimum readable width
- when columns become too narrow
- when navigation no longer fits
- when action groups wrap badly
- when forms become too wide/narrow
- when dialogs exceed viewport height
- when tables stop being scannable

Choose breakpoints where the content/interface fails.

Vercel's Web Interface Guidelines explicitly recommend testing mobile, laptop, and ultra-wide layouts and favor CSS-driven layout over JavaScript measurement where possible. citeturn194089search0

---

## 4. Layout Model

Prefer:
- CSS flexbox
- CSS grid
- max-width containers
- fluid sizing
- intrinsic sizing
- wrapping
- min/max constraints

Avoid:
- fixed widths everywhere
- hardcoded viewport calculations when CSS can solve the problem
- measuring DOM layout in JavaScript for ordinary responsive layout
- absolute-positioned page layouts that collapse on content growth

Use JavaScript for behavior when necessary, not to manually recreate CSS layout.

---

## 5. Breakpoint Decision Process

A breakpoint is justified when the current layout can no longer:
- preserve hierarchy
- keep controls usable
- keep text readable
- keep related content grouped
- maintain acceptable scrolling/interaction

Decision:

```text
Can current layout still complete the task?
        ↓ yes
Keep layout
        ↓ no
What changed?
 ├── navigation width → collapse/reorganize navigation
 ├── action group → wrap/menu/stack
 ├── columns → remove/deprioritize/transform
 ├── form → stack/group differently
 ├── dialog → adapt to sheet/full-screen
 └── content → reflow/reorder
```

Do not introduce a breakpoint just because another framework uses one.

---

## 6. Mobile Is a Different Constraint Set

At small widths:
- prioritize primary actions
- reduce secondary clutter
- preserve readable text
- avoid tiny controls
- ensure horizontal relationships remain understandable
- minimize accidental destructive activation
- keep important navigation reachable

Do not simply scale desktop typography and spacing down.

---

## 7. Touch

Touch interfaces have less precision than a mouse.

Review:
- target size
- spacing between adjacent controls
- drag/drop alternatives
- hover-dependent behavior
- context menus
- swipe interactions
- sticky controls

Do not make essential functionality depend solely on hover.

If an interaction works with pointer hover but has no equivalent on touch/keyboard, it is incomplete.

---

## 8. Keyboard

Responsive behavior must not break keyboard workflows.

Check:
- tab order
- focus visibility
- focus after menus/dialogs
- no keyboard trap
- controls remain reachable when navigation collapses
- responsive reorder does not create confusing DOM order

Visual order and DOM order should not become dangerously inconsistent.

Use `frontend/accessibility` for detailed focus/keyboard rules.

---

## 9. Navigation

At larger widths:
- persistent sidebar/top navigation may be appropriate

At smaller widths:
- collapse into an accessible menu/drawer when there are many destinations
- keep primary destinations reachable
- retain clear current-location state

Do not hide primary navigation behind an interaction that is difficult to discover.

Avoid duplicate navigation structures unless they have clear behavior.

---

## 10. Tables

Tables often require special responsive treatment.

Possible strategies:
1. horizontal scrolling
2. hide low-priority columns
3. move details into expandable rows
4. transform rows into cards
5. use a dedicated detail page

Choose based on the user's task.

### Use horizontal scrolling when:
- comparison across columns is important
- the table remains semantically a table
- the content cannot reasonably be removed

### Transform when:
- mobile users need record-by-record scanning
- column comparison is less important
- actions/details can be reorganized

Do not shrink fonts until the table is technically visible but practically unusable.

---

## 11. Forms

On narrow screens:
- stack fields when horizontal grouping no longer helps
- preserve logical field order
- avoid excessively long labels/inputs
- keep submit actions accessible
- prevent keyboard from obscuring important controls

On wide screens:
- do not stretch short fields across the full viewport without reason
- group related fields

Use `frontend/forms` for validation/state behavior.

---

## 12. Dialogs and Drawers

A desktop dialog may need to become:
- a full-width sheet
- full-screen modal
- vertically scrollable panel

At small heights, a modal that exceeds the viewport becomes unusable.

Ensure:
- header/close action remains accessible
- content can scroll
- action buttons remain reachable
- focus management remains correct
- safe-area insets are considered when edge-attached/fixed

Do not assume a desktop-sized centered modal will work on mobile.

---

## 13. Action Groups

When a toolbar has:

```text
Create | Import | Export | Filter | Refresh | More
```

review what happens as width decreases.

Possible strategy:
```text
Create | Filter | More
```

with less frequent operations moved to `More`.

Do not hide the primary action merely to make the toolbar fit.

---

## 14. Dense Admin Interfaces

Admin/SaaS interfaces can remain information-dense, but density must adapt.

At small width:
- preserve identity and action-critical data
- move secondary data to details
- preserve row actions
- maintain status visibility
- avoid reducing tap target size

Do not transform every table into cards automatically. The interaction model may become slower or less scannable.

---

## 15. Large Screens / Ultra-Wide

More width is not always better.

Use:
- max-width content containers
- multi-column layouts when they improve task flow
- balanced whitespace
- stable reading widths

Avoid:
- 100% width text blocks
- controls spread to opposite edges without grouping
- huge gaps that disconnect labels from actions

Vercel's guidance specifically calls out ultra-wide layouts as a separate verification condition. citeturn194089search0

---

## 16. Dynamic Content

Responsive layouts must survive:
- long names
- long translations
- large numbers
- error messages
- optional fields
- user-generated content
- different font sizes

Never assume:
```text
button label = 8 characters
username = short
error = one line
```

Check wrapping and overflow.

---

## 17. Localization

Text length can expand significantly in other languages.

Review:
- buttons
- navigation
- table headers
- dialogs
- form labels
- status messages

Do not solve localization overflow by permanently truncating meaningful text.

Use responsive/wrapping patterns that preserve comprehension.

---

## 18. Zoom and Reflow

Responsive layouts should remain usable under browser zoom and reflow constraints.

Do not:
- rely on fixed pixel canvases
- make text scale with viewport width in ways that become unreadable
- hide essential content when zoomed
- require two-dimensional scrolling for ordinary content when avoidable

Use semantic structure and flexible layout.

---

## 19. Safe Areas

For fixed/sticky UI on mobile:
- consider device safe-area insets
- prevent controls from being obscured by system UI

Particularly relevant to:
- bottom sheets
- fixed bottom actions
- full-screen drawers
- mobile navigation

Do not hardcode one device's inset.

---

## 20. Sticky and Fixed Elements

Sticky/fixed UI can improve access but creates risks:
- content obstruction
- reduced viewport
- keyboard overlap
- mobile safe-area issues
- focus hidden behind fixed bars

For every fixed element ask:
- does it cover content?
- can keyboard users reach covered controls?
- what happens at short viewport heights?
- does zoom create overlap?

---

## 21. Overflow Strategy

Every overflow should be intentional.

Choose:
- wrap
- truncate with accessible full value
- horizontal scroll
- collapse
- move to details
- resize container

Do not use:
```css
overflow: hidden;
```
merely to hide a layout bug if content becomes inaccessible.

---

## 22. Responsive Images / Media

Use responsive image sizing/cropping appropriate to content importance.

Review:
- loading cost
- aspect ratio
- object fit
- intrinsic dimensions
- layout stability

Do not allow images to cause unexpected layout shift.

---

## 23. Motion and Responsive Behavior

Avoid adding complex responsive animations that:
- delay task completion
- create motion accessibility problems
- behave unpredictably on touch

Respect reduced-motion preferences.

---

## 24. Testing Matrix

A meaningful responsive review includes at least:

### Width
- narrow mobile
- normal mobile
- tablet-ish width
- laptop
- large desktop
- ultra-wide

### Height
- short viewport
- normal viewport
- tall viewport

### Input
- mouse/pointer
- touch
- keyboard

### Content
- long labels
- long names
- empty data
- large data
- errors
- localized strings

### Accessibility
- zoom
- keyboard
- reduced motion
- screen reader where relevant

Do not validate only by resizing one desktop browser window.

---

## 25. Review Procedure

For each responsive feature ask:

1. What is the primary user task?
2. What breaks first as width decreases?
3. What should remain visible?
4. What can move into a menu/details view?
5. Does interaction mode change from pointer to touch?
6. Does keyboard access remain correct?
7. Do dialogs/forms still fit?
8. Do tables remain useful?
9. Do long strings overflow?
10. Does zoom/reflow work?
11. Does fixed UI obscure content?
12. Does the design work on very wide screens?
13. Are loading/error/empty states still usable?

---

## 26. Anti-Patterns

### Device Breakpoint First
Choosing breakpoints from device lists rather than content failure.

### Desktop Shrink
Everything becomes smaller until it barely fits.

### Hover Dependency
Critical actions only appear on hover.

### Tiny Mobile Controls
Reducing target size to fit more content.

### Table Squashing
Unreadable columns instead of a deliberate mobile strategy.

### Fixed Canvas
Desktop layout with horizontal scrolling for the entire application.

### Overflow Hidden Fix
Hiding content to conceal broken responsive layout.

### JS Layout Engine
Measuring every element in JavaScript instead of using CSS.

### One Mobile Strategy
Converting every screen into the same card/list pattern.

### Fixed Bottom Bar Without Testing
Controls become hidden by keyboard/safe areas.

---

## 27. Verification Checklist

- [ ] breakpoints correspond to content failure
- [ ] CSS handles ordinary layout
- [ ] primary task preserved on small screens
- [ ] touch interactions work
- [ ] keyboard workflow remains correct
- [ ] navigation adapts intentionally
- [ ] tables have deliberate mobile behavior
- [ ] forms remain usable
- [ ] dialogs/sheets fit short viewports
- [ ] fixed/sticky UI doesn't obscure content
- [ ] long content/localization tested
- [ ] zoom/reflow tested
- [ ] large/ultra-wide layout tested
- [ ] reduced motion considered
- [ ] no accidental overflow hidden/content loss

## References
- `references/breakpoints.md`
- `references/responsive-tables.md`
- `references/mobile-interaction.md`
- `references/overflow-and-content.md`
