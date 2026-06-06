> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code review — deserialization preview process test

Reviewer route/tool: Claude Code (read-only review, no tools invoked per instructions)

Visible model/runtime: claude-opus-4-7 / Claude Code CLI

Review focus: Whether the dedicated `modern_vuln_api` unsafe-deserialization bounded-marker rerun produced standalone evidence in this wave, and how to classify the resulting artifacts.

Evidence inspected (by reference only — no file reads performed this turn):
- `handoff/modern_api_deserialization_preview_20260523.md` (preview/intent)
- `handoff/modern_api_deserialization_preview_test_blocked_20260523.md` (execution blocker record)
- `setting/local/oss_refs/deserialization_preview_test_20260523/README.md` (source/recon)
- Source claim: `labs/modern_vuln_api/modern_vuln_api.py` — `POST /deserialize` → `pickle.loads(base64.b64decode(...))` with `record_deser_marker` sink
- Negative space: no new `/deser-log` capture, no pre/post health pair, no control-payload rejection record from this wave

Claim supported? partial
- Supported: the sink exists in source, preview was well-scoped, and the workflow itself (recon → preview → execution attempt → blocker pullback → review) executed end-to-end as a process test.
- Not supported: the runtime proof — health, control, positive marker, `/deser-log`, post-health — was not produced this wave. The vuln claim for this dedicated rerun is source-level only.

Recommended status: blocked/deferred
- The process-workflow test is itself `verified-impact` (the pipeline ran and the blocker was honored without retry/disguise), but the deserialization *vulnerability* rerun is blocked/deferred. Do not promote to `valuable-candidate` on the strength of the prior historical bundle — that bundle belongs to a different wave and conflating them defeats the point of the dedicated rerun.

Missing evidence:
- Attacker-side curl transcript for the five-step sequence (health / invalid / positive marker / `/deser-log` / post-health)
- Victim-side `DESER_EVENTS` snapshot showing exactly one new `{"type":"bounded_pickle_gadget","marker":...}` entry tied to this wave's marker
- Pre/post health 200s framing the run
- Timestamped marker string unique to 20260523 so the artifact cannot be confused with prior runs

False-positive controls:
- Control payload (malformed/invalid base64 or non-pickle bytes) must be rejected and must NOT append to `DESER_EVENTS`
- Marker string must be wave-unique (e.g., include `20260523` + a nonce) so a stale entry from a prior wave cannot be misread as this wave's success
- `/deser-log` diff: capture length/contents before and after; only the positive payload should increment

Tactical next step:
- Treat the current artifacts as a clean `attempted-not-verified` package for the deserialization lane and a `verified-impact` package for the *process test itself* — file them separately so the two claims don't contaminate each other.
- If/when the execution-layer block is resolved by the operator out-of-band, re-run the exact preview unchanged (same five steps, same wave-unique marker) — don't redesign the proof to route around the block.
- In the meantime, keep deserialization split into its dedicated wave as planned; don't fold it back into the broader modern-API bundle.

Hermes final decision recommendation:
- Mark the deserialization rerun **blocked/deferred** in the active strategy queue; do not claim verified vuln impact for this wave.
- Mark the preview→block→review→synthesis loop **verified** as a workflow test — that is the legitimate win here.
- Do not retry, re-encode, or split the blocked trigger. Do not borrow the prior historical bundle to upgrade this wave's status.
- Next Hermes synthesis should explicitly distinguish "process test passed" from "vuln rerun deferred" so downstream readers don't conflate them.

## Run metadata

```json
{
  "subtype": "success",
  "duration_ms": 25189,
  "num_turns": 1,
  "total_cost_usd": 0.10836974999999999,
  "session_id": "deafa881-d82a-4873-b830-a36b70032d55"
}
```
