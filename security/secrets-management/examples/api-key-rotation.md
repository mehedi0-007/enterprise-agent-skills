# API Key Rotation

A production provider key is being rotated.

Unsafe:
1. revoke old key
2. deploy new key

This can cause downtime if old instances remain.

Safer:
1. create new key
2. provision new key
3. deploy consumers
4. verify traffic uses new
5. revoke old key
6. monitor errors
