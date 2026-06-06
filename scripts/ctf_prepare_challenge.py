#!/usr/bin/env python3
"""Prepare a local CTF challenge artifact directory.

P2.17 offline/local CTF artifact preparer. Standard-library only.

The script creates ``setting/local/ctf/<slug>/`` and writes two artifacts:

* ``challenge.json`` -- operator-supplied metadata (slug, category, source,
  kali_required flag, created_at_utc).
* ``solve_notes.md`` -- a skeleton solve note containing the output-side review
  checklist from ``handoff/ctf_workflow_validation_and_escalation.md``.

The script is intentionally inert:

* No network, no sockets, no external target interaction.
* No subprocess against external hosts.
* Refuses to overwrite an existing slug directory or artifacts unless
  ``--force`` is supplied (idempotency).
* The slug must be operator-supplied; it is never derived from a URL or host.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
ALLOWED_CATEGORIES = (
    "crypto",
    "web",
    "reverse",
    "forensics",
    "misc",
    "pwn",
    "unknown",
)
SOURCE_MAX_LEN = 256

CHECKLIST_LINES = (
    "- [ ] Is scope/authorization clear?",
    "- [ ] Is this output a hint, candidate, or verified result?",
    "- [ ] Is there an independent invariant/checksum/parser/oracle validation?",
    "- [ ] Does the result have expected format and terminator/wrapper rules?",
    "- [ ] Could the checker/UI/scanner have accepted a false positive?",
    "- [ ] Did any tool time out or fail in a way that changes confidence?",
    "- [ ] If using external writeups/PoCs, was the active instance verified?",
    "- [ ] Does this require a second agent/reviewer before reporting/submission?",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _resolve_repo_root(explicit: str | None) -> Path:
    if explicit is not None:
        return Path(explicit).resolve()
    return Path(__file__).resolve().parents[1]


def _validate_slug(slug: str) -> str | None:
    if not isinstance(slug, str):
        return "slug must be a string"
    if not SLUG_RE.match(slug):
        return (
            "slug must match ^[a-z0-9][a-z0-9._-]{1,63}$ "
            "(operator-supplied; not derived from URL/host)"
        )
    if "/" in slug or "\\" in slug or slug.startswith("."):
        return "slug must not contain path separators or leading dot"
    return None


def _validate_category(category: str) -> str | None:
    if category not in ALLOWED_CATEGORIES:
        return (
            f"category must be one of {list(ALLOWED_CATEGORIES)}; got {category!r}"
        )
    return None


def _validate_source(source: str) -> str | None:
    if not isinstance(source, str):
        return "source must be a string"
    if len(source) > SOURCE_MAX_LEN:
        return f"source must be <= {SOURCE_MAX_LEN} chars"
    if any(ord(c) < 0x20 for c in source):
        return "source must not contain control characters"
    return None


def _challenge_json(slug: str, category: str, source: str, kali_required: bool) -> dict:
    return {
        "schema_hint": "ctf_challenge_local/0.1-unversioned",
        "slug": slug,
        "category": category,
        "source": source,
        "kali_required": bool(kali_required),
        "created_at_utc": _utc_now(),
    }


def _solve_notes_text(slug: str, category: str, kali_required: bool) -> str:
    lines: list[str] = []
    lines.append(f"# Solve notes: {slug}")
    lines.append("")
    lines.append(f"- Category: {category}")
    lines.append(f"- Kali required for external interaction: {str(bool(kali_required)).lower()}")
    lines.append("")
    lines.append("## Triage")
    lines.append("")
    lines.append("- [ ] Confirm CTF/training scope and authorization.")
    lines.append("- [ ] Identify weakness class and likely tooling.")
    lines.append("- [ ] If external service/URL is involved, use Kali (control plane stays on the host repo).")
    lines.append("")
    lines.append("## Working notes")
    lines.append("")
    lines.append("Add observations here. Treat intermediate outputs as candidates until verified.")
    lines.append("")
    lines.append("## Output-side review checklist")
    lines.append("")
    lines.append("Before treating any answer/finding as accepted:")
    lines.append("")
    lines.extend(CHECKLIST_LINES)
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    lines.append("Pipe a structured result through `scripts/ctf_review_decision.py` to obtain a")
    lines.append("status/confidence/triggers decision. The decision helper is offline and pure.")
    lines.append("")
    return "\n".join(lines)


def _write_text_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(path)


def _write_json_atomic(path: Path, payload: dict) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    _write_text_atomic(path, rendered)


def prepare_challenge(
    *,
    repo_root: Path,
    slug: str,
    category: str,
    source: str,
    kali_required: bool,
    force: bool,
) -> tuple[int, dict]:
    """Perform the prepare action. Returns (exit_code, report_dict).

    Pure helper -- no stdout/stderr writing happens here.
    """

    error = _validate_slug(slug)
    if error is not None:
        return 2, {"status": "error", "error": error, "error_code": "INVALID_SLUG"}

    error = _validate_category(category)
    if error is not None:
        return 2, {"status": "error", "error": error, "error_code": "INVALID_CATEGORY"}

    error = _validate_source(source)
    if error is not None:
        return 2, {"status": "error", "error": error, "error_code": "INVALID_SOURCE"}

    ctf_root = (repo_root / "setting" / "local" / "ctf").resolve()
    slug_dir = (ctf_root / slug).resolve()

    try:
        slug_dir.relative_to(ctf_root)
    except ValueError:
        return 2, {
            "status": "error",
            "error": "resolved slug directory escaped setting/local/ctf",
            "error_code": "PATH_ESCAPE",
        }

    challenge_path = slug_dir / "challenge.json"
    notes_path = slug_dir / "solve_notes.md"

    pre_existing = slug_dir.exists() or challenge_path.exists() or notes_path.exists()
    if pre_existing and not force:
        return 1, {
            "status": "exists",
            "error": "slug directory or artifacts already exist; rerun with --force to overwrite",
            "error_code": "ALREADY_EXISTS",
            "slug_dir": str(slug_dir),
        }

    if slug_dir.is_symlink():
        return 2, {
            "status": "error",
            "error": "slug directory is a symlink; refusing to write",
            "error_code": "UNSAFE_SLUG_DIR",
            "slug_dir": str(slug_dir),
        }

    slug_dir.mkdir(parents=True, exist_ok=True)

    if challenge_path.is_symlink() or notes_path.is_symlink():
        return 2, {
            "status": "error",
            "error": "artifact path is a symlink; refusing to write",
            "error_code": "UNSAFE_ARTIFACT_PATH",
            "slug_dir": str(slug_dir),
        }

    challenge_payload = _challenge_json(slug, category, source, kali_required)
    _write_json_atomic(challenge_path, challenge_payload)
    _write_text_atomic(notes_path, _solve_notes_text(slug, category, kali_required))

    return 0, {
        "status": "ok",
        "slug": slug,
        "slug_dir": str(slug_dir),
        "wrote": [str(challenge_path), str(notes_path)],
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ctf_prepare_challenge",
        description=(
            "Create setting/local/ctf/<slug>/ with challenge.json and solve_notes.md. "
            "Offline/local only; no network, sockets, or target interaction."
        ),
    )
    parser.add_argument("--slug", required=True, help="Operator-supplied slug. Not derived from URL/host.")
    parser.add_argument(
        "--category",
        required=True,
        choices=ALLOWED_CATEGORIES,
        help="Challenge category.",
    )
    parser.add_argument(
        "--source",
        default="",
        help="Free-text origin (e.g. 'picoCTF 2024', 'lab'). Bounded length.",
    )
    parser.add_argument(
        "--kali-required",
        action="store_true",
        help="Mark this challenge as requiring Kali for external service interaction.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting an existing slug directory and artifacts.",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Override repo root. Defaults to the parent of scripts/.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    repo_root = _resolve_repo_root(args.repo_root)
    if not repo_root.is_dir():
        sys.stderr.write(
            json.dumps(
                {
                    "status": "error",
                    "error": f"repo root not a directory: {repo_root}",
                    "error_code": "REPO_ROOT_MISSING",
                },
                sort_keys=True,
            )
            + "\n"
        )
        return 2

    code, report = prepare_challenge(
        repo_root=repo_root,
        slug=args.slug,
        category=args.category,
        source=args.source,
        kali_required=args.kali_required,
        force=args.force,
    )

    stream = sys.stdout if code == 0 else sys.stderr
    stream.write(json.dumps(report, sort_keys=True) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
