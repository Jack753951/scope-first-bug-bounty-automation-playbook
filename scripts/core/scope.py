"""Target normalization and offline scope matching helpers.

This module performs policy matching only. It never opens sockets, resolves DNS,
or calls external tools.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


DOMAIN_RE = re.compile(r"^[a-z0-9-]+(?:\.[a-z0-9-]+)+$")
CONTROL_OR_SPACE_RE = re.compile(r"[\x00-\x20\x7f]")


@dataclass(frozen=True)
class NormalizedTarget:
    original: str
    normalized: str
    target_type: str
    host: str | None = None
    scheme: str | None = None
    port: int | None = None
    path: str | None = None
    ip: ipaddress.IPv4Address | None = None
    network: ipaddress.IPv4Network | None = None


@dataclass(frozen=True)
class ScopeEntry:
    entry_type: str
    value: str
    include_apex: bool = True
    source: str = "scope"


@dataclass
class ScopeParseResult:
    entries: list[ScopeEntry] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class TargetParseResult:
    target: NormalizedTarget | None
    errors: tuple[str, ...] = ()


def _is_safe_ascii_text(value: str) -> bool:
    return value.isascii() and not CONTROL_OR_SPACE_RE.search(value)


def validate_domain_name(value: str, *, allow_localhost: bool = False) -> str | None:
    if not value:
        return "domain is empty"
    if not value.isascii():
        return "raw Unicode/IDN targets are not allowed; use reviewed punycode"
    if value != value.lower():
        return "domain must be lowercase ASCII/punycode"
    if value.endswith("."):
        return "domain must not use a trailing dot"
    if allow_localhost and value == "localhost":
        return None
    if len(value) > 253:
        return "domain must be 253 characters or shorter"
    if not DOMAIN_RE.fullmatch(value):
        return "domain must contain at least two valid labels"
    for label in value.split("."):
        if len(label) > 63:
            return "domain labels must be 63 characters or shorter"
        if label.startswith("-") or label.endswith("-"):
            return "domain labels must not start or end with hyphen"
    return None


def normalize_target(value: str) -> TargetParseResult:
    errors: list[str] = []
    if not isinstance(value, str) or not value:
        return TargetParseResult(None, ("target must be a non-empty string",))
    if value != value.strip():
        errors.append("target must not contain leading or trailing whitespace")
    if not _is_safe_ascii_text(value):
        errors.append("target must be ASCII and contain no whitespace/control characters")
    if errors:
        return TargetParseResult(None, tuple(errors))

    lowered = value.lower()
    if _is_ipv6_literal_or_network(lowered):
        return TargetParseResult(None, ("IPv6 targets are unsupported by current policy",))

    parsed = urlsplit(lowered)
    if parsed.scheme or parsed.netloc:
        return _normalize_url(value, parsed)

    try:
        network = ipaddress.IPv4Network(lowered, strict=False)
    except ValueError:
        network = None
    else:
        if "/" in lowered:
            return TargetParseResult(
                NormalizedTarget(
                    original=value,
                    normalized=str(network),
                    target_type="cidr",
                    network=network,
                )
            )

    try:
        address = ipaddress.IPv4Address(lowered)
    except ValueError:
        address = None
    else:
        return TargetParseResult(
            NormalizedTarget(
                original=value,
                normalized=str(address),
                target_type="ip",
                host=str(address),
                ip=address,
            )
        )

    reason = validate_domain_name(lowered, allow_localhost=True)
    if reason:
        return TargetParseResult(None, (f"unsupported or invalid target syntax: {reason}",))
    return TargetParseResult(
        NormalizedTarget(
            original=value,
            normalized=lowered,
            target_type="domain",
            host=lowered,
        )
    )


def _normalize_url(original: str, parsed) -> TargetParseResult:
    errors: list[str] = []
    if parsed.scheme not in {"http", "https"}:
        errors.append("URL target must use http or https")
    if parsed.username or parsed.password:
        errors.append("URL target must not contain userinfo")
    if not parsed.netloc or parsed.hostname is None:
        errors.append("URL target must include a host")
        return TargetParseResult(None, tuple(errors))

    host = parsed.hostname.lower()
    if not host.isascii():
        errors.append("URL host must be ASCII/punycode only")
    try:
        port = parsed.port
    except ValueError:
        errors.append("URL target port must be 1-65535")
        port = None
    if port is not None and not 1 <= port <= 65535:
        errors.append("URL target port must be 1-65535")

    ip_address = None
    try:
        ip_address = ipaddress.IPv4Address(host)
    except ValueError:
        if _is_ipv6_literal_or_network(host):
            errors.append("IPv6 targets are unsupported by current policy")
        else:
            reason = validate_domain_name(host, allow_localhost=True)
            if reason:
                errors.append(f"URL host is invalid: {reason}")

    if errors:
        return TargetParseResult(None, tuple(errors))
    path = parsed.path or "/"
    return TargetParseResult(
        NormalizedTarget(
            original=original,
            normalized=host,
            target_type="url",
            host=host,
            scheme=parsed.scheme,
            port=port,
            path=path,
            ip=ip_address,
        )
    )


def _is_ipv6_literal_or_network(value: str) -> bool:
    try:
        if "/" in value:
            ipaddress.IPv6Network(value, strict=False)
        else:
            ipaddress.IPv6Address(value)
    except ValueError:
        return False
    return True


def load_global_scope(path: str | Path) -> ScopeParseResult:
    result = ScopeParseResult()
    source_path = Path(path)
    try:
        lines = source_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        result.errors.append(f"global scope file not found: {source_path}")
        return result
    except PermissionError:
        result.errors.append(f"global scope file permission denied: {source_path}")
        return result
    except UnicodeDecodeError as exc:
        result.errors.append(f"global scope file is not valid UTF-8: {exc}")
        return result

    for line_number, raw_line in enumerate(lines, start=1):
        body = raw_line.split("#", 1)[0].strip()
        if not body:
            continue
        entry = parse_global_scope_line(body, f"{source_path}:{line_number}")
        if entry is None:
            result.warnings.append(f"{source_path}:{line_number}: unsupported scope entry ignored")
            continue
        result.entries.append(entry)
    if not result.entries:
        result.errors.append(f"global scope file contains no usable entries: {source_path}")
    return result


def parse_global_scope_line(value: str, source: str) -> ScopeEntry | None:
    lowered = value.lower()
    if not _is_safe_ascii_text(lowered):
        return None
    if lowered.startswith("*."):
        if validate_domain_name(lowered[2:], allow_localhost=False) is None:
            return ScopeEntry("wildcard", lowered, include_apex=True, source=source)
        return None
    parsed = urlsplit(lowered)
    if parsed.scheme or parsed.netloc:
        if _parse_url_prefix(lowered) is not None:
            return ScopeEntry("url_prefix", lowered, source=source)
        return None
    try:
        if "/" in lowered:
            return ScopeEntry("cidr", str(ipaddress.IPv4Network(lowered, strict=False)), source=source)
        return ScopeEntry("ip", str(ipaddress.IPv4Address(lowered)), source=source)
    except ValueError:
        pass
    if validate_domain_name(lowered, allow_localhost=True) is None:
        return ScopeEntry("domain", lowered, source=source)
    return None


def entries_from_program_scope(entries: list[dict[str, Any]], source: str) -> ScopeParseResult:
    result = ScopeParseResult()
    for index, item in enumerate(entries):
        entry_type = item.get("type")
        value = item.get("value")
        if not isinstance(entry_type, str) or not isinstance(value, str):
            result.errors.append(f"{source}[{index}]: scope entry must contain string type and value")
            continue
        include_apex = item.get("include_apex", True)
        if not isinstance(include_apex, bool):
            result.errors.append(f"{source}[{index}]: include_apex must be boolean")
            continue
        if not value.isascii():
            result.errors.append(f"{source}[{index}]: raw Unicode/IDN scope entries are unsupported")
            continue
        result.entries.append(
            ScopeEntry(
                entry_type=entry_type,
                value=value.lower(),
                include_apex=include_apex,
                source=f"{source}[{index}]",
            )
        )
    return result


def target_matches_any(target: NormalizedTarget, entries: list[ScopeEntry]) -> bool:
    return any(target_matches_entry(target, entry) for entry in entries)


def target_matches_entry(target: NormalizedTarget, entry: ScopeEntry) -> bool:
    if entry.entry_type == "domain":
        return _target_host(target) == entry.value
    if entry.entry_type == "wildcard":
        if not entry.value.startswith("*."):
            return False
        return _host_matches_wildcard(_target_host(target), entry.value[2:], entry.include_apex)
    if entry.entry_type == "ip":
        return _target_ip(target) == _safe_ipv4_address(entry.value)
    if entry.entry_type == "cidr":
        return _target_in_cidr(target, entry.value)
    if entry.entry_type == "url_prefix":
        return _url_matches_prefix(target, entry.value)
    return False


def _target_host(target: NormalizedTarget) -> str | None:
    if target.target_type in {"domain", "url", "ip"}:
        return target.host
    return None


def _target_ip(target: NormalizedTarget) -> ipaddress.IPv4Address | None:
    return target.ip


def _safe_ipv4_address(value: str) -> ipaddress.IPv4Address | None:
    try:
        return ipaddress.IPv4Address(value)
    except ValueError:
        return None


def _host_matches_wildcard(host: str | None, base: str, include_apex: bool) -> bool:
    if host is None:
        return False
    if include_apex and host == base:
        return True
    return host.endswith("." + base)


def _target_in_cidr(target: NormalizedTarget, value: str) -> bool:
    try:
        network = ipaddress.IPv4Network(value, strict=False)
    except ValueError:
        return False
    if target.ip is not None:
        return target.ip in network
    if target.network is not None:
        return target.network.subnet_of(network)
    return False


def _parse_url_prefix(value: str):
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.username or parsed.password or parsed.hostname is None:
        return None
    host = parsed.hostname.lower()
    try:
        port = parsed.port
    except ValueError:
        return None
    if port is not None and not 1 <= port <= 65535:
        return None
    if not parsed.path.startswith("/") or parsed.path == "":
        return None
    if parsed.query or parsed.fragment:
        return None
    try:
        ipaddress.IPv4Address(host)
    except ValueError:
        if validate_domain_name(host, allow_localhost=True) is not None:
            return None
    return parsed


def _url_matches_prefix(target: NormalizedTarget, prefix: str) -> bool:
    if target.target_type != "url":
        return False
    parsed = _parse_url_prefix(prefix)
    if parsed is None or parsed.hostname is None:
        return False
    if target.scheme != parsed.scheme:
        return False
    if target.host != parsed.hostname.lower():
        return False
    try:
        prefix_port = parsed.port
    except ValueError:
        return False
    if target.port != prefix_port:
        return False
    return (target.path or "/").startswith(parsed.path)
