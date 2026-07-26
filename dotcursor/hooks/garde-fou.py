#!/usr/bin/env python3
"""Garde-fou sécurité pour hooks Cursor.

deny  = refusé (catastrophique)
ask   = confirmation utilisateur (risqué mais parfois nécessaire)
allow = OK
"""
from __future__ import annotations

import json
import os
import re
import shlex
import sys
from typing import Any, Final, Literal

Decision = Literal["allow", "ask", "deny"]

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

# Cibles vraiment catastrophiques : /, /*, ~, ~/, $HOME, $HOME/, racines système.
# Important : ~/foo et $HOME/foo ne matchent PAS (scoped → ask si récursif).
_RM_CATASTROPHIC_TARGET: Final[re.Pattern[str]] = re.compile(
    r"(?:^|" + _PATH_DELIM + r"|[(])"
    r"(?:"
    r"/(?=" + _PATH_DELIM + r"|$)"
    r"|/\*"
    r"|~(?=" + _PATH_DELIM + r"|$)"
    r"|~/(?=" + _PATH_DELIM + r"|$)"
    r"|\$\{?HOME\}?(?=" + _PATH_DELIM + r"|$)"
    r"|\$\{?HOME\}?/(?=" + _PATH_DELIM + r"|$)"
    r"|/(?:bin|sbin|usr|etc|var|System|private|dev|boot|lib|opt|Volumes)"
    r"(?=/|" + _PATH_DELIM + r"|$|\*)"
    r")",
    re.IGNORECASE,
)

# Motifs toujours refusés (pas de confirmation possible via l'agent).
_DENY_SHELL_PATTERNS: Final[tuple[tuple[re.Pattern[str], str], ...]] = (
    (re.compile(r"\bmkfs(?:\.\w+)?\b", re.IGNORECASE), "formatage disque (mkfs)"),
    (
        re.compile(r"\bdiskutil\b[^\n]*\b(?:erase|reformat|partitionDisk|zeroDisk)\b", re.IGNORECASE),
        "effacement disque (diskutil)",
    ),
    (re.compile(r"\b(?:fdisk|parted|wipefs)\b", re.IGNORECASE), "partitionnement disque"),
    (
        re.compile(r"\bdd\b[^\n]*\bof=/dev/(?:sd|hd|nvme|disk|rdisk)\w*", re.IGNORECASE),
        "écriture brute sur un disque (dd)",
    ),
    (re.compile(r">\s*/dev/(?:sd|hd|nvme|disk|rdisk)\w*", re.IGNORECASE), "redirection vers un disque"),
    (
        re.compile(r"\btruncate\b[^\n]*/dev/(?:sd|hd|nvme|disk|rdisk)\w*", re.IGNORECASE),
        "truncate sur un disque",
    ),
    (re.compile(r":\s*\(\)\s*\{\s*:\|:&\s*\}", re.IGNORECASE), "fork bomb"),
    (re.compile(r"\bchmod\b[^\n]*\b777\b[^\n]*/(?:\s|$|\*)", re.IGNORECASE), "chmod 777 /"),
    (re.compile(r"\bchmod\b[^\n]*-R[^\n]*/(?:\s|$|\*)", re.IGNORECASE), "chmod -R /"),
    (re.compile(r"\bchown\b[^\n]*-R[^\n]*/(?:\s|$|\*)", re.IGNORECASE), "chown -R /"),
    (
        re.compile(r"\bcurl\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b", re.IGNORECASE),
        "curl | sh (pipe remote → shell)",
    ),
    (
        re.compile(r"\bwget\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b", re.IGNORECASE),
        "wget | sh (pipe remote → shell)",
    ),
    (
        re.compile(r"\bcurl\b[^\n]*\b(?:-O|-o)\b[^\n]*&&\s*(?:sudo\s+)?(?:ba)?sh\b", re.IGNORECASE),
        "curl + exécution shell",
    ),
    (re.compile(r"\bshred\b", re.IGNORECASE), "shred (destruction irréversible)"),
    (
        re.compile(r"\b(?:ba)?sh\s+-i\s+>&\s*/dev/tcp/", re.IGNORECASE),
        "reverse shell",
    ),
    (
        re.compile(r"\b(?:nc|ncat|netcat)\b[^\n]*\s-(?:e|c)\b", re.IGNORECASE),
        "netcat avec exécution (-e/-c)",
    ),
    (re.compile(r"\bgit\s+push\b[^\n]*--mirror\b", re.IGNORECASE), "git push --mirror"),
    (re.compile(r"\bfind\s+/\s+[^\n]*-delete\b", re.IGNORECASE), "find / … -delete"),
    (re.compile(r"\bfind\s+/\s+[^\n]*-exec\s+rm\b", re.IGNORECASE), "find / … -exec rm"),
    (re.compile(r"\bcsrutil\s+disable\b", re.IGNORECASE), "désactivation SIP (csrutil)"),
    (re.compile(r"\bnvram\b[^\n]*\b(?:-c|delete)\b", re.IGNORECASE), "modification NVRAM"),
    (
        re.compile(r"\blaunchctl\b[^\n]*\bbootout\s+system\b", re.IGNORECASE),
        "launchctl bootout system",
    ),
    (re.compile(r"\biptables\b[^\n]*\s-F\b", re.IGNORECASE), "iptables -F"),
    (re.compile(r"\bpfctl\b[^\n]*-F\b", re.IGNORECASE), "pfctl -F"),
)

