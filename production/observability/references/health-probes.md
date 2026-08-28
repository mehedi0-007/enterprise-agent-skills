# Health Probes

Startup → has initialization completed?
Liveness → should process restart?
Readiness → should traffic be sent?

Keep liveness cheap and stable.
Use readiness for temporary inability to serve traffic.
Do not create dependency-induced restart storms.
