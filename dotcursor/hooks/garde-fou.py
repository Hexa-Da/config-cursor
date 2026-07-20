#!/usr/bin/env python3
"""Garde-fou sécurité pour hooks Cursor."""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Any, Final

_RM_RF_FLAGS: Final[re.Pattern[str]] = re.compile(
    r"\brm\b[^\n]*?-(?:[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*|[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*)\b",
    re.IGNORECASE,
)
_RM_RECURSIVE: Final[re.Pattern[str]] = re.compile(
    r"\brm\b[^\n]*?(?:-[a-zA-Z]*r[a-zA-Z]*\b|--recursive\b)",
    re.IGNORECASE,
)
_RM_NO_PRESERVE: Final[re.Pattern[str]] = re.compile(
    r"\brm\b[^\n]*?--no-preserve-root\b",
    re.IGNORECASE,
)

_PATH_DELIM: Final[str] = r"[\s;|&`'\"<>)]"
_RM_DANGEROUS_TARGET: Final[re.Pattern[str]] = re.compile(
    r"(?:^|" + _PATH_DELIM + r"|[(])"
    r"(?:"
    r"/(?=" + _PATH_DELIM + r"|$)"
    r"|/\*"
    r"|~(?=" + _PATH_DELIM + r"|/|$)"
    r"|~/(?=" + _PATH_DELIM + r"|$)"
    r"|\$\{?HOME\}?/?(?=" + _PATH_DELIM + r"|$)"
    r"|/(?:bin|sbin|usr|etc|var|System|private|dev|boot|lib|opt|Volumes)"
    r"(?=/|" + _PATH_DELIM + r"|$|\*)"
    r")",
    re.IGNORECASE,
)

_DANGEROUS_SHELL_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"\bmkfs(?:\.\w+)?\b", re.IGNORECASE),
    re.compile(r"\bdiskutil\b[^\n]*\b(?:erase|reformat|partitionDisk|zeroDisk)\b", re.IGNORECASE),
    re.compile(r"\b(?:fdisk|parted|wipefs)\b", re.IGNORECASE),
    re.compile(r"\bdd\b[^\n]*\bof=/dev/(?:sd|hd|nvme|disk|rdisk)\w*", re.IGNORECASE),
    re.compile(r">\s*/dev/(?:sd|hd|nvme|disk|rdisk)\w*", re.IGNORECASE),
    re.compile(r"\btruncate\b[^\n]*/dev/(?:sd|hd|nvme|disk|rdisk)\w*", re.IGNORECASE),
    re.compile(r":\s*\(\)\s*\{\s*:\|:&\s*\}", re.IGNORECASE),
    re.compile(r"\bchmod\b[^\n]*\b777\b[^\n]*/(?:\s|$|\*)", re.IGNORECASE),
    re.compile(r"\bchmod\b[^\n]*-R[^\n]*/(?:\s|$|\*)", re.IGNORECASE),
    re.compile(r"\bchown\b[^\n]*-R[^\n]*/(?:\s|$|\*)", re.IGNORECASE),
    re.compile(r"\bcurl\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b", re.IGNORECASE),
    re.compile(r"\bwget\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b", re.IGNORECASE),
    re.compile(r"\bcurl\b[^\n]*\b(?:-O|-o)\b[^\n]*&&\s*(?:sudo\s+)?(?:ba)?sh\b", re.IGNORECASE),
    re.compile(r"\bshred\b", re.IGNORECASE),
    re.compile(r"\b(?:ba)?sh\s+-i\s+>&\s*/dev/tcp/", re.IGNORECASE),
    re.compile(r"\b(?:nc|ncat|netcat)\b[^\n]*\s-(?:e|c)\b", re.IGNORECASE),
    re.compile(r"\bgit\s+push\b[^\n]*--force(?:-with-lease)?\b", re.IGNORECASE),
    re.compile(r"\bgit\s+push\b[^\n]*\s-f(?:\s|$)", re.IGNORECASE),
    re.compile(r"\bgit\s+push\b[^\n]*--mirror\b", re.IGNORECASE),
    re.compile(r"\bfind\s+/\s+[^\n]*-delete\b", re.IGNORECASE),
    re.compile(r"\bfind\s+/\s+[^\n]*-exec\s+rm\b", re.IGNORECASE),
    re.compile(r"\bcsrutil\s+disable\b", re.IGNORECASE),
    re.compile(r"\bnvram\b[^\n]*\b(?:-c|delete)\b", re.IGNORECASE),
    re.compile(r"\blaunchctl\b[^\n]*\bbootout\s+system\b", re.IGNORECASE),
    re.compile(r"\biptables\b[^\n]*\s-F\b", re.IGNORECASE),
    re.compile(r"\bpfctl\b[^\n]*-F\b", re.IGNORECASE),
)

_CRITICAL_BASENAMES_UNDER_CURSOR: Final[frozenset[str]] = frozenset(
    {"auth.json", "mcp.json", "api_key.txt"}
)
_PROTECTED_TOOL_NAMES: Final[frozenset[str]] = frozenset(
    {"Write", "Delete", "StrReplace"}
)


