---
name: navigation
description: Design and review web application information architecture, navigation hierarchy, routes, tabs, sidebars, breadcrumbs, deep links, browser history, unsaved changes, mobile navigation, and permission-aware destinations. Use when adding pages/sections, changing route structure, or designing how users move through a product.
---

# Navigation — Production Playbook

## 1. Mission

Navigation helps users answer:

- Where am I?
- What belongs here?
- Where can I go?
- How do I get back?
- What is the current context?
- What happens if I leave?

Good navigation reflects the user's mental model and task structure—not the backend module tree.

---

## 2. Activation

Use when:
- adding a page/route
- adding a product section
- creating nested resources
- deciding between sidebar/tabs/breadcrumbs
- changing URL structure
- adding mobile navigation
- handling unsaved changes
- adding search/command navigation
- changing permission-aware destinations
- reviewing browser back/forward behavior

---

## 3. Start With Information Architecture

Before choosing a navigation component, identify:

- top-level product areas
- related concepts
- common tasks
- hierarchy depth
- frequency of access
- user roles/personas
- current resource context
- expected URL/deep-link behavior

Do not mirror internal code modules simply because they exist.

Example:

Bad IA:
```text
Database
Services
Repositories
Controllers
```

Good product IA:
```text
Customers
Orders
Billing
Reports
Settings
```

Users think in product concepts.

---

## 4. Navigation Pattern Selection

### Primary Navigation
Use for top-level destinations that users regularly switch between.

### Sidebar
Good for:
- SaaS/admin products
- multiple persistent sections
- hierarchical navigation

### Tabs
Good for:
- closely related peer views
- same resource/context
- switching among a small set of views

Example:
```text
Project
[Overview] [Members] [Activity] [Settings]
```

Do not use tabs as a substitute for unrelated navigation.

### Breadcrumbs
Useful when:
- hierarchy is deep
- users need orientation
- navigating back up the hierarchy is valuable

Do not add breadcrumbs to shallow structures just because a design system offers them.

### Contextual Menu
Use for local actions, not destination navigation unless the menu deliberately represents navigation.

### Command/Search Navigation
Useful when:
- many destinations exist
- power users need fast access
- navigation hierarchy is deep

Do not make command search the only discoverable navigation mechanism.

---

## 5. Navigation Hierarchy

Keep hierarchy understandable.

Prefer:

```text
Workspace
  Projects
    Project A
      Overview
      Members
      Activity
```

rather than:

```text
Workspace → Settings → Advanced → Management → Project
```

Deep nesting increases orientation cost.

If hierarchy is genuinely deep, use contextual navigation and breadcrumbs.

---

## 6. URL Design

Important application states should have stable, meaningful URLs when practical.

A URL may represent:
- resource identity
- sub-resource
- view/tab
- search/query state
- filters
- pagination/cursor where useful

Examples:

```text
/workspaces/acme/projects/123
/workspaces/acme/projects/123/members
/workspaces/acme/invoices?status=overdue
```

Avoid URLs that expose framework implementation details unnecessarily.

Do not put secrets or sensitive credentials in URLs.

---

## 7. Deep Linking

A user should be able to:
- bookmark important views
- refresh and remain in context
- open a copied URL and reach the same logical destination

For deep-linked state, define what must be encoded:
- filters
- selected tab
- search
- resource ID
- sort order

Do not put ephemeral UI state into URLs merely because technically possible.

---

## 8. URL vs Local State

Use URL state when the state:
- changes what data/content is shown
- should survive refresh
- should be shareable/bookmarkable
- is useful in browser history

Use local component state when the state:
- is ephemeral
- does not represent a meaningful destination
- should not create history entries

Example:
```text
search query → URL
modal open state → usually local state
```

This is a heuristic, not an absolute rule.

---

## 9. Browser History

Respect browser navigation.

Ask:
- should this interaction create a history entry?
- should Back return to previous filter/search state?
- does changing a tab represent meaningful navigation?
- does opening a modal change URL/context or remain local?

Do not hijack `Back` to perform unrelated product logic.

For SPA navigation, preserve expected browser semantics.

---

## 10. Tabs and History

