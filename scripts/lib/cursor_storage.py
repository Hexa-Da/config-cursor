#!/usr/bin/env python3
"""Export/import a filtered Cursor state.vscdb allowlist → user/cursor-storage.json."""
from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA = 1

APPLICATION_USER_KEY = (
    "src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl"
    ".persistentStorage.applicationUser"
)

CURSOR_KEYS_AGENTS: frozenset[str] = frozenset(
    {
        "autoRunBugbotOnCommit",
        "bugbotDeepReviewDefault",
        "bugbotIncludeSubmodules",
        "bugbotIncludeUntrackedFiles",
        "reviewControlLocation",
        "autoFormatOnAgentFinish",
        "sandboxAutoRunSettingEnabled",
        "attributeCommitsToAgent",
        "attributePRsToAgent",
        "subagentModelOverrides",
        "chatSubmitOnCmdEnter",
        "composerAutocompleteHeuristicsEnabled",
    }
)

CURSOR_KEYS_LAYOUT: frozenset[str] = frozenset(
    {
        "unifiedAppLayout",
        "autoHideEditorWhenEmpty",
        "agentLayout.sidebarLocationAgentOverride",
        "agentLayout.quickMenu.lastSelectedLayoutId",
        "userOpenAgentsWindowOnStartupPreference",
        "noTitlebarLayout.visibility",
        "userWindowRestorationPreference",
    }
)

CURSOR_KEYS: frozenset[str] = CURSOR_KEYS_AGENTS | CURSOR_KEYS_LAYOUT

COMPOSER_STATE_KEYS: frozenset[str] = frozenset(
    {
        "autoApproveModeTransitions",
        "autoApprovedModeTransitions",
        "autoRejectedModeTransitions",
        "autoAcceptWebSearchTool",
        "autoAcceptGenerateImageTool",
        "webFetchDomainAllowlist",
        "enableSmartAuto",
        "mcpAuthBlocking",
        "autoApplyFilesOutsideContext",
        "yoloEnableRunEverything",
        "yoloOutsideWorkspaceDisabled",
        "yoloDeleteFileDisabled",
        "yoloMcpToolsDisabled",
        "yoloCommandAllowlist",
        "yoloCommandDenylist",
        "codeBlockDisplayPreference",
        "maxOpenTabsMode",
        "maxOpenTabsCustomValue",
        "thinkingLevel",
        "modes4",
    }
)

MODES4_IDS: frozenset[str] = frozenset({"agent", "plan", "chat", "debug"})
# Tuple (not frozenset): insertion order must be stable across Python processes
# so export JSON does not churn key order in modes4 on every run.
MODES4_FIELDS: tuple[str, ...] = (
    "autoRun",
    "fullAutoRun",
    "autoFix",
    "smartModeAutoRun",
)

META_NOTE = (
    "Filtered Agents/Review + Layout prefs from state.vscdb. "
    "Not glass/session sizes. Quit Cursor before install.sh for this layer."
)


