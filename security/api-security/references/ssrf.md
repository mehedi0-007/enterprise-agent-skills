# SSRF Review

If the server fetches a user-influenced URL:

1. Is arbitrary destination truly required?
2. Can destinations be allow-listed?
3. Are schemes restricted?
4. Are private/link-local/loopback destinations blocked?
5. Are redirects controlled?
6. Are DNS/address resolution changes handled?
7. Is outbound network access restricted?
8. Are timeouts and response-size limits enforced?
9. Are failures non-sensitive?

String prefix checks are not a sufficient SSRF defense.