Tabs can be:
- separate routes
- query/fragment state
- local state

Prefer route/query representations when users reasonably expect:
- refresh persistence
- deep links
- browser Back/Forward
- shareable views

Do not create URL history entries for every tiny visual toggle unless it is meaningful navigation.

---

## 11. Navigation and Permissions

A navigation item can be:
- visible and usable
- visible but unavailable
- hidden

Choose deliberately.

### Hide when:
- feature is irrelevant to the user
- revealing it adds confusion/no value

### Show but disable/explain when:
- feature is relevant
- user benefits from knowing it exists
- access can be requested/upgraded

Never rely on hidden navigation for authorization.

The backend must still enforce access.

---

## 12. Permission Changes

Permissions can change while a user is active.

Examples:
- membership revoked
- admin role removed
- workspace access removed

When access changes:
- navigation should update
- current route should handle authorization failure
- cached permission state should not remain indefinitely
- sensitive data should not remain accessible through already-open UI

Coordinate with `security/authorization`.

---

## 13. Unauthorized vs Not Found

If a user follows a URL they cannot access:
- show the appropriate access state
- do not leak resource existence if the security model intentionally hides it
- provide a useful way forward

The UI should not assume every missing route means "404" independently of backend semantics.

---

## 14. Nested Resources

Use nested routes when the parent context is meaningful.

Good:
```text
/projects/:projectId/members
```

Potentially bad:
```text
/organizations/:orgId/users/:userId/projects/:projectId/settings/history/events/...
```

Deep nesting can make:
- URLs unreadable
- authorization difficult
- navigation burdensome

Use flatter routes when the child has an independent global identity, while still showing context in the UI.

---

## 15. Sidebar Behavior

A sidebar should make:
- current section obvious
- top-level destinations accessible
- nested sections understandable

For collapsible sidebars:
- preserve current-location indication
- avoid hiding the only navigation cue
- define keyboard behavior
- ensure collapsed icon-only state remains accessible

Do not make icons carry all navigation meaning without accessible labels/tooltips.

---

## 16. Mobile Navigation

On mobile:
- keep primary destinations accessible
- move secondary destinations into an appropriate drawer/menu
- preserve current location
- provide an obvious close/back behavior
- manage focus correctly

Do not simply hide the desktop sidebar without providing equivalent access.

Use `frontend/responsive-design` for layout behavior and `frontend/accessibility` for interaction/focus behavior.

---

## 17. Navigation Labels

Use labels users understand.

Prefer:
```text
Customers
Billing
Reports
Settings
```

over:
```text
CRM
Finance Ops
Analytics Hub
Configuration
```

unless those are established product terms.

Be consistent with terminology across:
- navigation
- page titles
- buttons
- help text
- URLs where practical

Do not create synonyms for the same concept.

---

## 18. Icons

Icons can support navigation labels.

For icon-only collapsed navigation:
- maintain an accessible name
- provide recognizable visual semantics
- avoid relying on hover alone for understanding

Do not assume a symbol has universal meaning.

---

## 19. Active State

The current destination should be obvious.

Consider:
- current route
- nested current section
- selected tab
- expanded parent

Do not mark a broad navigation item active for unrelated descendant routes unless that hierarchy is intentional.

Avoid color-only active indicators.

---

## 20. Breadcrumbs

Use breadcrumbs when they provide orientation in a hierarchy.

Good:
```text
Projects / Apollo / Settings
```

Bad:
```text
Home / Dashboard / Settings
```

when the hierarchy is shallow and the breadcrumb adds no useful information.

Breadcrumbs should reflect meaningful hierarchy, not every UI transition.

---

## 21. Back Buttons

A custom Back button should have deliberate semantics.

Ask:
- does it go to browser history?
- parent resource?
- fixed product destination?

Do not label an action "Back" when it unexpectedly sends users to a hardcoded page.

If the product requires a context-specific return destination, make that behavior clear.

---

## 22. Unsaved Changes

Warn before navigation when leaving would cause meaningful user work to be lost.

Do not warn for:
- trivial view state
- already-saved data
- every navigation just because a form was focused

For forms, coordinate with `frontend/forms`.

