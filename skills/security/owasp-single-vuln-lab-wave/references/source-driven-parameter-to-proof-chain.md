> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Source-driven parameter discovery to one-vulnerability proof chain

Use this when a vulnerability-source/library lane points to a tool or PoC family, but the current lab should remain isolated, bounded, and candidate-only.

## Pattern

1. Preserve source lineage first.
   - Record whether the idea came from CISA KEV/NVD/Exploit-DB/GitHub tooling/HTB/OWASP/CWE.
   - Treat product-specific CVEs and raw PoCs as pattern inspiration unless the lab actually has the affected component/version.

2. Try the mature tool safely, but do not let setup state block the lane.
   - Prefer running tool help/version from the attacker VM, not the Windows control plane.
   - If a source checkout is present but not installed globally, try invoking it from its repo with the right package/module path.
   - If dependency installation would require opening NAT/network, either schedule a deliberate temporary-NAT install window or port the safe core idea into a bounded local runner.
   - Record the missing setup as setup debt, not as a durable claim that the tool is unusable.

3. Port the safe core idea when useful.
   - Example: Arjun-style parameter discovery can be approximated with a curated parameter list, low-rate GET probes, response status/length/hash comparison, and post-health checks.
   - Keep the wordlist small and purpose-bound for the first wave.
   - Store inputs, script, results JSON, summary, and post-health under `<artifact-output-dir>/<wave>/`.

4. Continue from candidate surface to one-vulnerability proof.
   - Pick one discovered parameter or behavior.
   - Test a single vulnerability hypothesis with minimal payloads.
   - Compare baseline / normal / positive / negative controls; rely on differential behavior and stable controls rather than noisy keyword matches alone.
   - Keep output as candidate/verified-lab-flow language depending on evidence; do not auto-promote to report-ready.

5. Promote the proof into a reusable bundle/module immediately after the focused proof stabilizes.
   - Add a focused RED/GREEN test for the bounded adapter, including plan-only output, `--lab-approved` runner generation, public-target rejection, candidate-only classification, and false-positive/noisy-keyword controls.
   - Put the reusable generator under `scripts/lab_modules/`, the operator-facing bundle under `modules/bundles/`, and the generated local runner under `setting/local/`.
   - Update `scripts/SCRIPT_INVENTORY.md`, append `handoff/accepted_changes.md`, and, when the operator asks for coverage visibility, generate a dated `handoff/bundle_inventory_<date>.md` from `modules/bundles/*.md`.
   - On Windows/Git-Bash, validate generated bash by piping script text to `bash -n` or running `bash -n <msys-path>` after path conversion. Avoid passing raw native `C:\...` paths to bash syntax checks.

## Session-derived example

A GitHub/Arjun recommendation from `script_acquisition_wave2` led to bounded local-lab parameter discovery against Juice Shop. Raw Arjun source invocation failed due setup/dependency state in the isolated lab, so the safe idea was ported into a stdlib probe:

- targets: Juice Shop `/rest/products/search`, `/rest/user/login`, `/api/Products`;
- params: a 20-item curated list (`q`, `id`, `sort`, `name`, etc.);
- result: `q` on `/rest/products/search` and several `/api/Products` params produced response-length/status deltas.

The next wave selected only `q` and ran a bounded SQLi behavior check with baseline, normal, single-quote, boolean-true, and boolean-false probes. The stronger signal was true/false response-size differential, not generic `SELECT`/`WHERE` keyword presence, which can be product-content noise.

## Pitfalls

- Do not raw-execute downloaded exploit scripts just because the source lane is Exploit-DB/GitHub.
- Do not stop at dependency failure if the useful idea can be safely reimplemented as a bounded local probe.
- Do not call HTTP 500 or response-size changes a vulnerability by themselves; require controls and, when possible, a single-vulnerability proof wave.
- Do not treat generic SQL/error keywords in response text as proof without checking whether the application content itself may contain those words.
- Do not forget post-health; parameter/fuzz-style probes should leave the target healthy.

- Do not leave a successful proof as a temporary script only; convert it into a tested `scripts/lab_modules/` adapter plus `modules/bundles/` document while the proof details are fresh.
- Do not let Windows path syntax create false test failures for generated Linux/bash runners. Validate script content through stdin (`bash -n` with input) or convert paths explicitly before invoking bash.
- Do not let a bundle directory grow opaque; periodically inventory bundle docs by maturity/capability so the next wave can target real gaps instead of duplicating coverage.

## Minimum artifact set

- source lineage and rationale in handoff;
- bounded target list and parameter/payload list;
- runner/probe script copied into artifact dir;
- `results.json` with status/length/hash/control fields;
- `summary.txt` with candidate/control classification;
- `post_health.txt`;
- accepted-changes and active-queue updates when the lane changes direction.
