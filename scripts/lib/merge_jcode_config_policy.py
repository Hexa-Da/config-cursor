#!/usr/bin/env python3
"""Merge dotjcode/config.policy.toml keys into ~/.jcode/config.toml.

Only keys present in the policy file are written. Everything else in the
machine config (display, auth, providers, …) is left untouched. Comments and
ordering outside touched keys are preserved via line-oriented edits.
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path


_SECTION_RE = re.compile(r"^\[([^\]]+)\]\s*$")
_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+)\s*=")


def _toml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    raise TypeError(f"unsupported policy value type: {type(value).__name__}")


def _flatten_policy(policy: dict) -> dict[str, dict[str, object]]:
    """Return {section: {key: value}} for top-level tables with scalar values."""
    out: dict[str, dict[str, object]] = {}
    for section, body in policy.items():
        if not isinstance(body, dict):
            raise SystemExit(
                f"policy: top-level key [{section}] must be a table, got {type(body).__name__}"
            )
        keys: dict[str, object] = {}
        for key, value in body.items():
            if isinstance(value, dict):
                raise SystemExit(
                    f"policy: nested tables not supported ([{section}.{key}])"
                )
            keys[key] = value
        if keys:
            out[str(section)] = keys
    return out


def _find_section_span(lines: list[str], section: str) -> tuple[int, int] | None:
    """Return [start, end) line indices for `section`, or None if absent."""
    start: int | None = None
    for i, line in enumerate(lines):
        m = _SECTION_RE.match(line.strip())
        if not m:
            continue
        name = m.group(1)
        if start is not None:
            return (start, i)
        if name == section:
            start = i
    if start is None:
        return None
    return (start, len(lines))


def _upsert_keys_in_section(
    lines: list[str], section: str, keys: dict[str, object]
) -> list[str]:
    span = _find_section_span(lines, section)
    if span is None:
        # Append a blank line if file non-empty and doesn't end with one.
        out = list(lines)
        if out and out[-1].strip() != "":
            out.append("")
        out.append(f"[{section}]")
        for key, value in keys.items():
            out.append(f"{key} = {_toml_scalar(value)}")
        out.append("")
        return out

    start, end = span
    section_lines = lines[start:end]
    remaining = dict(keys)
    new_section: list[str] = [section_lines[0]]  # header

    for line in section_lines[1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_section.append(line)
            continue
        m = _KEY_RE.match(stripped)
        if not m:
            new_section.append(line)
            continue
        key = m.group(1)
        if key in remaining:
            new_section.append(f"{key} = {_toml_scalar(remaining.pop(key))}")
        else:
            new_section.append(line)

    # Insert missing keys before trailing blank lines at end of section.
    insert_at = len(new_section)
    while insert_at > 1 and new_section[insert_at - 1].strip() == "":
        insert_at -= 1
    for key, value in remaining.items():
        new_section.insert(insert_at, f"{key} = {_toml_scalar(value)}")
        insert_at += 1

    return lines[:start] + new_section + lines[end:]


def merge_policy(machine_text: str, policy: dict[str, dict[str, object]]) -> str:
    lines = machine_text.splitlines()
    # Preserve a final newline if the source had one / always end with one.
    for section, keys in policy.items():
        lines = _upsert_keys_in_section(lines, section, keys)
    text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path, help="path to config.policy.toml")
    parser.add_argument("machine", type=Path, help="path to ~/.jcode/config.toml")
    args = parser.parse_args(argv)

    if not args.policy.is_file():
        print(f"✗ policy absent: {args.policy}", file=sys.stderr)
        return 1

    with args.policy.open("rb") as f:
        raw_policy = tomllib.load(f)
    policy = _flatten_policy(raw_policy)
    if not policy:
        print("→ jcode config.policy: empty, skip")
        return 0

    if args.machine.is_file():
        machine_text = args.machine.read_text(encoding="utf-8")
    else:
        machine_text = ""
        args.machine.parent.mkdir(parents=True, exist_ok=True)

    merged = merge_policy(machine_text, policy)
    tmp = args.machine.with_suffix(args.machine.suffix + ".tmp")
    tmp.write_text(merged, encoding="utf-8")
    tmp.replace(args.machine)
    keys = ", ".join(
        f"{sec}.{k}" for sec, body in policy.items() for k in body
    )
    print(f"→ jcode config.toml: merged policy ({keys})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
