# Session Model Choices

## Server Session
Server stores session state; browser holds an opaque session identifier.
Strength: simple revocation and server control.
Tradeoff: session-store dependency.

## Access + Refresh Tokens
Useful for API/client ecosystems.
Requires explicit token lifecycle, audience/scope, refresh rotation/reuse handling, revocation policy, and secure client storage.

## Browser BFF
Browser talks to a backend-for-frontend; BFF manages tokens server-side.
Can reduce browser token exposure.

Choose from application architecture, not fashion.
