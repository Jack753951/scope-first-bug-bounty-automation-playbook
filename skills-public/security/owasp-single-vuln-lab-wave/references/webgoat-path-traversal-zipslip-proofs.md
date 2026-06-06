> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebGoat Path Traversal and Zip Slip Proof Waves

Session-derived reference for OWASP single-vulnerability local-lab waves involving path traversal file write and archive extraction traversal.

## Trigger conditions

Use this reference when the operator asks for:

- path traversal / file read / file write proof waves;
- upload filename traversal;
- Zip Slip / archive extraction path traversal;
- destructive but recoverable local靶機 testing;
- improving bundles with OSS/project source references.

## Source-first workflow

Before writing a custom runner or bundle, preserve source lineage and OSS references:

- WebGoat upstream source for the concrete lesson endpoints, e.g. `ProfileUpload.java`, `ProfileUploadBase.java`, `ProfileUploadRetrieval.java`, and lesson JS.
- PayloadsAllTheThings Directory Traversal for payload pattern vocabulary and controls.
- Snyk Zip Slip reference for archive-entry traversal concepts and impact framing.

Recommended repo locations for session-acquired refs:

- `setting/local/oss_refs/webgoat_pathtraversal_<date>/`
- `setting/local/oss_refs/path_traversal_zipslip_<date>/`

Decision rule: mature tools and public PoCs are reference/adapt material first. For local labs, use small bounded runners when they give cleaner artifacts, pre/post health, and safer marker-only impact than raw PoC execution.

## Verified lane A: upload-field path traversal file write

Pattern:

1. Register/login with a short throwaway WebGoat user.
2. Fetch the lesson HTML and JS to preserve endpoint/form provenance.
3. Create a lab marker image/file; do not use sensitive files.
4. POST to `/WebGoat/PathTraversal/profile-upload` with:
   - `uploadedFile=@marker.jpg`
   - `fullName=../<unique-marker>.jpg`
5. Save positive response, control upload response, marker file, lesson HTML/JS, JSONL observations, and summary.
6. Success criteria:
   - HTTP response is sane (typically 200).
   - response contains `lessonCompleted: true` for assignment `ProfileUpload`.
   - pre/post health remains good.

Boundary: This is a bounded local-lab file write. Do not write system files, web shells, real config, or host data. Keep report-readiness local-learning unless a separate authorized assessment gate exists.

## Verified lane B: Zip Slip profile overwrite

Pattern:

1. Register/login with a short throwaway WebGoat user.
2. Build a zip containing one marker image whose zip entry path traverses to the throwaway user's expected WebGoat profile image path.
3. POST to `/WebGoat/PathTraversal/zip-slip` with the zip as `uploadedFileZipSlip`.
4. Preserve the zip payload, marker source image, upload response, profile-picture check, lesson source, JSONL observations, and summary.
5. Success criteria:
   - response contains `lessonCompleted: true`.
   - post-health remains good.
   - impact is limited to the throwaway profile image.

Boundary: Do not overwrite system binaries, shell scripts, application code, secrets, or host files. The point is to prove archive-entry traversal and bounded overwrite, not to create persistence.

## Attempted-not-verified lane: direct random-picture retrieval

A direct WebGoat `/PathTraversal/random-picture?id=...` file-read variant may be blocked by app/Tomcat encoded traversal rejection. If raw and encoded traversal both return 400 but lesson hash submission succeeds, record the runner as `attempted-not-verified` rather than upgrading to a verified file-read bundle.

Do not claim file-read proof from lesson-completion alone. Direct read proof requires actual marker response evidence or a clean lab-owned marker read.

## Destructive-lab permission handling

When the operator explicitly allows aggressive/destructive scripts on recoverable local靶機, encode that as local-lab permission only:

Allowed inside the authorized recoverable lab:

- bounded marker overwrites;
- lab state corruption;
- service breakage with recovery;
- aggressive scanners or exploit-shaped scripts when scope-locked and recoverable.

Still disallowed:

- public/unknown targets;
- malware, stealth, persistence, evasion;
- real credential theft or exfiltration;
- uncontrolled DoS/propagation;
- automatic report submission or finding promotion.

Required closeout:

- route/tool;
- source/OSS references used;
- exact artifact path;
- pre-health and post-health;
- whether snapshot/container restore was required;
- project benefit (`對專案有什麼幫助`);
- new/changed files (`新增/更新了什麼`).

## Bundle improvement rule

Bundles may and should borrow structure from mature OSS/training-lab references, but must translate them into this project's evidence discipline:

- source references;
- when to use;
- exact runner;
- required inputs;
- success criteria;
- positive/control evidence;
- false-positive or attempted-not-verified cases;
- recovery rule;
- real-target boundary and report-readiness gate.
