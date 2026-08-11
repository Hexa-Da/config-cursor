#!/usr/bin/env python3
"""Merge bootstrap.mdc canon (§1–3) into project files; sync init-project/reference.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ANNEXES_HEADER = "## Annexes `memoire/` — lecture sur condition, jamais par défaut"
CANON_ITEMS = (1, 2, 3)
ITEM_RE = re.compile(r"^(\d+)\.\s")


def split_bootstrap(content: str) -> tuple[str, dict[int, str]]:
    if ANNEXES_HEADER not in content:
        raise ValueError(f"Section « {ANNEXES_HEADER} » introuvable")
    header, rest = content.split(ANNEXES_HEADER, 1)
    header = header + ANNEXES_HEADER
    items = _parse_numbered_items(rest.strip())
    if not items:
        raise ValueError("Aucune règle numérotée sous la section Annexes")
    return header, items


def _parse_numbered_items(text: str) -> dict[int, str]:
    items: dict[int, str] = {}
    current_num: int | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_num, current_lines
        if current_num is not None:
            items[current_num] = "\n".join(current_lines).strip()
        current_num = None
        current_lines = []

    for line in text.splitlines():
        match = ITEM_RE.match(line)
        if match:
            flush()
            current_num = int(match.group(1))
            current_lines = [line]
        elif current_num is not None:
            current_lines.append(line)
    flush()
    return items


def _build_annexes_section(items: dict[int, str], nums: list[int]) -> str:
    missing = [n for n in nums if n not in items]
    if missing:
        raise ValueError(f"Règles manquantes : {missing}")
    return "\n".join(items[n] for n in nums) + "\n"


def build_bootstrap(header: str, items: dict[int, str], nums: list[int]) -> str:
    body = _build_annexes_section(items, nums)
    return header.rstrip() + "\n\n" + body.rstrip() + "\n"


def merge_bootstrap(canon_path: Path, target_path: Path) -> None:
    canon_header, canon_items = split_bootstrap(canon_path.read_text(encoding="utf-8"))
    _, target_items = split_bootstrap(target_path.read_text(encoding="utf-8"))

    merged = {n: canon_items[n] for n in CANON_ITEMS}
    for num, text in target_items.items():
        if num >= 4:
            merged[num] = text

    target_path.write_text(
        build_bootstrap(canon_header, merged, sorted(merged)),
        encoding="utf-8",
    )


def export_canon(source_path: Path, canon_path: Path, ref_path: Path) -> None:
    _, source_items = split_bootstrap(source_path.read_text(encoding="utf-8"))
    missing = [n for n in CANON_ITEMS if n not in source_items]
    if missing:
        raise ValueError(f"bootstrap source incomplet — règles {missing} absentes")

    canon_header, _ = split_bootstrap(canon_path.read_text(encoding="utf-8"))
    canon_path.write_text(
        build_bootstrap(canon_header, source_items, list(CANON_ITEMS)),
        encoding="utf-8",
    )
    update_reference(ref_path, canon_path)
    print(f"→ canon : {canon_path}")
    print(f"→ reference.md mis à jour ({ref_path})")


def update_reference(ref_path: Path, canon_path: Path) -> None:
    body = canon_path.read_text(encoding="utf-8")
    ref = ref_path.read_text(encoding="utf-8")
    marker = "## Copie bootstrap.mdc"
    start = ref.find(marker)
    if start == -1:
        raise ValueError("Bloc « ## Copie bootstrap.mdc » introuvable dans reference.md")

    fence_open = ref.find("```\n", start)
    if fence_open == -1:
        raise ValueError("Fence ``` introuvable sous ## Copie bootstrap.mdc")
    content_start = fence_open + 4

    fence_close = ref.find("\n```", content_start)
    if fence_close == -1:
        raise ValueError("Fence fermant ``` introuvable")

    updated = ref[:content_start] + body.rstrip("\n") + ref[fence_close:]
    ref_path.write_text(updated, encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "Usage:\n"
            "  bootstrap_annexes.py export <source.mdc> <canon.mdc> <reference.md>\n"
            "  bootstrap_annexes.py install <canon.mdc> <target.mdc>",
            file=sys.stderr,
        )
        return 2

    cmd = argv[1]
    try:
        if cmd == "export":
            if len(argv) != 5:
                raise ValueError("export attend 3 chemins : source canon reference")
            export_canon(Path(argv[2]), Path(argv[3]), Path(argv[4]))
        elif cmd == "install":
            if len(argv) != 4:
                raise ValueError("install attend 2 chemins : canon target")
            merge_bootstrap(Path(argv[2]), Path(argv[3]))
            print(f"synced → {argv[3]}")
        else:
            raise ValueError(f"commande inconnue : {cmd}")
    except (ValueError, OSError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
