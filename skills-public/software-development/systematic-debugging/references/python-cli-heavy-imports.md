> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Python CLI Heavy Import Debugging Pattern

Use when a lightweight CLI command such as `validate`, `status`, `channels`, or `--help` fails before executing its command logic because the top-level module imports heavy runtime dependencies.

## Symptom

- A non-generation/read-only command fails at process startup with `ModuleNotFoundError` or import-time side effects.
- The missing dependency belongs to a different command path, e.g. video generation, cloud upload, ML inference, browser OAuth, or analytics.
- Running through a project wrapper may pass after environment setup, but direct `python agent.py validate` still proves whether the CLI startup path is robust.

## Investigation Steps

1. Reproduce with the lightest command directly:

```bash
python agent.py validate
python agent.py status
```

2. Inspect top-level imports in the CLI entrypoint. Look for imports of modules that pull in optional/heavy deps such as ML packages, cloud SDKs, browser OAuth, or media libraries.

3. Confirm the import boundary with a regression test that blocks those modules at entrypoint import time:

```python
import builtins, importlib, sys

blocked = {"pipeline", "strategy", "youtube_api"}
original_import = builtins.__import__

def guarded_import(name, *args, **kwargs):
    if name.split(".")[0] in blocked:
        raise AssertionError(f"entrypoint imported {name} at module import time")
    return original_import(name, *args, **kwargs)

sys.modules.pop("agent", None)
builtins.__import__ = guarded_import
try:
    importlib.import_module("agent")
finally:
    builtins.__import__ = original_import
```

4. Fix at the command boundary: keep shared lightweight modules at top level, but lazy-load heavy modules inside the command functions that actually need them.

```python
def get_pipeline():
    import pipeline
    return pipeline

def cmd_create(args):
    pipeline = get_pipeline()
    ...
```

5. Verify both direct and wrapper paths:

```bash
python agent.py validate
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
```

## Pitfalls

- Do not solve startup failures by making every dependency mandatory for every command. Lightweight, read-only commands should stay usable for diagnostics even when optional generation/upload dependencies are absent.
- Do not record a transient missing package as a durable fact. Capture the design lesson: command entrypoints should avoid eager imports of command-specific heavy dependencies.
- Keep lazy imports narrow and explicit; do not hide real runtime requirements for commands that actually need them.
