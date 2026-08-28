# Artifact Promotion

Preferred:
1. build image from commit X
2. test image
3. tag/identify by digest
4. deploy exact digest to staging
5. verify
6. deploy exact digest to production

Do not rebuild from commit X separately for production unless the process explicitly guarantees identical controlled inputs.
