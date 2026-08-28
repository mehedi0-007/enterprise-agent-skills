# Stale Update

Two clients load version 7.

Client A saves → version 8.
Client B must not silently overwrite A.

Use version/ETag conditional write:
`UPDATE ... WHERE id = ? AND version = 7`.

If zero rows are affected, return a conflict/reload outcome defined by the API.
