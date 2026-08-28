# Bulk Authorization

Single endpoint:
`PATCH /documents/:id`

checks ownership.

Bulk endpoint:
`PATCH /documents`

must apply equivalent authorization to every targeted document.

Do not authorize the whole batch merely because the caller can access one document or because the request was made by an administrator-like UI.
