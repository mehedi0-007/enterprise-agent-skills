# Runner Trust

Hosted runners provide stronger ephemeral isolation than persistent self-hosted runners in many setups.

If untrusted code executes on a self-hosted runner, assume it may access anything the runner can reach or anything left behind by previous jobs.

Scope network/credentials and clean state aggressively.
