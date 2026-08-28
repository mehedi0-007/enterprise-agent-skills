# Edit Profile

Use explicit editable fields.

On save:
- submitting state
- server validation
- preserve input on failure
- reflect saved server state on success
- if concurrent edits matter, use version/ETag/conflict handling
- warn before navigation only when meaningful unsaved changes would be lost