def _emit_allow() -> None:
    sys.stdout.write('{"permission":"allow"}\n')
    sys.stdout.flush()


def _emit_deny(message: str) -> None:
    payload: dict[str, str] = {
        "permission": "deny",
        "user_message": message,
        "agent_message": message,
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _is_dangerous_rm(command: str) -> bool:
    lowered: str = command.lower()
    if not re.search(r"\brm\b", lowered):
        return False
    if _RM_NO_PRESERVE.search(lowered):
        return True
    recursive: bool = bool(_RM_RF_FLAGS.search(lowered) or _RM_RECURSIVE.search(lowered))
    if not recursive:
        return False
    if _RM_DANGEROUS_TARGET.search(command):
        return True
    try:
        home: str = os.path.realpath(os.path.expanduser("~"))
    except OSError:
        return False
    home_re: re.Pattern[str] = re.compile(
        r"(?:^|" + _PATH_DELIM + r"|[(])"
        + re.escape(home)
        + r"(?:/\*)?(?="
        + _PATH_DELIM
        + r"|$)"
    )
    return bool(home_re.search(command))


def _is_dangerous_shell(command: str) -> bool:
    stripped: str = command.strip()
    if not stripped:
        return False
    if _is_dangerous_rm(stripped):
        return True
    lowered: str = stripped.lower()
    for pattern in _DANGEROUS_SHELL_PATTERNS:
        if pattern.search(lowered):
            return True
    return False


def _extract_tool_path(tool_input: dict[str, Any]) -> str:
    candidate: Any = (
        tool_input.get("path")
        or tool_input.get("file_path")
        or tool_input.get("target_file")
        or tool_input.get("filename")
        or ""
    )
    if isinstance(candidate, str):
        return candidate
    return ""


def _resolve_path(raw_path: str, cwd: str) -> str:
    if not raw_path:
        return ""
    expanded: str = os.path.expanduser(raw_path)
    if os.path.isabs(expanded):
        return os.path.realpath(expanded)
    base: str = cwd if cwd else os.getcwd()
    return os.path.realpath(os.path.join(base, expanded))


def _critical_path_prefixes(home: str) -> tuple[str, ...]:
    return (
        os.path.join(home, ".ssh"),
        os.path.join(home, ".gnupg"),
        os.path.join(home, ".aws"),
        os.path.join(home, ".kube"),
        os.path.join(home, ".netrc"),
        os.path.join(home, ".git-credentials"),
        os.path.join(home, ".npmrc"),
        os.path.join(home, ".password-store"),
        os.path.join(home, ".config", "gh"),
        os.path.join(home, ".config", "gcloud"),
        os.path.join(home, ".docker", "config.json"),
        "/etc",
        "/private/etc",
        "/System",
        "/Library/Application Support/com.apple.TCC",
        "/usr/bin",
        "/usr/sbin",
        "/bin",
        "/sbin",
    )


def _is_critical_path(resolved: str, home: str) -> bool:
    if not resolved:
        return False
    resolved_norm: str = os.path.normpath(resolved)
    try:
        home_real: str = os.path.realpath(home)
    except OSError:
        home_real = home
    for prefix in _critical_path_prefixes(home_real):
        try:
            pfx_real: str = os.path.realpath(os.path.expanduser(prefix))
        except OSError:
            pfx_real = os.path.normpath(os.path.expanduser(prefix))
        if resolved_norm == pfx_real or resolved_norm.startswith(pfx_real + os.sep):
            return True
    cursor_dir: str = os.path.join(home_real, ".cursor")
    basename: str = os.path.basename(resolved_norm)
    if (
        resolved_norm.startswith(cursor_dir + os.sep)
        and basename in _CRITICAL_BASENAMES_UNDER_CURSOR
    ):
        return True
    return False


def main() -> int:
    try:
        data: dict[str, Any] = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.stderr.write("garde-fou: JSON stdin invalide\n")
        return 2

    tool_name: str | None = data.get("tool_name")
    cwd: str = str(data.get("cwd") or "")

    if not tool_name:
        cmd: str = str(data.get("command") or "")
        if _is_dangerous_shell(cmd):
            _emit_deny(
                "Commande shell bloquée par le garde-fou (motif dangereux détecté). "
                "Vérifie la commande ou exécute-la manuellement hors agent."
            )
            return 0
        _emit_allow()
        return 0

    if tool_name in _PROTECTED_TOOL_NAMES:
        ti: Any = data.get("tool_input")
        if not isinstance(ti, dict):
            _emit_allow()
            return 0
        raw_path: str = _extract_tool_path(ti)
        home: str = os.path.expanduser("~")
        resolved: str = _resolve_path(raw_path, cwd)
        if _is_critical_path(resolved, home):
            _emit_deny(
                f"Modification/suppression refusée : chemin critique « {resolved or raw_path} »."
            )
            return 0

    _emit_allow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
