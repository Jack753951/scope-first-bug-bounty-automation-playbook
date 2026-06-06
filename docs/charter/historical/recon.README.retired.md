> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# recon/

Reserved for future recon-stage modules or structured recon artifacts.

Current recon behavior still lives primarily in `recon.sh`. Future work should gradually move reusable stage logic into policy-gated modules or helpers rather than growing `recon.sh` further.

Expected future candidates:

- subdomain enumeration stage wrappers
- HTTP probe stage wrappers
- TLS metadata collection
- technology fingerprint normalization

All future recon stages must respect global scope, program scope, technique gates, rate limits, testing windows, and audit logging.
