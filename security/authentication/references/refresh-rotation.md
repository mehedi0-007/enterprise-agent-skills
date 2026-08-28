# Refresh Token Rotation

For public clients, RFC 9700 requires sender-constrained refresh tokens or refresh-token rotation.

Rotation:
1. receive current refresh token
2. atomically verify it is current
3. invalidate/advance token family state
4. issue new refresh token
5. retain enough relationship state to detect replay

Review concurrent refresh carefully. Two legitimate requests can overlap.
