#!/usr/bin/env python3
"""Shared profile issue vocabulary and detail helpers.

This module is intentionally standard-library only and performs no filesystem,
network, scanner, module, subprocess, callback, or target-touching activity. It
centralizes stable machine-readable profile issue codes plus the JSON-compatible
issue-detail shape used by the dry-run runner and profile validator CLIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROFILE_ID_INVALID = "PROFILE_ID_INVALID"
PROFILE_NOT_FOUND = "PROFILE_NOT_FOUND"
PROFILE_PATH_INVALID = "PROFILE_PATH_INVALID"
PROFILE_READ_ERROR = "PROFILE_READ_ERROR"
PROFILE_MALFORMED_JSON = "PROFILE_MALFORMED_JSON"
PROFILE_SCHEMA_INVALID = "PROFILE_SCHEMA_INVALID"
PROFILE_ID_MISMATCH = "PROFILE_ID_MISMATCH"
PROFILE_MEMBERSHIP_MISMATCH = "PROFILE_MEMBERSHIP_MISMATCH"
PROFILE_CONSTRAINT_MODE = "PROFILE_CONSTRAINT_MODE"
PROFILE_CONSTRAINT_RISK = "PROFILE_CONSTRAINT_RISK"
PROFILE_CONSTRAINT_TARGET_TYPE = "PROFILE_CONSTRAINT_TARGET_TYPE"
PROFILE_CONSTRAINT_TECHNIQUE_TAG = "PROFILE_CONSTRAINT_TECHNIQUE_TAG"
PROFILE_CONSTRAINT_EXECUTION = "PROFILE_CONSTRAINT_EXECUTION"
PROFILE_CONSTRAINT_OUTPUT = "PROFILE_CONSTRAINT_OUTPUT"
PROFILE_CONSTRAINT_SAFETY_GATE = "PROFILE_CONSTRAINT_SAFETY_GATE"
PROFILE_EMPTY_SELECTION = "PROFILE_EMPTY_SELECTION"

PROFILE_ERROR_CODES = frozenset(
    {
        PROFILE_ID_INVALID,
        PROFILE_NOT_FOUND,
        PROFILE_PATH_INVALID,
        PROFILE_READ_ERROR,
        PROFILE_MALFORMED_JSON,
        PROFILE_SCHEMA_INVALID,
        PROFILE_ID_MISMATCH,
        PROFILE_MEMBERSHIP_MISMATCH,
        PROFILE_CONSTRAINT_MODE,
        PROFILE_CONSTRAINT_RISK,
        PROFILE_CONSTRAINT_TARGET_TYPE,
        PROFILE_CONSTRAINT_TECHNIQUE_TAG,
        PROFILE_CONSTRAINT_EXECUTION,
        PROFILE_CONSTRAINT_OUTPUT,
        PROFILE_CONSTRAINT_SAFETY_GATE,
        PROFILE_EMPTY_SELECTION,
    }
)


@dataclass(frozen=True)
class IssueDetail:
    code: str
    message: str
    severity: str = "error"
    component: str = "module_profile"
    path: str | None = None
    field: str | None = None
    profile_id: str | None = None
    module_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "component": self.component,
        }
        for key in ("path", "field", "profile_id", "module_id"):
            value = getattr(self, key)
            if value is not None:
                payload[key] = value
        return payload


def issue_codes(details: list[IssueDetail]) -> list[str]:
    return sorted({issue.code for issue in details})


def add_issue(
    messages: list[str],
    details: list[IssueDetail] | None,
    code: str,
    message: str,
    *,
    severity: str = "error",
    component: str = "module_profile",
    path: Path | str | None = None,
    field: str | None = None,
    profile_id: str | None = None,
    module_id: str | None = None,
) -> None:
    """Append a human-readable message and optional structured detail."""
    messages.append(message)
    if details is not None:
        details.append(
            IssueDetail(
                code=code,
                message=message,
                severity=severity,
                component=component,
                path=str(path) if path is not None else None,
                field=field,
                profile_id=profile_id,
                module_id=module_id,
            )
        )


def add_warning(
    messages: list[str],
    details: list[IssueDetail] | None,
    code: str,
    message: str,
    *,
    component: str = "module_profile",
    path: Path | str | None = None,
    field: str | None = None,
    profile_id: str | None = None,
    module_id: str | None = None,
) -> None:
    """Append a warning message and optional structured warning detail."""
    add_issue(
        messages,
        details,
        code,
        message,
        severity="warning",
        component=component,
        path=path,
        field=field,
        profile_id=profile_id,
        module_id=module_id,
    )
