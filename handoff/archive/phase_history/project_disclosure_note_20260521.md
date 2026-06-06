> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Project disclosure note — items Hermes should have stated earlier

Status: active caveat / operator-facing
Date: 2026-05-21

The operator asked whether there is anything about the project Hermes should have said but had not said clearly enough. Current answer: yes.

## 1. Kali shared repo path is currently not usable from the SSH wrapper

During the headers/CORS run, the Kali SSH wrapper connected, but both expected repo paths failed:

```text
cd: /home/kali/projects/cybersec: Permission denied
cd: /mnt/hacking: Permission denied
```

Impact:

- Windows Git-Bash can still reach the local靶機 and run many scripts.
- Kali-native tooling remains usable if invoked from a path Kali can access, but repo-mounted workflow is impaired.
- This should be fixed before relying on Kali as the default tool VM for bigger scans/tool runs.

Suggested follow-up:

```text
fix Kali shared-folder permissions or remount /mnt/hacking so user kali can read the repo
```

## 2. The working tree contains many old untracked/modified artifacts

`git status` shows many historical untracked handoff/report/test/module files and some modified rolling handoffs unrelated to the current slice.

Impact:

- It is easy to accidentally commit stale work.
- PR scope is harder to review.
- The project needs a cleanup/archive pass soon.

Current mitigation:

- Recent commits staged only focused files.
- Runtime/download artifacts remain under ignored `<artifact-output-dir>/` and `setting/local/`.

## 3. The GitHub PR is carrying too many phases in one branch

The active branch/PR is still:

```text
feat/p1-4-program-policy-boundary
PR #1: feat(policy/schema): program gates, module contracts, runner, and discovery
```

But the branch now includes Phase 4B learning-lab/module work too.

Impact:

- PR title/body no longer describes the final scope well.
- Review burden is high.

Suggested follow-up:

- Either retitle/update PR as a broad platform+lab milestone PR, or split future work onto a new Phase 4B branch after stabilizing this one.

## 4. Runtime artifacts are intentionally not committed

The actual downloaded tools/wordlists and lab run outputs are under ignored paths:

```text
setting/local/tool_acquisition/wave1_20260521/
<artifact-output-dir>/...
```

Impact:

- The repo has summaries/manifests, not the full third-party repos or raw runtime outputs.
- This is good for repo hygiene, but the operator should know local artifacts are machine-local.

## 5. Learning-stage safety pause is local-lab only

The new pause removes over-broad internal project brakes for learning, but it does not authorize public/unknown target testing or abuse surfaces.

Still not allowed:

```text
public/unknown targets without scope
malware
stealth persistence
real credential theft
real exfiltration
unauthorized pivoting
automatic submission
scanner output -> confirmed finding promotion
```

## 6. OWASP spelling correction

The user wrote `OWSAP`; project docs should use `OWASP`. This is only a spelling issue, not a scope change.
