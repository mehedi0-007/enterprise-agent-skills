# Sources and Provenance

This repository synthesizes engineering guidance for AI agents. It does not copy upstream `SKILL.md` files.

## Agent Skills Standard
- Agent Skills specification and documentation: https://github.com/agentskills/agentskills
- Progressive-disclosure model: discovery metadata → activated instructions → optional references/resources.

## Backend / API
- IETF RFC 9110 — HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110.html
- wshobson/agents — https://github.com/wshobson/agents
- Selected production-oriented backend agent skills from open-source repositories were used as comparison/reference material.

## PostgreSQL / Database
- PostgreSQL documentation: https://www.postgresql.org/docs/current/
- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- PostgreSQL indexes: https://www.postgresql.org/docs/current/indexes.html
- PostgreSQL transaction isolation: https://www.postgresql.org/docs/current/transaction-iso.html
- Neon postgres-skills: https://github.com/neondatabase/postgres-skills

## Security
- OWASP API Security Top 10: https://owasp.org/API-Security/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

## Frontend / UX / Accessibility
- Vercel Web Interface Guidelines: https://github.com/vercel-labs/web-interface-guidelines
- MDN Web Docs: https://developer.mozilla.org/
- W3C Web Accessibility Initiative / WCAG: https://www.w3.org/WAI/standards-guidelines/wcag/
- Material Design: https://m3.material.io/

## Production / Operations
- Docker Build documentation: https://docs.docker.com/build/
- GitHub Actions documentation: https://docs.github.com/actions
- GitHub Actions security hardening: https://docs.github.com/actions/security-for-github-actions/security-hardening-for-github-actions
- OpenTelemetry: https://opentelemetry.io/docs/
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

## Maintenance Rule
Primary documentation should win when upstream guidance conflicts with a community skill. Re-check fast-changing platform guidance periodically.
