---
name: authentication
description: Design and review secure authentication and credential lifecycles. Use for signup, login, password changes, email verification, OTP, MFA, sessions, cookies, access tokens, refresh tokens, OAuth/OIDC, account recovery, logout, and credential revocation.
---

# Authentication — Production Playbook

## 1. Mission

Authentication proves identity and maintains that identity safely over time.

A production authentication design must define:
- identity proof
- credential storage
- credential delivery
- session/token lifecycle
- revocation
- recovery
- abuse resistance
- auditing
- compromise response

Do not treat "generate a JWT" as an authentication architecture.

OWASP separates authentication, session management, and authorization as related but distinct concerns. citeturn830897search1turn830897search4

---

## 2. Activation

Use when:
- creating login/signup
- implementing email verification
- adding OTP/passwordless authentication
- adding or changing sessions/JWTs
- implementing refresh tokens
- adding MFA
- integrating OAuth/OIDC
- changing password/recovery flows
- adding logout/revocation
- responding to credential compromise

---

## 3. Identity Lifecycle

Model the account lifecycle explicitly.

Example:

```text
registered
   ↓
email_verified
   ↓
active
   ↓
suspended / locked / disabled
```

Define:
- how identity is established
- when it becomes verified
- whether unverified users can log in
- what suspension means
- what happens to active sessions after security-sensitive account changes

Do not assume "user row exists" means "user is fully authenticated/verified."

---

## 4. Choose the Authentication Model

Consider:

### Server-managed session
Good when:
- browser application
- strong server control/revocation desired
- session state is acceptable

### Short-lived access token + refresh mechanism
Useful when:
- APIs/clients need token-based delegation
- multiple resource servers/clients exist
- explicit scopes/audiences are needed

### OIDC
Use for authentication/SSO with an identity provider.

### OAuth
OAuth is an authorization framework for delegated API access; OIDC is the identity layer used for authentication. OWASP explicitly recommends OIDC for authentication/SSO and OAuth for authorization to APIs. citeturn830897search1

Do not invent a custom authentication protocol when a maintained standard/library fits.

---

## 5. Password Storage

Never store plaintext or reversible passwords.

OWASP currently recommends strong password hashing such as Argon2id, bcrypt, or PBKDF2 with a unique salt, and warns against fast hashes such as SHA-256 for password storage. citeturn830897search6

Use a maintained library and let its recommended parameters guide configuration.

Do not invent custom password hashing or encryption schemes.

---

## 6. Login Flow

A login flow should define:

```text
credential submission
      ↓
input validation
      ↓
credential lookup
      ↓
password/hash verification
      ↓
account state checks
      ↓
MFA/step-up if required
      ↓
session/token issuance
      ↓
audit/security event
```

Review:
- rate limits
- credential stuffing resistance
- timing/enumeration behavior
- suspended/disabled state
- suspicious login detection where warranted
- secure cookie/token transport

Do not reveal unnecessary distinctions such as:
- "email exists"
- "password was wrong"
- "account is suspended"
if doing so materially improves account enumeration.

---

## 7. Account Enumeration

Authentication and recovery flows can leak whether an account exists.

Review:
- login errors
- signup
- forgot-password
- resend-verification
- OTP send/verify
- username/email lookup

Use consistent user-facing behavior where enumeration risk matters.

However, do not blindly make every internal/API response identical if the product requires privileged administrative diagnostics. Define separate trusted/admin behavior when appropriate.

---

## 8. Session Management

A session should have:
- unpredictable identifier/token
- expiration
- defined idle/absolute lifetime
- revocation mechanism
- secure transport
- appropriate cookie flags if cookie-based
- association with user/device/session metadata as required

OWASP recommends that session identifiers be unique and computationally difficult to predict. citeturn830897search1

### Browser storage

OWASP currently advises not storing authentication/session/JWT/refresh credentials in `localStorage` or `sessionStorage` because JavaScript-accessible storage increases token exposure under XSS; it recommends secure HTTP-only cookie patterns or an appropriate BFF/browser architecture. citeturn830897search4

Do not blindly put JWTs in localStorage because "it's easy."

---

## 9. Cookies

For session/cookie authentication review:
- `Secure`
- `HttpOnly`
- appropriate `SameSite`
- domain/path scope
- expiration
- CSRF implications

Choose SameSite behavior based on the actual cross-site flow rather than copying a value blindly.

If cross-site cookies are required, explicitly analyze CSRF and browser behavior.

---

## 10. Access Tokens

When using access tokens define:
- lifetime
- issuer
- audience/resource server
- scopes/permissions
- signature algorithm
- key management/rotation
- revocation expectations
- transport

RFC 9700 recommends restricting access-token privileges to the minimum required and audience-restricting them to the intended resource server where feasible. citeturn830897search0

Do not put unnecessary sensitive data in tokens just because JWT payloads are convenient.

Remember:
A signed token is not automatically encrypted.

---

## 11. Refresh Tokens

Refresh tokens are high-value credentials.

