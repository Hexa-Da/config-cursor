#!/usr/bin/env python3
"""Fetch a GitLab MR and optional discussion thread via glab. Prints markdown."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Any
from urllib.parse import unquote, urlparse

URL_RE = re.compile(
    r"""
    https?://(?P<host>[^/]+)/
    (?P<project>.+?)/-/merge_requests/(?P<iid>\d+)
    (?:\#note_(?P<note>\d+))?
    """,
    re.VERBOSE,
)


def die(msg: str, code: int = 1) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(code)


def run(args: list[str]) -> str:
    try:
        proc = subprocess.run(args, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        die("glab introuvable dans PATH")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        die(f"{' '.join(args)}\n{err}")
    return proc.stdout


def parse_target(raw: str) -> dict[str, str | None]:
    text = raw.strip().strip("'\"")
    match = URL_RE.search(text)
    if match:
        project = unquote(match.group("project")).strip("/")
        return {
            "host": match.group("host"),
            "project": project,
            "iid": match.group("iid"),
            "note": match.group("note"),
        }
    if re.fullmatch(r"\d+", text):
        return {"host": None, "project": None, "iid": text, "note": None}
    die(f"cible invalide (URL MR ou iid) : {raw}")


def git_branch() -> str | None:
    proc = subprocess.run(
        ["git", "branch", "--show-current"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def mr_json(iid: str, project: str | None) -> dict[str, Any]:
    cmd = ["glab", "mr", "view", iid, "-F", "json"]
    if project:
        cmd.extend(["-R", project])
    return json.loads(run(cmd))


def discussions(
    iid: str, project: str | None, host: str | None
) -> list[dict[str, Any]]:
    if project:
        encoded = project.replace("/", "%2F")
        endpoint = f"projects/{encoded}/merge_requests/{iid}/discussions"
    else:
        endpoint = f"projects/:id/merge_requests/{iid}/discussions"
    cmd = ["glab", "api", "--paginate", endpoint]
    if host:
        cmd.extend(["--hostname", host])
    data = json.loads(run(cmd))
    if not isinstance(data, list):
        die("discussions : JSON inattendu (pas une liste)")
    return data


def note_preview(body: str, limit: int = 400) -> str:
    text = (body or "").strip().replace("\r\n", "\n")
    if len(text) > limit:
        return text[: limit].rstrip() + "…"
    return text


def position_label(note: dict[str, Any]) -> str:
    pos = note.get("position") or {}
    path = pos.get("new_path") or pos.get("old_path") or ""
    line = pos.get("new_line") or pos.get("old_line")
    if path and line:
        return f"{path}:{line}"
    return path or "—"


def author_name(note: dict[str, Any]) -> str:
    author = note.get("author") or {}
    return str(author.get("username") or author.get("name") or "?")


def find_thread(
    discs: list[dict[str, Any]], note_id: int
) -> dict[str, Any] | None:
    for disc in discs:
        for note in disc.get("notes") or []:
            if note.get("id") == note_id:
                return disc
    return None


def is_diff_or_discussion(note: dict[str, Any]) -> bool:
    if note.get("system"):
        return False
    return bool(note.get("type") in {"DiffNote", "DiscussionNote"} or note.get("resolvable"))


def unresolved_notes(discs: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    out: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for disc in discs:
        for note in disc.get("notes") or []:
            if not is_diff_or_discussion(note):
                continue
            if note.get("resolved") is True:
                continue
            if note.get("resolvable") and note.get("resolved") is not True:
                out.append((disc, note))
                break
            if note.get("type") in {"DiffNote", "DiscussionNote"} and not note.get(
                "resolved"
            ):
                out.append((disc, note))
                break
    return out


def print_note(note: dict[str, Any], *, full: bool) -> None:
    nid = note.get("id")
    resolved = note.get("resolved")
    resolvable = note.get("resolvable")
    print(f"- id: `{nid}`  author: @{author_name(note)}  {position_label(note)}")
    print(f"  resolvable: {resolvable}  resolved: {resolved}  type: {note.get('type')}")
    body = note.get("body") or ""
    print("  " + (body if full else note_preview(body)).replace("\n", "\n  "))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="URL merge_requests/…[#note_N] ou iid")
    parser.add_argument("--note", type=int, default=None, help="id de note (surcharge le #note_ de l’URL)")
    parser.add_argument("--json", action="store_true", help="dump JSON compact (mr + thread/unresolved)")
    args = parser.parse_args()

    parsed = parse_target(args.target)
    iid = str(parsed["iid"])
    project = parsed["project"]
    host = parsed["host"]
    note_id = args.note or (int(parsed["note"]) if parsed["note"] else None)

    mr = mr_json(iid, project)
    discs = discussions(iid, project, host)
    head = git_branch()
    source = mr.get("source_branch") or ""
    mismatch = bool(head and source and head != source)

    if args.json:
        payload: dict[str, Any] = {
            "mr": {
                "iid": mr.get("iid"),
                "title": mr.get("title"),
                "state": mr.get("state"),
                "source_branch": source,
                "target_branch": mr.get("target_branch"),
                "web_url": mr.get("web_url"),
                "head": head,
                "head_mismatch": mismatch,
            },
            "note_id": note_id,
        }
        if note_id is not None:
            thread = find_thread(discs, note_id)
            payload["thread"] = thread
            payload["note_found"] = thread is not None
        else:
            payload["unresolved"] = [
                {"discussion_id": d.get("id"), "note": n}
                for d, n in unresolved_notes(discs)
            ]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    title = mr.get("title") or ""
    print(f"# MR {mr.get('iid')} — {title}")
    print(f"- state: {mr.get('state')}  draft: {mr.get('draft')}")
    print(f"- source: `{source}`  → target: `{mr.get('target_branch')}`")
    if mismatch:
        print(f"- HEAD: `{head}`  **≠ source_branch** (ne pas checkout sans accord)")
    elif head:
        print(f"- HEAD: `{head}` (aligné)")
    print(f"- url: {mr.get('web_url')}")
    print()

    if note_id is not None:
        thread = find_thread(discs, note_id)
        if not thread:
            print(f"## Note `{note_id}` introuvable dans les discussions")
            print("Ne pas appeler `GET …/notes/{id}`. Vérifier iid / projet.")
            print()
        else:
            notes = thread.get("notes") or []
            print(f"## Note `{note_id}` — fil ({len(notes)} message(s))")
            for note in notes:
                marker = " ← cible" if note.get("id") == note_id else ""
                print(f"### note `{note.get('id')}`{marker}")
                print_note(note, full=True)
                print()
            return

    open_notes = unresolved_notes(discs)
    print(f"## Discussions non résolues ({len(open_notes)})")
    if not open_notes:
        print("(aucune)")
        return
    for _disc, note in open_notes:
        print(f"### note `{note.get('id')}`")
        print_note(note, full=False)
        print()


if __name__ == "__main__":
    main()
