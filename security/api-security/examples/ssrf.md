# SSRF Example

Endpoint:
`POST /integrations/test`

Body:
`{ "url": "https://..." }`

Risk:
Attacker supplies internal destination.

Review:
- do we truly need arbitrary URLs?
- can we allow-list hosts?
- block internal/private ranges
- control redirects
- constrain response size
- set timeout
- restrict egress
- log safe destination metadata