# Motifs qui demandent confirmation (parfois nécessaires).
_ASK_SHELL_PATTERNS: Final[tuple[tuple[re.Pattern[str], str], ...]] = (
    (
        re.compile(r"\bgit\s+push\b[^\n]*--force-with-lease\b", re.IGNORECASE),
        "git push --force-with-lease",
    ),
    (
        re.compile(r"\bgit\s+push\b[^\n]*--force\b", re.IGNORECASE),
        "git push --force",
    ),
    (
        re.compile(r"\bgit\s+push\b[^\n]*\s-f(?:\s|$)", re.IGNORECASE),
        "git push -f",
    ),
)

_CRITICAL_BASENAMES_UNDER_CURSOR: Final[frozenset[str]] = frozenset(
    {"auth.json", "mcp.json", "api_key.txt"}
)
_PROTECTED_TOOL_NAMES: Final[frozenset[str]] = frozenset(
    {"Write", "Delete", "StrReplace"}
)

_SHELL_SEGMENT_SPLIT: Final[re.Pattern[str]] = re.compile(r"(?:&&|\|\||[;|])")
_MAXDEPTH_RE: Final[re.Pattern[str]] = re.compile(
    r"(?:--maxdepth|-maxdepth)\s+(\d+)\b",
    re.IGNORECASE,
)
_FIND_PRE_PATH_FLAGS: Final[frozenset[str]] = frozenset(
    {"-H", "-L", "-P", "-X", "-x", "-E", "-s", "-q", "-d"}
)
_FIND_PRE_PATH_VALUE_OPTS: Final[frozenset[str]] = frozenset(
    {"-f", "-D", "-O"}
)
_RG_VALUE_OPTS: Final[frozenset[str]] = frozenset(
    {
        "-e",
        "--regexp",
        "-f",
        "--file",
        "-g",
        "--glob",
        "--iglob",
        "-t",
        "--type",
        "-T",
        "--type-not",
        "--type-add",
        "--type-clear",
        "-A",
        "--after-context",
        "-B",
        "--before-context",
        "-C",
        "--context",
        "-j",
        "--threads",
        "-m",
        "--max-count",
        "-r",
        "--replace",
        "--max-depth",
        "--max-filesize",
        "--max-columns",
        "-d",
        "--dereference-max-depth",
        "--pre",
        "--pre-glob",
        "--encoding",
        "--sort",
        "--sortr",
        "--color",
        "--colors",
        "--engine",
        "--path-separator",
    }
)
_RG_SHORT_VALUE_CHARS: Final[frozenset[str]] = frozenset("efgABCjtmd")

_TIP_BROAD_FIND: Final[str] = (
    "Ne relance pas ce find. Borne-le avec -maxdepth 1..3 sur un sous-dossier précis, "
    "ou utilise l’outil Glob / Grep Cursor."
)
_TIP_BARE_RG: Final[str] = (
    "Ne relance pas ce rg. Utilise `rg PAT .` (ou un sous-dossier), ou l’outil Grep intégré Cursor."
)


def _emit(permission: Decision, user_message: str = "", agent_message: str = "") -> None:
    payload: dict[str, str] = {"permission": permission}
    if user_message:
        payload["user_message"] = user_message
    if agent_message:
        payload["agent_message"] = agent_message
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _emit_allow() -> None:
    _emit("allow")


def _emit_deny(reason: str, command: str = "", tip: str = "") -> None:
    preview = f"\nCommande : `{command}`" if command else ""
    tip_user = f"\n{tip}" if tip else (
        "\nTrop dangereux pour une confirmation agent. Lance-la toi-même hors agent si tu es sûr."
    )
    agent_core = (
        f"Garde-fou DENY : {reason}. N’insiste pas et ne contourne pas. "
        + (
            tip
            if tip
            else (
                "Explique le risque à l’utilisateur ; s’il veut vraiment, "
                "il doit l’exécuter manuellement dans son terminal."
            )
        )
        + (f" Commande bloquée : {command}" if command else "")
    )
    _emit(
        "deny",
        user_message=f"Garde-fou : refusé — {reason}.{preview}{tip_user}",
        agent_message=agent_core,
    )


