> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent Hermes Pipeline Example

Context: Windows host where the terminal tool runs commands through Git-Bash/MSYS bash, while the project documentation shows PowerShell commands.

## Observed Pattern

The documented command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_hermes_pipeline.ps1 -Mode full
```

failed from bash because PowerShell received a malformed `-File` path resembling `.run_hermes_pipeline.ps1`.

The working bash-safe command was:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_hermes_pipeline.ps1' -Mode full
```

The same conversion worked for adding flags:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_hermes_pipeline.ps1' -Mode full -UseClaudeCode
```

## Orchestration Follow-up

After a pipeline command finishes, inspect generated handoff reports rather than relying only on stdout:

- `handoff/hermes_run.md`
- `handoff/latest_check.md`
- `handoff/codex_review.md`
- `handoff/accepted_changes.md`

If the pipeline reports that a proposal is still template-only, stop orchestration and ask for a real proposal instead of forcing implementation.

## API key reload in wrappers

In this project, required API keys existed as Windows User environment variables, but some already-running processes did not inherit them. The durable fix was not to reinstall keys; it was to update `run_agent.ps1` to import User-scoped variables into the Process scope before invoking Python. Verification should print only presence (`set`/`missing`), never secret values.

Known-good wrapper snippet:

```powershell
function Import-UserEnvironmentVariable {
    param([string]$Name)
    if (-not [Environment]::GetEnvironmentVariable($Name, "Process")) {
        $value = [Environment]::GetEnvironmentVariable($Name, "User")
        if ($value) {
            [Environment]::SetEnvironmentVariable($Name, $value, "Process")
        }
    }
}

foreach ($name in @("ANTHROPIC_API_KEY", "PEXELS_API_KEY", "ELEVENLABS_API_KEY")) {
    Import-UserEnvironmentVariable $name
}
```

Validate through the wrapper, not direct Python, when testing this behavior:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
```

## Local verification after worker sandbox blockers

Codex/Claude worker sandboxes can misreport the project Python or `.venv` as broken even when the local wrapper environment is healthy. Do not leave `handoff/codex_review.md` or `handoff/accepted_changes.md` saying Python validation is blocked until local verification has been tried from the project root.

Bash-safe verification sequence:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\\.venv\\Scripts\\python.exe' -m py_compile agent.py pipeline.py config.py database.py youtube_api.py strategy.py competitor.py render_qa.py; exit $LASTEXITCODE"
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\\.venv\\Scripts\\python.exe' -m unittest tests.test_safety_optimizations -v; exit $LASTEXITCODE"
powershell -NoProfile -ExecutionPolicy Bypass -File './run_codex_review.ps1'
```

If these pass, patch the handoff docs to record the worker issue as a sandbox/PATH mismatch, not a project blocker. The refreshed `handoff/latest_check.md` should show Python compile OK and `.agent.lock` clear.

## Safe local draft / render QA loop

For the YouTube agent project, after render or subtitle-safety changes, prefer upload-free draft review before any create/upload path:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel redditstories 1
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' review-output --channel redditstories
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' review-output --channel redditstories --path 'data\\redditstories\\output\\...\\final_short.mp4'
```

Use `draft` for production rendering without YouTube upload/OAuth, then `review-output` for MP4 readability, duration/metadata, subtitle checks, and channel font-size caps. Keep `DEFAULT_PRIVACY = "private"` and any force-private render-fix gate intact until visual review is clean.

When the user asks to "run one and let me see the result", do the full delivery loop, not just generation:

1. Run `./run_agent.ps1 validate` first to confirm `.agent.lock`, API-key visibility, `DEFAULT_PRIVACY`, and ffmpeg/ffprobe.
2. Run the upload-free draft command for the requested channel.
3. Read the emitted `metadata.json` and `subtitles.srt` to report title/topic/path and catch obvious transcript errors.
4. Run `review-output --path <final_short.mp4>` explicitly even if draft already ran QA, so the path is verified after generation.
5. Extract a contact sheet and at least one full-resolution frame for visual inspection. From bash on Windows, ffmpeg may rewrite `/tmp/...` to the Windows temp path; use the output path ffmpeg reports or a native Windows path if needed.

```bash
mkdir -p /tmp/redditstories_review
ffmpeg -y -i '<user-home> \
  -vf "select='eq(n,30)+eq(n,180)+eq(n,360)+eq(n,600)+eq(n,900)',scale=270:480,tile=5x1" \
  -frames:v 1 /tmp/redditstories_review/contact.jpg
ffmpeg -y -ss 00:00:21.8 -i '<user-home> \
  -frames:v 1 /tmp/redditstories_review/frame_21s.jpg
```

