> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video/Shorts Channel Script Engine Modularization

Use this reference when a video automation project has multiple channels or formats whose script logic is starting to diverge. The goal is to prevent prompt/rules drift across channels while preserving upload/privacy safety.

## Trigger conditions

Apply this pattern when:

- Different channels need different hooks, pacing, source selection, or metadata labels.
- An experimental format must not fall through to the normal narration/stock-video pipeline.
- Public audience reaction will be used to tune one channel without contaminating other channels.
- The existing code has `if channel/story_source == ...` branches inside a large pipeline function.

## Phase 1: behavior-preserving registry

Start with a narrow registry layer. Do not change creative strategy and architecture in the same phase.

Example target shape:

```text
script_engines/
  __init__.py
  base.py
  normal_narration.py
  reddit_rewrite.py
  experimental_stub.py
```

Example API:

```python
@dataclass
class ScriptContext:
    channel: Channel
    topic: str | None
    strategy_hint: str = ""

@dataclass
class ScriptResult:
    topic: str
    script: dict
    seed: dict | None = None  # engine-specific opaque payload

class ScriptEngine(Protocol):
    name: str
    def create_script(self, context: ScriptContext) -> ScriptResult: ...
```

Use lazy factories or method-local imports to avoid circular imports with a legacy `pipeline.py`:

```python
ENGINE_FACTORIES = {
    "normal_narration_v1": NormalNarrationEngine,
    "reddit_rewrite_v1": RedditRewriteEngine,
    "meme_theater_v1": MemeTheaterOfflineStub,
}

def get_script_engine(name: str) -> ScriptEngine:
    try:
        return ENGINE_FACTORIES[name]()
    except KeyError:
        raise ValueError(f"Unknown script engine: {name}")
```

## Preserve manual-test semantics

If a channel currently has a manual topic/local-test path, preserve it in Phase 1. For example, a Reddit channel may fetch/rewrite Reddit stories in auto mode, but a manually supplied `--topic` may intentionally use normal script generation for local tests. Do not silently reclassify those outputs as the channel's auto engine for future analytics.

## Experimental formats fail closed

For disabled or proposal-only formats, create an engine stub that raises before any TTS, stock asset download, DB write, upload, scheduler, or OAuth action:

```python
class MemeTheaterOfflineStub:
    name = "meme_theater_v1"

    def create_script(self, context: ScriptContext) -> ScriptResult:
        raise RuntimeError("meme_theater_v1 is offline-only in this phase")
```

This protects experimental configs from accidentally entering the normal narration pipeline.

## TDD checklist

Write tests before production code:

- Default channel resolves to the normal script engine.
- Unknown engine fails closed with the engine name.
- Experimental/offline engine raises before downstream work.
- Normal adapter delegates to the existing normal script function and preserves shape.
- Specialized adapter delegates to the existing source/rewrite functions and preserves metadata.
- The main pipeline asks the registry for the selected engine but leaves TTS/render/upload behavior untouched.
- Existing disabled-format isolation tests still pass unmodified.

## Safety boundaries

Do not change in the registry phase:

- Upload/publication behavior.
- Scheduler behavior.
- OAuth/token/client-secret handling.
- Privacy defaults or render-fix gates.
- Active channel destinations.
- Runtime user data or generated videos.
- Disabled experimental channel activation.

## Next phase after registry

Only after the registry is stable, add channel-specific strategy labels for analytics, such as:

```json
{
  "format": "workplace_justice",
  "hook_type": "artifact_contradiction",
  "tone": "satisfying_reversal",
  "artifact": "email",
  "payoff": "HR_exposure"
}
```

This lets public audience reaction tune each channel by archetype, not just by broad title/topic.
