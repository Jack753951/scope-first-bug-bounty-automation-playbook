> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Path traversal file-read local target expansion

Session-derived reference for continuing a file-read/path traversal lane when a training target rejects traversal before marker content can be read.

## Trigger conditions

Use when:

- a file-read/path traversal lane is useful, but the current lab target only produces rejection/control evidence;
- a previous direct-read attempt is `attempted-not-verified` because no lab-owned marker content was returned;
- the operator wants capability growth without reading sensitive files such as `/etc/passwd`, secrets, tokens, SSH keys, or real user data.

## Pattern

1. Preserve the rejected attempt honestly as `attempted-not-verified`.
   - Keep status codes, request paths, app/Tomcat/router rejection evidence, pre/post health, and why no marker read is claimed.
2. Switch to an equivalent recoverable local target instead of forcing a bad surface.
   - Prefer a source-controlled disposable target when it can express the vulnerability behavior cleanly.
   - Record this as `write-custom` local target expansion after OSS/source reconnaissance.
3. Create lab-owned fixtures at target startup:
   - a public control file inside an intended public/readable directory;
   - a marker file just outside that directory but still under lab-owned temp/workspace storage.
4. Add one intentionally vulnerable read route for the local lab, e.g. `GET /file-read?name=` that naively joins `PUBLIC_DIR / name`.
5. Run a bounded proof from the attacker VM to the victim/container target.
   - Pre-health 200.
   - Public-file control returns the public marker.
   - Missing-file negative control returns 404 or equivalent.
   - Positive traversal uses `../<lab-marker>` and returns only the lab marker content.
   - Post-health 200.
   - Cleanup removes the disposable target.
   - Attacker/victim Internet remains closed for host-only execution.
6. Pull artifacts back and run a read-only evidence review before bundle/promotion.

## Evidence shape

Minimum artifacts:

- preview/handoff explaining why local target expansion is chosen;
- runner script;
- target source diff or route description;
- `summary.md` with statuses and verdict;
- `run.log`;
- `http/public_control.json`;
- `http/missing_control.json`;
- `http/traversal_positive.json`;
- `http/pre_health.json` and `http/post_health.json`;
- cleanup evidence from attacker and victim;
- read-only review that challenges overclaim risk.

A verified positive should include marker content similar to:

```json
{
  "name": "../hermes_modern_api_file_read_marker.txt",
  "resolved": "/tmp/hermes_modern_api_public_files/../hermes_modern_api_file_read_marker.txt",
  "content": "FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB\n"
}
```

## Classification

Use a narrow classification such as:

```text
verified_file_read_safe_marker_lab_only
```

Do not upgrade to production finding or arbitrary sensitive file read.

## Boundary

Allowed:

- lab-owned marker file read;
- public-file and missing-file controls;
- one bounded traversal request against a disposable local target;
- source-level explanation of the vulnerable join.

Not allowed / not claimed:

- reading `/etc/passwd`, cloud metadata, tokens, config secrets, SSH keys, or real user data;
- public/third-party targets;
- shell execution, persistence, webshell writes, credential theft, or exfiltration;
- automatic report submission or confirmed real-target finding promotion.

## Pitfalls

- Do not treat training-lab lesson completion, status-code deltas, or rejected traversal payloads as file-read proof. Require actual marker content read.
- Do not keep hammering an unsuitable endpoint after useful rejection evidence is captured. Switch to source-level review, an equivalent disposable local target, or a nearby safe-marker lane.
- A `resolved` path string is useful but not canonical proof by itself; marker content plus controls carry the claim. For packet-grade evidence, optionally add raw headers, `curl -v`, canonical `realpath`, and container inspect/log metadata.