6. Inspect the contact sheet/frame visually for subtitle obstruction, hook-box styling, subject relevance, and Whisper mistranscriptions.
7. Open the MP4 for the user with PowerShell `Start-Process`, then report the plain Windows path and concise QA findings. Quote the entire PowerShell command with outer single quotes so bash does not expand `$p`/`$f`:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -Command '$p = "<user-home>"; Start-Process -FilePath $p; $f=Get-Item $p; Write-Output ("OPENED=" + $f.FullName); Write-Output ("SIZE_MB=" + [Math]::Round($f.Length/1MB,2))'
```

Pitfall: if you use double quotes around that `-Command` from bash, `$p` and `$f` can be expanded away before PowerShell sees them, causing ParserError messages such as `Unexpected token '.FullName'`. Retrying with outer single quotes is the durable pattern.

## Visual template iteration loop

When the user delegates YouTube-agent channel styling decisions (subtitle shadow, frame choice, Shorts aesthetics), make an owner decision and run a measurable local loop instead of only describing options:

1. Update `handoff/claude_proposal.md` with the channel-scoped decision and safety constraints.
2. Apply only channel JSON / handoff edits unless engineering changes are explicitly required.
3. Keep `redditscary` unchanged unless the user asks; for non-scary channels, treat `chinese` and `redditstories` separately.
4. Validate before rendering:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
node -e "const fs=require('fs'); for (const f of fs.readdirSync('channels').filter(f=>f.endsWith('.json'))) { JSON.parse(fs.readFileSync('channels/'+f,'utf8')); console.log('OK '+f) }"
```

5. Render upload-free drafts with the new style:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel chinese 1
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel redditstories 1
```

6. Read each `metadata.json`, extract contact sheets, and inspect visually before reporting. Prefer Python `subprocess.run([...])` for ffmpeg contact sheets when paths contain CJK or when PowerShell quoting would involve `$p` variables from bash.

Example Python contact-sheet extraction:

```python
import subprocess
subprocess.run([
    'ffmpeg', '-y', '-i', r'C:\path\to\final_short.mp4',
    '-vf', 'fps=1/7,scale=270:-1,tile=5x1',
    '-frames:v', '1', '-update', '1', r'<user-home>
], check=True)
```

7. Update `handoff/codex_review.md`, `handoff/accepted_changes.md`, then rerun `run_codex_review.ps1` so `handoff/latest_check.md` is current.

Project-specific visual heuristics observed:

- `chinese`: keep `gold_frame.png` for brand continuity, but use a lighter gold-frame style: yellow/gold captions, outline around 2, shadow 0, smaller hook padding, and action-oriented visuals (phone/message/door/office movement). Heavy black panels and thick shadows look dated.
- `redditstories`: a clean no-frame evidence-card look fits better than ornate gold framing. If the renderer does not have a dedicated no-frame switch, setting `frame_image` to an intentional missing asset such as `reddit_clean_no_frame.png` makes the renderer fall back to the template background; document this as intentional so future agents do not "fix" it back to `gold_frame.png`.
- High-traffic Reddit Shorts still need an evidence layer beyond background video + captions: message/card/receipt/email/HR/court-paper overlays and a binary comment-bait ending matter more than another one-pixel subtitle tweak.
- ElevenLabs `paid_plan_required` on library voices is non-blocking in this project when Edge TTS fallback succeeds; report the fallback, but do not treat it as render failure.

## Worker Readiness Example

For project wrappers that call Claude Code, a successful binary check is not enough. If the worker output contains:

```text
Not logged in · Please run /login
```

then the durable fix is for the user to run `claude` interactively and complete `/login`, then rerun the wrapper.

## Native CLI stderr under PowerShell wrappers

In this project, a PowerShell pipeline wrapper had `$ErrorActionPreference = "Stop"` and called a Codex worker through another PowerShell script. Codex prints some progress/banner output via `node.exe` stderr; when the wrapper captured `2>&1`, PowerShell surfaced it as `NativeCommandError` / `RemoteException` and aborted even though the worker pattern should have been governed by `$LASTEXITCODE`.

Durable wrapper pattern:

```powershell
$oldErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
try {
    $Prompt | & $CodexExe exec --sandbox workspace-write --output-last-message $OutFile - 2>&1 |
        Tee-Object -FilePath $LogFile
    $workerExitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $oldErrorActionPreference
}
exit $workerExitCode
```

For a higher-level `Run-Step` helper, use the same scoped preference change around `Invoke-Expression`, then return `[int]$LASTEXITCODE`. This keeps strict behavior for the rest of the script but prevents native CLI stderr from being misclassified as orchestration failure.
