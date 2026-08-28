# Frontend Secret Review

A developer wants to put a third-party secret into a React/Next.js client bundle.

Reject the design if the provider credential must remain secret.

Anything delivered to the browser can be inspected by the user. Put the privileged call behind a backend and apply server-side authorization/rate limits.
