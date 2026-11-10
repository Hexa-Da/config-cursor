#!/usr/bin/env python3
"""Write init-project rule canons into ~/Documents harness projects.

Always syncs (no dry-run). Exit 1 if any file is still not IDENTIQUE after write.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HOME = Path.home()
DOCUMENTS = Path(os.environ.get("HARNESS_DOCUMENTS", HOME / "Documents"))
CONFIG = Path(os.environ.get("CURSOR_CONFIG_REPO", DOCUMENTS / "config-cursor"))

CANON_KEYS = (
    ("bootstrap.mdc", "Copie bootstrap.mdc"),
    ("context-mode.mdc", "Copie context-mode.mdc"),
    ("ponytail.mdc", "Copie ponytail.mdc"),
)


def _skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _reference_path() -> Path:
    sibling = _skill_dir().parent / "init-project" / "reference.md"
    if sibling.is_file():
        return sibling
    fallback = CONFIG / "dotcursor" / "skills" / "init-project" / "reference.md"
    if fallback.is_file():
        return fallback
    raise SystemExit(f"reference.md introuvable (essayé {sibling} et {fallback})")


def extract_canons(reference: Path) -> dict[str, str]:
    text = reference.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for filename, heading in CANON_KEYS:
        pat = rf"## {re.escape(heading)}\n.*?```(?:\w*)\n(.*?)```"
        m = re.search(pat, text, re.S)
        if not m:
            raise SystemExit(f"Section manquante dans {reference}: ## {heading}")
        body = m.group(1)
        if not body.endswith("\n"):
            body += "\n"
        out[filename] = body
    return out


def harness_projects(root: Path) -> list[Path]:
    if not root.is_dir():
        raise SystemExit(f"Documents introuvable: {root}")
    projects: list[Path] = []
    for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if (
            (child / "memoire").is_dir()
            and (child / "tasks").is_dir()
            and (child / ".cursor" / "rules").is_dir()
        ):
            projects.append(child)
    return projects


def norm(s: str) -> str:
    return s if s.endswith("\n") else s + "\n"


def is_identical(path: Path, canon: str) -> bool:
    if not path.is_file():
        return False
    return norm(path.read_text(encoding="utf-8")) == norm(canon)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--documents",
        type=Path,
        default=DOCUMENTS,
        help="Racine des projets (défaut: ~/Documents)",
    )
    args = parser.parse_args()

    reference = _reference_path()
    canons = extract_canons(reference)
    projects = harness_projects(args.documents)

    print(f"source: {reference}")
    print(f"documents: {args.documents}")
    print(f"projets harness: {len(projects)}")
    print()
    print("| Projet | Fichier | Action |")
    print("| ------ | ------- | ------ |")

    wrote = 0
    skipped = 0
    for project in projects:
        rules = project / ".cursor" / "rules"
        for filename, canon in canons.items():
            path = rules / filename
            body = norm(canon)
            if is_identical(path, body):
                skipped += 1
                print(f"| `{project.name}` | `{filename}` | SKIPPED |")
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            wrote += 1
            print(f"| `{project.name}` | `{filename}` | WROTE |")

    bad = 0
    for project in projects:
        rules = project / ".cursor" / "rules"
        for filename, canon in canons.items():
            if not is_identical(rules / filename, canon):
                bad += 1
                print(f"FAIL: {project.name}/{filename}", file=sys.stderr)

    print()
    print(f"SKIPPED={skipped} WROTE={wrote}")
    if bad:
        print(f"FAIL after sync: {bad}", file=sys.stderr)
        return 1
    print("OK: tous les canons rules sont IDENTIQUES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
