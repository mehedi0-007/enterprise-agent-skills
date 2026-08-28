# Artifacts and Provenance

Prefer:
source commit → reproducible build → immutable artifact → verifiable provenance → promotion.

Container deployments should use immutable digests rather than mutable tags as the release identity.

SLSA provenance describes what built an artifact, how it was built, and its inputs.
