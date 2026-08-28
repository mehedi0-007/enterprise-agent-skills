# Deployment Strategy Selection

Rolling:
simple default for compatible services.

Canary:
use when staged exposure gives valuable production signal.

Blue/green:
use when traffic cutover matters and duplicate capacity is acceptable.

Feature flag:
use when deployment and exposure should be decoupled.

The strategy does not remove the need for schema/data compatibility.
