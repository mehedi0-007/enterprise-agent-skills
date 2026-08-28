# Server Error Mapping

Map stable backend error codes/details to UI behavior.

Example:
`EMAIL_ALREADY_USED` → email field error.

Do not branch on:
`message === "Email already exists"`.

Keep transport/server semantics stable enough for the UI contract.