def _emit_ask(reason: str, command: str) -> None:
    _emit(
        "ask",
        user_message=(
            f"Garde-fou : confirmation requise — {reason}.\n"
            f"Commande : `{command}`\n"
            "Autorise si c’est intentionnel, sinon refuse."
        ),
        agent_message=(
            f"Garde-fou ASK : {reason}. "
            "Dis clairement à l’utilisateur pourquoi cette commande est nécessaire et attends sa décision "
            "(autoriser dans l’UI, ou la lancer lui-même). Ne contourne pas le hook "
            "(ex. Python shutil à la place d’un rm bloqué) sauf s’il te le demande."
            f" Commande : {command}"
        ),
    )


def _home_exact_target(command: str) -> bool:
    """True si la commande cible exactement $HOME ou $HOME/* (pas un sous-dossier)."""
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


def _classify_rm(command: str) -> Decision | None:
    """None = pas un rm récursif pertinent ; sinon deny ou ask."""
    lowered: str = command.lower()
    if not re.search(r"\brm\b", lowered):
        return None
    if _RM_NO_PRESERVE.search(lowered):
        return "deny"
    recursive: bool = bool(_RM_RF_FLAGS.search(lowered) or _RM_RECURSIVE.search(lowered))
    if not recursive:
        return None
    if _RM_CATASTROPHIC_TARGET.search(command) or _home_exact_target(command):
        return "deny"
    return "ask"


def _shell_segments(command: str) -> list[str]:
    return [seg.strip() for seg in _SHELL_SEGMENT_SPLIT.split(command) if seg.strip()]


def _safe_tokenize(segment: str) -> list[str]:
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def _has_bounded_maxdepth(segment: str) -> bool:
    match = _MAXDEPTH_RE.search(segment)
    if not match:
        return False
    try:
        depth = int(match.group(1))
    except ValueError:
        return False
    return 1 <= depth <= 3


def _hang_prone_roots(home: str) -> frozenset[str]:
    roots = {
        "/",
        home,
        os.path.join(home, "Library"),
        "/Applications",
        "/System",
        "/Volumes",
        "/private",
        "/usr",
        "/usr/local",
        "/opt",
        "/opt/homebrew",
    }
    normalized: set[str] = set()
    for root in roots:
        try:
            normalized.add(os.path.realpath(root))
        except OSError:
            normalized.add(os.path.normpath(root))
    return frozenset(normalized)


def _is_hang_prone_path(raw_path: str, cwd: str) -> bool:
    if not raw_path:
        return False
    try:
        home = os.path.realpath(os.path.expanduser("~"))
    except OSError:
        home = os.path.expanduser("~")

    expanded = os.path.expanduser(raw_path)
    # $HOME / ${HOME} littéraux non expandés par expanduser
    expanded = re.sub(
        r"\$\{?HOME\}?",
        home,
        expanded,
        count=1,
    )
    if expanded in ("~",):
        resolved = home
    elif os.path.isabs(expanded):
        try:
            resolved = os.path.realpath(expanded)
        except OSError:
            resolved = os.path.normpath(expanded)
    else:
        base = cwd if cwd else os.getcwd()
        try:
            resolved = os.path.realpath(os.path.join(base, expanded))
        except OSError:
            resolved = os.path.normpath(os.path.join(base, expanded))

    return resolved in _hang_prone_roots(home)


def _find_start_paths(tokens: list[str]) -> list[str]:
    """Extrait les chemins de départ d’un find (défaut « . » si absent)."""
    if not tokens:
        return []
    idx = 0
    while idx < len(tokens) and re.match(r"^\w+=", tokens[idx]):
        idx += 1
    if idx >= len(tokens) or os.path.basename(tokens[idx]) != "find":
        return []
    idx += 1
    paths: list[str] = []
    while idx < len(tokens):
        tok = tokens[idx]
        if tok in _FIND_PRE_PATH_FLAGS:
            idx += 1
            continue
        if tok in _FIND_PRE_PATH_VALUE_OPTS or tok.startswith("-O") or tok.startswith("-D"):
            idx += 1
            if tok in _FIND_PRE_PATH_VALUE_OPTS and idx < len(tokens):
                idx += 1
            continue
        if tok.startswith("-") or tok in ("(", "!", ","):
            break
        paths.append(tok)
        idx += 1
    return paths if paths else ["."]