Define:
- secure storage/transport
- expiration
- inactivity policy
- rotation
- reuse/replay detection
- revocation
- client binding where appropriate
- session association

RFC 9700's current OAuth 2.0 Security BCP requires sender-constrained refresh tokens or refresh-token rotation for public clients and recommends privilege/scope restrictions. citeturn830897search0

### Rotation

Concept:

```text
RT1
 ↓ refresh
RT1 invalidated
RT2 issued
 ↓
RT2 becomes current
```

If an old refresh token is replayed, the system can detect potential compromise and revoke the active grant/session according to its security policy. RFC 9700 describes this replay-detection model. citeturn830897search0

Do not implement rotation without thinking through concurrent refresh requests.

---

## 12. Refresh Race

Two browser tabs may refresh at nearly the same time.

Possible outcomes:
- one request invalidates the token needed by the other
- both attempt rotation
- legitimate client gets logged out unexpectedly
- replay detection incorrectly fires

Define concurrency behavior explicitly.

Possible controls:
- serialized refresh per session/grant
- short grace window where justified
- atomic token-family state transition
- session-level locking/compare-and-swap

Do not assume refresh requests happen one at a time.

---

## 13. Logout and Revocation

Logout semantics depend on the session architecture.

Define:
- revoke current session
- revoke all sessions
- invalidate refresh token/grant
- access-token lifetime after logout
- server-side session deletion
- cookie clearing
- device/session management

For high-risk security events, consider revoking sessions/tokens automatically.

RFC 9700 notes refresh-token revocation can be used after security events such as password changes or authorization-server logout. citeturn830897search0

---

## 14. Password Change

A successful password change is a security-sensitive event.

Review:
- require current credential or step-up authentication where appropriate
- invalidate/revoke relevant sessions according to policy
- rotate/revoke recovery artifacts
- notify user
- audit event
- rate limits

Do not assume changing a password automatically invalidates every existing session unless the system actually implements that behavior.

---

## 15. Forgot Password

The recovery flow can be as powerful as login.

OWASP recommends:
- cryptographically secure, sufficiently long tokens
- secure storage
- single use
- expiration
- no account change before a valid token is presented
- avoiding automatic login after reset citeturn830897search3

Typical flow:

```text
forgot password request
     ↓
generic response
     ↓
secure recovery token/code
     ↓
side-channel delivery
     ↓
verify token
     ↓
set new password
     ↓
invalidate token
     ↓
session policy
     ↓
audit/notification
```

Do not expose whether the target account exists.

---

## 16. Email Verification / OTP

Email verification and OTP are authentication-adjacent but have distinct threat models.

Define:
- secure generation
- short expiry
- single use
- attempt limit
- resend limit
- rate limit
- replay handling
- safe persistence
- enumeration behavior
- delivery abuse monitoring

OWASP's current email verification guidance warns against treating email as a strong authentication factor and recommends monitoring verification/reset activity without logging tokens or full sensitive URLs. citeturn830897search5

Do not log OTP values or verification/reset tokens.

---

## 17. MFA

MFA should be modeled as a separate factor lifecycle.

For sensitive actions, consider step-up authentication even when the user already has a valid session.

Define:
- enrolled factors
- factor verification
- backup/recovery
- factor reset
- session trust
- risk-sensitive operations

OWASP's MFA guidance covers multiple factor types and recovery considerations. citeturn830897search8

Do not design MFA recovery as an easy bypass around MFA.

---

## 18. OAuth / OIDC

When integrating an IdP:

For OIDC, validate at minimum:
- issuer
- audience
- signature
- expiration
- required claims

OWASP explicitly recommends validating ID tokens using provider keys/discovery and verifying issuer, audience, signature, and expiration. citeturn830897search1

Use maintained standards-based libraries.

Do not:
- trust decoded JWT payloads without verification
- accept arbitrary issuers/audiences
- manually implement cryptographic token validation unnecessarily

For OAuth 2.0 security, follow current RFC 9700 guidance rather than older assumptions. citeturn830897search0

---

## 19. Token Audience and Scope

A token issued for one resource should not automatically be valid for every API.

Define:
- audience
- scope
- client
- user
- resource server

RFC 9700 recommends audience restriction and minimum necessary privilege. citeturn830897search0

If the backend accepts a token intended for another audience, privilege boundaries can collapse.

---

## 20. Cryptographic Keys

Define:
- key storage
- signing algorithms
- rotation
- active/previous keys
- key identifiers (`kid`) when applicable
- overlap during rotation
- revocation
- emergency rollover

Never hardcode private signing keys in source.

Do not invent cryptographic primitives.

---

## 21. Rate Limiting and Abuse

Authentication endpoints are high-value abuse targets.

Review limits for:
- login
- signup
- password reset requests
- OTP send
- OTP verification
- MFA verification
- token refresh
- email verification

Consider limits by:
- account/identifier
- IP/network
- device/session
- global service capacity

Do not rely on only one dimension if attackers can rotate identities or IPs.

---

## 22. Security Events and Audit

