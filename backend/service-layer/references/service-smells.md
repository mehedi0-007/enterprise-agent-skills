# Service Smells

## Too many responsibilities
Different business capabilities mixed together.

## Too many dependencies
May indicate poor boundaries or an aggregate/facade with excessive scope.

## Pass-through methods
If the service only forwards every repository method, it may add no meaningful application boundary.

## Conditional explosion
Many branches based on unrelated product areas can signal missing domain policies/use cases.

## Hidden side effects
A method named `updateUser` unexpectedly sends emails, charges cards, or publishes events without making the behavior visible.

## Fix
Refactor around cohesive use cases and preserve behavior with tests. Do not split merely to make classes smaller.
