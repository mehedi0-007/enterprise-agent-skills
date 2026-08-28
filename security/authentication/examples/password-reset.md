# Password Reset Example

Request:
`POST /forgot-password`

Response should not reveal whether the account exists.

If an account exists:
- create secure single-use token
- expire it
- send through approved side channel
- do not log token

Reset:
- verify token
- set new password securely
- invalidate token
- apply session revocation policy
- audit and notify
