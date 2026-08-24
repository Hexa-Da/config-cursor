#!/usr/bin/env python3
"""Estimate always-on vs on-demand token overhead for the Cursor harness."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HOME = Path.home()
CURSOR = HOME / ".cursor"
# Canonical source for Cursor User Rules in this harness (UI copy is not on disk).
CONFIG = Path(os.environ.get("CURSOR_CONFIG_REPO", HOME / "Documents" / "config-cursor"))
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
AT_RE = re.compile(r"@([^\s]+)")
SKIP_DIR = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".tox",
}
SKILL_ROOT_NAMES = (".cursor", ".agents", ".claude", ".codex")


def tokens(text: str, code: bool = False) -> int:
    if not text:
        return 0
    if code:
        return max(1, len(text) // 4)
    return max(1, int(len(text.split()) * 1.3))


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def parse_fm(text: str) -> tuple[dict[str, str], str]:
    match = FM_RE.match(text)
    if not match:
        return {}, text
    fields: dict[str, str] = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" not in line or line.lstrip().startswith("#"):
            i += 1
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value in {">", ">-", "|", "|-"} or value.startswith(">"):
            block: list[str] = []
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i][0].isspace()):
                block.append(lines[i].strip())
                i += 1
            fields[key] = " ".join(p for p in block if p)
            continue
        fields[key] = value.strip("\"'")
        i += 1
    return fields, text[match.end() :]


def row(name: str, path: Path | None, tok: int, bucket: str, *, exists: bool | None = None, lines: int = 0) -> dict:
    present = path.is_file() if path and exists is None else bool(exists)
    return {
        "name": name,
        "path": str(path) if path else "",
        "exists": present,
        "tokens": tok if present else 0,
        "bucket": bucket,
        "lines": lines if present else 0,
    }


def skipped(path: Path) -> bool:
    return any(part in SKIP_DIR for part in path.parts)


def walk_named(root: Path, filename: str):
    if not root.is_dir():
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
        if filename in filenames:
            yield Path(dirpath) / filename


def iter_mdc(rules_root: Path):
    if not rules_root.is_dir():
        return
    for dirpath, dirnames, filenames in os.walk(rules_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
        for name in sorted(filenames):
            if name.endswith(".mdc"):
                yield Path(dirpath) / name


def truthy(value: str) -> bool:
    return value.strip().strip("\"'").lower() == "true"


def attached_paths(workspace: Path, body: str) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()
    for raw in AT_RE.findall(body):
        rel = raw.split("#", 1)[0].rstrip(".,;:)")
        if not rel or rel.startswith(("http://", "https://")):
            continue
        candidate = (workspace / rel).resolve()
        try:
            candidate.relative_to(workspace.resolve())
        except ValueError:
            continue
        if candidate in seen or not candidate.is_file():
            continue
        seen.add(candidate)
        found.append(candidate)
    return found


def skill_rows(root: Path, *, catalog_always: bool, include_body: bool = True) -> list[dict]:
    rows: list[dict] = []
    if not root.is_dir():
        return rows
    for skill_md in sorted(walk_named(root, "SKILL.md")):
        text = read(skill_md)
        fields, body = parse_fm(text)
        disabled = truthy(fields.get("disable-model-invocation", ""))
        desc = fields.get("description", "")
        fm_tok = tokens(fields.get("name", "") + " " + desc)
        in_catalog = catalog_always or not disabled
        if in_catalog and fm_tok:
            rows.append(
                {
                    "name": f"skill:{skill_md.parent.name} frontmatter",
                    "path": str(skill_md),
                    "exists": True,
                    "tokens": fm_tok,
                    "bucket": "always-on",
                    "lines": 0,
                }
            )
        if not include_body:
            continue
        body_tok = tokens(body)
        for extra in skill_md.parent.glob("*.md"):
            if extra.name != "SKILL.md" and extra.is_file():
                body_tok += tokens(read(extra))
        rows.append(
            {
                "name": f"skill:{skill_md.parent.name} body",
                "path": str(skill_md.parent),
                "exists": True,
                "tokens": body_tok,
                "bucket": "on-demand",
                "lines": len(body.splitlines()),
            }
        )
    return rows


def workspace_skill_roots(workspace: Path) -> list[Path]:
    roots: list[Path] = []
    seen: set[Path] = set()
    for vendor in SKILL_ROOT_NAMES:
        direct = workspace / vendor / "skills"
        if direct.is_dir():
            resolved = direct.resolve()
            if resolved not in seen:
                seen.add(resolved)
                roots.append(direct)
    for skill_md in walk_named(workspace, "SKILL.md"):
        parent = skill_md.parent.parent
        if parent.name != "skills" or parent.parent.name not in SKILL_ROOT_NAMES:
            continue
        resolved = parent.resolve()
        if resolved not in seen:
            seen.add(resolved)
            roots.append(parent)
    return roots


def mcp_tokens(*paths: Path) -> tuple[int, Path | None, int]:
    servers: set[str] = set()
    used: Path | None = None
    for path in paths:
        raw = read(path)
        if not raw:
            continue
        used = path
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return tokens(raw, code=True), path, 0
        block = data.get("mcpServers") or data.get("mcp") or {}
        if isinstance(block, dict):
            servers.update(block)
    n = len(servers)
    # Schema overhead ~500 tokens per tool; without a live tool list, count
    # servers × 4 tools as a conservative placeholder.
    return n * 4 * 500, used, n


def main() -> int:
    workspace = Path(sys.argv[1] if len(sys.argv) > 1 else os.getcwd()).resolve()
    rows: list[dict] = []
    counted: set[Path] = set()

    def add_file(name: str, path: Path, bucket: str, *, code: bool = False) -> None:
        resolved = path.resolve() if path.exists() else path
        if resolved in counted:
            return
        text = read(path)
        if path.is_file():
            counted.add(resolved)
        rows.append(
            row(name, path, tokens(text, code=code), bucket, lines=len(text.splitlines()) if text else 0)
        )

    # Canon AGENTS.md = source versionnée des User Rules Cursor (UI) et miroir
    # OpenCode (~/.config/opencode/AGENTS.md via install.sh). Même contenu,
    # runtimes différents — compter une seule fois pour un audit Cursor.
    canon_agents = CONFIG / "AGENTS.md"
    workspace_agents = workspace / "AGENTS.md"
    if canon_agents.is_file():
        add_file("user-rules (canon AGENTS.md)", canon_agents, "always-on")
    elif workspace_agents.is_file():
        add_file("user-rules (workspace AGENTS.md)", workspace_agents, "always-on")
    if (
        workspace_agents.is_file()
        and canon_agents.is_file()
        and workspace_agents.resolve() != canon_agents.resolve()
    ):
        add_file("AGENTS.md (workspace, ≠ canon)", workspace_agents, "always-on")

    add_file("CLAUDE.md", workspace / "CLAUDE.md", "always-on")
    add_file(".cursorrules", workspace / ".cursorrules", "always-on")

    for nested in walk_named(workspace, "AGENTS.md"):
        if nested.resolve() == workspace_agents.resolve():
            continue
        add_file(f"AGENTS.md:{nested.parent.name}", nested, "on-demand")

    for rule in iter_mdc(workspace / ".cursor" / "rules"):
        text = read(rule)
        fields, body = parse_fm(text)
        always = truthy(fields.get("alwaysApply", ""))
        bucket = "always-on" if always else "on-demand"
        add_file(f"rule:{rule.relative_to(workspace / '.cursor' / 'rules')}", rule, bucket)
        if always:
            for attached in attached_paths(workspace, body):
                add_file(f"attached:{attached.relative_to(workspace)}", attached, "always-on")

    mcp_tok, mcp_path, mcp_n = mcp_tokens(CURSOR / "mcp.json", workspace / ".cursor" / "mcp.json")
    rows.append(
        row(
            f"mcp.json ({mcp_n} servers × 4 tools × 500)",
            mcp_path or CURSOR / "mcp.json",
            mcp_tok,
            "always-on",
            exists=bool(mcp_tok) or (CURSOR / "mcp.json").is_file() or (workspace / ".cursor" / "mcp.json").is_file(),
        )
    )

    rows.extend(skill_rows(CURSOR / "skills", catalog_always=False))
    rows.extend(skill_rows(HOME / ".agents" / "skills", catalog_always=False))
    rows.extend(skill_rows(CURSOR / "skills-cursor", catalog_always=True, include_body=False))
    for root in workspace_skill_roots(workspace):
        rows.extend(skill_rows(root, catalog_always=False))

    for name, path in (
        ("CONVENTIONS.md", workspace / "memoire" / "CONVENTIONS.md"),
        ("ARCHITECTURE.md", workspace / "memoire" / "ARCHITECTURE.md"),
    ):
        add_file(name, path, "on-demand")

    present = [r for r in rows if r["exists"] and r["tokens"] > 0]
    always = sum(r["tokens"] for r in present if r["bucket"] == "always-on")
    demand = sum(r["tokens"] for r in present if r["bucket"] == "on-demand")

    print(f"workspace: {workspace}")
    print(f"always-on:  ~{always} tokens")
    print(f"on-demand:  ~{demand} tokens (if fully loaded)")
    print()
    print(f"{'tokens':>8}  {'bucket':<12}  {'lines':>5}  name")
    print("-" * 72)
    for r in sorted(present, key=lambda x: -x["tokens"]):
        flag = ""
        if r["bucket"] == "always-on" and r["lines"] > 100 and "skill:" not in r["name"]:
            flag = "  FLAG >100 lines"
        if "skill:" in r["name"] and "body" in r["name"] and r["lines"] > 400:
            flag = "  FLAG >400 lines"
        print(f"{r['tokens']:>8}  {r['bucket']:<12}  {r['lines']:>5}  {r['name']}{flag}")
        print(f"{'':>8}  {r['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
