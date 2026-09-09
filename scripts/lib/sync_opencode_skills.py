#!/usr/bin/env python3
"""Sync portable Cursor skills → OpenCode skills, adapting SKILL.md frontmatter.

Source of truth for skill *bodies* is dotcursor/skills/. Only the YAML frontmatter
is rewritten for OpenCode:

  Cursor  : description (optionally folded) + disable-model-invocation: true
  OpenCode: description (single line) + compatibility: opencode

Other files (reference.md, …) are copied as-is. Destination dirs absent from the
source are pruned (exact mirror of the repo skills tree).
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


def flatten_description(raw: str) -> str:
    """Turn a YAML description value (plain or >- / | folded) into one line."""
    text = raw.strip()
    if text.startswith(">-") or text.startswith(">") or text.startswith("|"):
        # Drop the block indicator line; keep indented content.
        lines = text.splitlines()
        body_lines: list[str] = []
        for line in lines[1:]:
            body_lines.append(line.strip())
        text = " ".join(part for part in body_lines if part)
    else:
        # Plain / quoted scalar — strip surrounding quotes if present.
        if (text.startswith('"') and text.endswith('"')) or (
            text.startswith("'") and text.endswith("'")
        ):
            text = text[1:-1]
        text = " ".join(text.split())
    return text.strip()


def parse_simple_frontmatter(fm: str) -> dict[str, str]:
    """Parse the flat skill frontmatter we author (name / description / flags)."""
    data: dict[str, str] = {}
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # Folded / literal block scalar.
        if value in {">", ">-", ">|", "|", "|-", "|+"} or value.startswith(">"):
            block = [value]
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt and not nxt[0].isspace() and ":" in nxt:
                    break
                block.append(nxt)
                i += 1
            data[key] = "\n".join(block)
            continue
        data[key] = value
        i += 1
    return data


def cursor_skill_md_to_opencode(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text
    fields = parse_simple_frontmatter(match.group(1))
    name = fields.get("name", "").strip()
    description = flatten_description(fields.get("description", ""))
    if not name or not description:
        raise ValueError("SKILL.md frontmatter must include name and description")

    new_fm = (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "compatibility: opencode\n"
        "---\n"
    )
    body = text[match.end() :]
    if body and not body.startswith("\n"):
        # Keep a single blank line after frontmatter when body starts immediately.
        pass
    return new_fm + body


def sync_skill(src_skill: Path, dst_skill: Path) -> None:
    if dst_skill.exists():
        shutil.rmtree(dst_skill)
    shutil.copytree(
        src_skill,
        dst_skill,
        ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", ".gitkeep"),
    )
    skill_md = dst_skill / "SKILL.md"
    if skill_md.is_file():
        original = skill_md.read_text(encoding="utf-8")
        skill_md.write_text(cursor_skill_md_to_opencode(original), encoding="utf-8")


def _skill_dirs_with_content(root: Path) -> list[Path]:
    """Non-empty skill directories under root (ignore .DS_Store / .gitkeep only)."""
    out: list[Path] = []
    for path in sorted(p for p in root.iterdir() if p.is_dir()):
        real = [
            p
            for p in path.rglob("*")
            if p.is_file() and p.name not in {".DS_Store", ".gitkeep"}
        ]
        if real:
            out.append(path)
    return out


def prune_skills(src_root: Path, dst_root: Path) -> list[str]:
    """Remove destination skill dirs that are not present (with content) in src."""
    if not dst_root.is_dir():
        return []
    keep = {p.name for p in _skill_dirs_with_content(src_root)}
    pruned: list[str] = []
    for dst_skill in sorted(p for p in dst_root.iterdir() if p.is_dir()):
        if dst_skill.name in keep:
            continue
        shutil.rmtree(dst_skill)
        pruned.append(dst_skill.name)
    return pruned


def sync_skills(src_root: Path, dst_root: Path) -> tuple[list[str], list[str]]:
    if not src_root.is_dir():
        raise FileNotFoundError(f"source skills dir missing: {src_root}")
    dst_root.mkdir(parents=True, exist_ok=True)
    synced: list[str] = []
    for src_skill in _skill_dirs_with_content(src_root):
        sync_skill(src_skill, dst_root / src_skill.name)
        synced.append(src_skill.name)
    pruned = prune_skills(src_root, dst_root)
    return synced, pruned


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src", type=Path, help="dotcursor/skills directory")
    parser.add_argument("dst", type=Path, help="OpenCode skills directory")
    args = parser.parse_args(argv)

    try:
        synced, pruned = sync_skills(args.src, args.dst)
    except Exception as exc:  # noqa: BLE001 — CLI boundary
        print(f"✗ opencode skills: {exc}", file=sys.stderr)
        return 1

    if synced:
        print(f"→ OpenCode skills: {', '.join(synced)} → {args.dst}")
    else:
        print(f"→ OpenCode skills: rien à sync ({args.src})")
    if pruned:
        print(f"→ OpenCode skills pruned: {', '.join(pruned)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