def _decode_item_value(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def _encode_item_value(value: Any) -> str:
    if isinstance(value, str):
        # Cursor stores plain strings without JSON quotes for some keys
        # (e.g. reviewControlLocation). Re-encode JSON for non-strings;
        # keep strings as-is if they look like simple tokens.
        try:
            json.loads(value)
            return value
        except json.JSONDecodeError:
            return value
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _slim_modes4(modes: Any) -> list[dict[str, Any]]:
    if not isinstance(modes, list):
        return []
    out: list[dict[str, Any]] = []
    for mode in modes:
        if not isinstance(mode, dict):
            continue
        mid = mode.get("id")
        if mid not in MODES4_IDS:
            continue
        slim: dict[str, Any] = {"id": mid}
        for field in MODES4_FIELDS:
            if field in mode:
                slim[field] = mode[field]
        out.append(slim)
    return out


def _merge_modes4(existing: Any, incoming: Any) -> list[dict[str, Any]]:
    base: list[dict[str, Any]] = list(existing) if isinstance(existing, list) else []
    by_id: dict[str, dict[str, Any]] = {
        m["id"]: dict(m)
        for m in base
        if isinstance(m, dict) and isinstance(m.get("id"), str)
    }
    incoming_list = incoming if isinstance(incoming, list) else []
    for mode in incoming_list:
        if not isinstance(mode, dict):
            continue
        mid = mode.get("id")
        if mid not in MODES4_IDS:
            continue
        current = by_id.get(mid, {"id": mid})
        for field in MODES4_FIELDS:
            if field in mode:
                current[field] = mode[field]
        by_id[mid] = current
    # Preserve original order for known modes, append new at end
    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    for m in base:
        if isinstance(m, dict) and m.get("id") in by_id:
            mid = m["id"]
            ordered.append(by_id[mid])
            seen.add(mid)
    for mid, m in by_id.items():
        if mid not in seen:
            ordered.append(m)
    return ordered


def export_storage(db_path: Path, out_path: Path) -> int:
    if not db_path.is_file():
        print(f"→ cursor-storage: skip export (DB absente: {db_path})")
        return 0

    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        cur = con.cursor()
        cursor_out: dict[str, Any] = {}
        for key in sorted(CURSOR_KEYS):
            full = f"cursor/{key}"
            cur.execute("SELECT value FROM ItemTable WHERE key=?", (full,))
            row = cur.fetchone()
            if row is None:
                continue
            cursor_out[key] = _decode_item_value(row[0])

        composer_out: dict[str, Any] = {}
        cur.execute("SELECT value FROM ItemTable WHERE key=?", (APPLICATION_USER_KEY,))
        row = cur.fetchone()
        if row is not None:
            try:
                app_user = json.loads(row[0])
            except json.JSONDecodeError:
                app_user = {}
            cs = app_user.get("composerState") if isinstance(app_user, dict) else None
            if isinstance(cs, dict):
                for key in sorted(COMPOSER_STATE_KEYS):
                    if key not in cs:
                        continue
                    if key == "modes4":
                        composer_out[key] = _slim_modes4(cs[key])
                    else:
                        composer_out[key] = cs[key]
    finally:
        con.close()

    payload = {
        "_meta": {"schema": SCHEMA, "note": META_NOTE},
        "cursor": cursor_out,
        "composerState": composer_out,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"→ cursor-storage.json "
        f"({len(cursor_out)} cursor keys, {len(composer_out)} composerState keys)"
    )
    return 0


def import_storage(in_path: Path, db_path: Path) -> int:
    if not in_path.is_file():
        print(f"→ cursor-storage: skip import (fichier absent: {in_path})")
        return 0
    if not db_path.is_file():
        print(f"→ cursor-storage: skip import (DB absente: {db_path})")
        return 0

    try:
        data = json.loads(in_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"→ cursor-storage: JSON invalide ({exc})", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("→ cursor-storage: racine JSON doit être un objet", file=sys.stderr)
        return 1

    schema = (data.get("_meta") or {}).get("schema") if isinstance(data.get("_meta"), dict) else None
    if schema is not None and schema != SCHEMA:
        print(
            f"→ cursor-storage: schema {schema} non supporté (attendu {SCHEMA})",
            file=sys.stderr,
        )
        return 1

    cursor_in = data.get("cursor") if isinstance(data.get("cursor"), dict) else {}
    composer_in = (
        data.get("composerState") if isinstance(data.get("composerState"), dict) else {}
    )

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = db_path.with_name(f"{db_path.name}.bak-{stamp}")
    shutil.copy2(db_path, backup)
    print(f"→ cursor-storage: backup {backup.name}")

    con = sqlite3.connect(str(db_path))
    try:
        cur = con.cursor()
        n_cursor = 0
        for key, value in cursor_in.items():
            if key not in CURSOR_KEYS:
                continue
            full = f"cursor/{key}"
            encoded = _encode_item_value(value)
            cur.execute(
                "INSERT INTO ItemTable (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (full, encoded),
            )
            n_cursor += 1

        n_composer = 0
        cur.execute("SELECT value FROM ItemTable WHERE key=?", (APPLICATION_USER_KEY,))
        row = cur.fetchone()
        if row is None:
            if composer_in:
                print(
                    "→ cursor-storage: warning — blob applicationUser absent, "
                    "composerState non appliqué"
                )
        else:
            try:
                app_user = json.loads(row[0])
            except json.JSONDecodeError:
                app_user = {}
            if not isinstance(app_user, dict):
                app_user = {}
            cs = app_user.get("composerState")
            if not isinstance(cs, dict):
                cs = {}
            for key, value in composer_in.items():
                if key not in COMPOSER_STATE_KEYS:
                    continue
                if key == "modes4":
                    cs[key] = _merge_modes4(cs.get("modes4"), value)
                else:
                    cs[key] = value
                n_composer += 1
            app_user["composerState"] = cs
            cur.execute(
                "UPDATE ItemTable SET value=? WHERE key=?",
                (
                    json.dumps(app_user, ensure_ascii=False, separators=(",", ":")),
                    APPLICATION_USER_KEY,
                ),
            )

        con.commit()
    finally:
        con.close()

    print(f"→ cursor-storage: importé ({n_cursor} cursor, {n_composer} composerState)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_export = sub.add_parser("export", help="state.vscdb → cursor-storage.json")
    p_export.add_argument("db", type=Path)
    p_export.add_argument("out", type=Path)

    p_import = sub.add_parser("import", help="cursor-storage.json → state.vscdb")
    p_import.add_argument("inp", type=Path)
    p_import.add_argument("db", type=Path)

    args = parser.parse_args(argv)
    if args.cmd == "export":
        return export_storage(args.db, args.out)
    if args.cmd == "import":
        return import_storage(args.inp, args.db)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
