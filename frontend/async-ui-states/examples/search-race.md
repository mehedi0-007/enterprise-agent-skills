# Search Race

`app` starts request A.
`apple` starts request B.

B returns first.
A returns later.

Correct behavior:
- show results for `apple`
- ignore/cancel stale A

Incorrect:
- A replaces current `apple` results.