Define:
- dirty state
- save state
- navigation behavior
- recovery

---

## 23. Navigation During Async Work

If the user navigates while an action is processing:
- determine whether work is durable
- preserve status if necessary
- avoid duplicate requests when returning
- make completion discoverable

Long-running tasks should generally be represented as durable jobs rather than tied to one page's lifetime.

Use `frontend/async-ui-states`.

---

## 24. Search / Command Navigation

For large applications, command search can supplement navigation.

Good command destinations/actions are:
- predictable
- labeled clearly
- permission-aware
- fast
- keyboard accessible

Do not expose actions the user is not authorized to perform simply because they are hidden from normal navigation.

---

## 25. Route Changes and Focus

In an SPA, route changes may not reload the document.

After significant navigation:
- update page title
- establish appropriate heading/context
- manage focus deliberately
- expose new route context to assistive technology

Do not focus arbitrary elements merely to announce every navigation.

Use `frontend/accessibility`.

---

## 26. Navigation Errors

Handle:
- unavailable route
- unauthorized route
- deleted resource
- stale deep link
- network/load failure

Give the user a useful next action:
- return to parent
- go to home
- retry
- request access
- choose another resource

Do not trap users on a dead-end error page.

---

## 27. Navigation and Caching

Be careful when menu visibility depends on cached permissions or stale account state.

A route may still be accessible through:
- direct URL
- old browser tab
- bookmark
- API call

Navigation is not an authorization boundary.

---

## 28. Navigation Testing

Test:
- direct deep links
- refresh
- browser Back/Forward
- tabs
- nested routes
- mobile navigation
- collapsed sidebar
- keyboard access
- unauthorized routes
- revoked access during session
- unsaved form navigation
- deleted resource URLs
- stale/deprecated URLs

---

## 29. Review Procedure

For each new route/feature ask:

1. What user concept does this represent?
2. Is it a top-level destination, sub-resource, or local action?
3. Which navigation pattern fits?
4. Should it have a stable URL?
5. Should state live in URL or local state?
6. What should browser Back do?
7. What happens on refresh/deep link?
8. What happens if the user lacks permission?
9. What happens if permission changes?
10. How does it work on mobile?
11. Does focus/context move correctly?
12. What happens with unsaved work?
13. Is terminology consistent?

---

## 30. Anti-Patterns

### Backend-Shaped Navigation
Users see implementation/module names.

### Everything as Tabs
Tabs become a second sidebar.

### Everything as Modal
Destinations are not bookmarkable/revisitable.

### Hardcoded Back
Back sends users somewhere surprising.

### URL Everything
Ephemeral state pollutes history/links.

### Local State Everything
Important views cannot be refreshed/shared.

### Hidden Authorization
UI hiding treated as security.

### Mobile Sidebar Removed
Desktop nav disappears with no equivalent.

### Active State Guessing
Broad parent remains active for unrelated routes.

### Deep URL Nesting
Routes become impossible to understand/authorize.

### Unsaved Warning Everywhere
Confirmation fatigue.

### Search Bypass
Command menu exposes unauthorized actions.

---

## 31. Verification Checklist

- [ ] information architecture follows user concepts
- [ ] navigation pattern matches task
- [ ] URL semantics deliberate
- [ ] important views deep-linkable
- [ ] URL vs local state decision justified
- [ ] browser history behaves predictably
- [ ] tabs represent related views
- [ ] active state clear
- [ ] permissions reflected in UX
- [ ] authorization remains server-side
- [ ] mobile navigation works
- [ ] focus/context handled
- [ ] unsaved-work behavior defined
- [ ] async navigation behavior defined
- [ ] error/dead-end routes recoverable
- [ ] terminology consistent
- [ ] direct links/refresh/back tested

## References
- `references/pattern-selection.md`
- `references/url-and-history.md`
- `references/permissions.md`
- `references/mobile-navigation.md`
- `references/unsaved-changes.md`

## Cross-Skill Routing
For keyboard/focus semantics, coordinate with `accessibility`.
For mobile layout/adaptation, coordinate with `responsive-design`.
For actual access control, coordinate with `authorization`.
