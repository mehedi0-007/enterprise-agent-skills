# SaaS Feature Review Example

Feature:
Organization admin can export customer data.

Review:
1. asset = sensitive customer data
2. principal = organization admin
3. object/tenant scope = current organization
4. function permission = data.export
5. resource consumption = potentially huge export
6. business risk = bulk exfiltration
7. async operation likely
8. audit event required
9. file storage/download authorization required
10. security test = admin A cannot export tenant B

Route details to:
- authorization
- api-security
- production/observability