def _classify_broad_find(command: str, cwd: str = "") -> Decision | None:
    """deny si find sur arbre large sans -maxdepth 1..3 ; None sinon."""
    for segment in _shell_segments(command):
        tokens = _safe_tokenize(segment)
        start_paths = _find_start_paths(tokens)
        if not start_paths:
            continue
        if _has_bounded_maxdepth(segment):
            continue
        for path in start_paths:
            if _is_hang_prone_path(path, cwd):
                return "deny"
    return None


def _rg_consume_option(tokens: list[str], idx: int) -> int:
    """Avance idx après une option rg ; idx pointe sur l’option."""
    tok = tokens[idx]
    if tok == "--":
        return idx
    if tok.startswith("--"):
        name = tok.split("=", 1)[0]
        if "=" in tok:
            return idx + 1
        if name in _RG_VALUE_OPTS:
            nxt = idx + 1
            if nxt < len(tokens) and not tokens[nxt].startswith("-"):
                return nxt + 1
            return nxt
        return idx + 1
    # short options, possibly clustered: -ina, -ePAT, -e PAT
    if len(tok) == 2 and tok in _RG_VALUE_OPTS:
        nxt = idx + 1
        if nxt < len(tokens) and not tokens[nxt].startswith("-"):
            return nxt + 1
        return nxt
    if len(tok) > 2 and tok[1] != "-":
        # -ePAT or -ina
        first = tok[1]
        if first in _RG_SHORT_VALUE_CHARS:
            # attached value already in tok, or needs next arg if exactly -X
            return idx + 1
        return idx + 1
    return idx + 1


def _classify_bare_rg(command: str) -> Decision | None:
    """deny si rg/ripgrep sans opérande chemin après le pattern ; None sinon."""
    for segment in _shell_segments(command):
        tokens = _safe_tokenize(segment)
        if not tokens:
            continue
        idx = 0
        while idx < len(tokens) and re.match(r"^\w+=", tokens[idx]):
            idx += 1
        if idx >= len(tokens):
            continue
        if os.path.basename(tokens[idx]) not in ("rg", "ripgrep"):
            continue
        idx += 1
        pattern_seen = False
        has_path_after = False
        while idx < len(tokens):
            tok = tokens[idx]
            if tok == "--":
                idx += 1
                rest = tokens[idx:]
                if not pattern_seen:
                    if rest:
                        pattern_seen = True
                        rest = rest[1:]
                if pattern_seen and rest:
                    has_path_after = True
                break
            if tok.startswith("-"):
                idx = _rg_consume_option(tokens, idx)
                continue
            if not pattern_seen:
                pattern_seen = True
                idx += 1
                continue
            has_path_after = True
            break
        if pattern_seen and not has_path_after:
            return "deny"
    return None


def _classify_shell(command: str, cwd: str = "") -> tuple[Decision, str, str]:
    """Retourne (decision, reason, tip). tip non vide seulement pour anti-hang deny."""
    stripped: str = command.strip()
    if not stripped:
        return "allow", "", ""

    rm_decision = _classify_rm(stripped)
    if rm_decision == "deny":
        return "deny", "suppression récursive sur une cible système / home entière", ""
    if rm_decision == "ask":
        return "ask", "suppression récursive (rm -r / rm -rf) sur un chemin ciblé", ""

    if _classify_broad_find(stripped, cwd) == "deny":
        return (
            "deny",
            "find non borné sur un arbre large (risque de hang agent)",
            _TIP_BROAD_FIND,
        )
    if _classify_bare_rg(stripped) == "deny":
        return (
            "deny",
            "rg/ripgrep sans chemin explicite (lit stdin → hang)",
            _TIP_BARE_RG,
        )

    lowered: str = stripped.lower()
    for pattern, reason in _DENY_SHELL_PATTERNS:
        if pattern.search(lowered):
            return "deny", reason, ""
    for pattern, reason in _ASK_SHELL_PATTERNS:
        if pattern.search(lowered):
            return "ask", reason, ""
    return "allow", "", ""


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

    # beforeShellExecution : souvent sans tool_name, avec "command"
    if not tool_name or tool_name == "Shell":
        cmd: str = str(data.get("command") or "")
        if not cmd and isinstance(data.get("tool_input"), dict):
            cmd = str(data["tool_input"].get("command") or "")
        if cmd:
            decision, reason, tip = _classify_shell(cmd, cwd)
            if decision == "deny":
                _emit_deny(reason, cmd, tip=tip)
                return 0
            if decision == "ask":
                _emit_ask(reason, cmd)
                return 0
        if not tool_name:
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
                f"modification/suppression d’un chemin critique « {resolved or raw_path} »",
                resolved or raw_path,
            )
            return 0

    _emit_allow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