Record important events as structured security events:
- login success/failure
- password change
- password reset
- MFA enrollment/removal
- session creation/revocation
- suspicious token reuse
- account lock/suspension
- email/phone change

Do not log credentials/tokens.

Where privacy matters, avoid unnecessary full identifiers; OWASP specifically advises against logging full email addresses in sensitive verification flows. citeturn830897search5

---

## 23. Account Lockout

Do not automatically implement permanent account lockout after a small number of failures; attackers can weaponize lockout to deny service.

Prefer risk-based/bounded defenses such as:
- rate limits
- progressive delays
- temporary throttling
- anomaly detection
- step-up challenges

Define recovery behavior if temporary blocking exists.

---

## 24. Sensitive Changes / Step-Up

Require stronger re-authentication or step-up for high-risk operations when appropriate:
- password change
- MFA change
- recovery-method change
- payout/bank changes
- API key creation
- organization ownership transfer

A valid long-lived session should not automatically be considered sufficient assurance for every security-sensitive action.

---

## 25. Authentication State in APIs

Avoid ambiguous states such as:
```text
token present → user trusted
```

Authentication middleware should establish a verified principal/context.

Application authorization still decides access.

The authenticated context should not be built from arbitrary client-provided IDs.

---

## 26. Testing Strategy

Test:
- valid/invalid credentials
- expired/revoked sessions
- password hashing/verification
- enumeration behavior
- brute-force/rate limits
- OTP expiry/single-use/replay
- refresh rotation
- concurrent refresh
- token audience/scope
- logout/revocation
- password-reset token reuse
- MFA recovery
- OAuth/OIDC token validation
- session invalidation after sensitive changes

Use integration tests for session/token persistence and concurrency behavior.

---

## 27. Threat Scenarios

At minimum consider:

```text
stolen password
stolen access token
stolen refresh token
replayed OTP
brute-force login
credential stuffing
account enumeration
session fixation/hijacking
stale session after password change
concurrent refresh
malicious recovery attempt
compromised IdP token
wrong token audience
```

For each:
- detection
- prevention
- containment
- recovery

---

## 28. Review Decision Tree

```text
How does the user authenticate?
       ↓
Password / session / token / IdP / MFA
       ↓
Where is the credential stored?
       ↓
How is it transported?
       ↓
How is it validated?
       ↓
How long is it valid?
       ↓
How is it revoked?
       ↓
Can it be replayed?
       ↓
Can it be brute-forced?
       ↓
Can users be enumerated?
       ↓
What happens after password/security changes?
       ↓
What happens on concurrent refresh/retry?
       ↓
How is compromise detected/contained?
```

---

## 29. Anti-Patterns

### Plaintext Passwords
Never.

### Fast Password Hash
SHA-256/MD5-style password hashing is not appropriate for password storage. citeturn830897search6

### JWT Everywhere
Using JWTs because they are available without defining session/revocation requirements.

### JWT in Local Storage
Blind browser-storage choice despite XSS/token exposure risk. citeturn830897search4

### Infinite Refresh Tokens
No expiration, rotation, revocation, or replay strategy.

### Decode Means Validate
Reading JWT claims without verifying signature/issuer/audience/expiry.

### Recovery as Backdoor
Weak password/MFA recovery that bypasses the security model.

### OTP as Password
Treating email OTP as equivalent to strong MFA without analyzing email-factor risk.

### Permanent Lockout
Easy account denial-of-service.

### Log Credentials
Passwords, OTPs, tokens, reset URLs, or signing material in logs.

### Custom Crypto
Inventing cryptographic algorithms or token formats without necessity.

---

## 30. Verification Checklist

- [ ] identity lifecycle defined
- [ ] authentication method justified
- [ ] credential storage secure
- [ ] password hashing appropriate
- [ ] session/token lifetime defined
- [ ] revocation defined
- [ ] browser credential storage reviewed
- [ ] access-token audience/scope defined
- [ ] refresh-token rotation/replay strategy defined
- [ ] concurrent refresh behavior safe
- [ ] logout behavior defined
- [ ] password/recovery security events defined
- [ ] OTP/MFA replay/rate limits defined
- [ ] enumeration risk reviewed
- [ ] brute-force/credential-stuffing controls exist
- [ ] OAuth/OIDC tokens fully validated when used
- [ ] keys/secrets have lifecycle
- [ ] sensitive changes use appropriate step-up
- [ ] audit/security events exist without secret leakage
- [ ] integration/security tests exist

## Review Procedure

1. Identify the authentication model and trust boundary.
2. Review credential/session/token lifecycle.
3. Review storage, transport, expiry, revocation, and rotation.
4. Review recovery, OTP/MFA, enumeration, and brute-force resistance.
5. Review concurrent refresh/retry behavior.
6. Verify audit and compromise-response behavior.

## Verification Checklist

- [ ] identity lifecycle defined
- [ ] credential storage secure
- [ ] session/token lifetime defined
- [ ] revocation/rotation defined
- [ ] recovery flows reviewed
- [ ] enumeration/abuse controls reviewed
- [ ] concurrent refresh/retry tested
