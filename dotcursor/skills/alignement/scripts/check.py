#!/usr/bin/env python3
"""Check config-cursor repo vs this machine. Exit 1 if unexpected drift."""
from __future__ import annotations

import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

HOME = Path.home()
CONFIG = Path(os.environ.get("CURSOR_CONFIG_REPO", HOME / "Documents" / "config-cursor"))
CURSOR = HOME / ".cursor"
SKIP_DIR = {"__pycache__", ".git"}
SKIP_NAMES = {".DS_Store", ".gitkeep"}
SKIP_SUFFIX = {".pyc", ".pyo"}


def _opencode_config() -> Path:
    if os.environ.get("OPENCODE_CONFIG_DIR"):
        return Path(os.environ["OPENCODE_CONFIG_DIR"])
    if os.environ.get("XDG_CONFIG_HOME"):
        return Path(os.environ["XDG_CONFIG_HOME"]) / "opencode"
    return HOME / ".config" / "opencode"


def _cursor_user() -> Path:
    system = os.uname().sysname
    if system == "Darwin":
        return HOME / "Library" / "Application Support" / "Cursor" / "User"
    if system == "Linux":
        return HOME / ".config" / "Cursor" / "User"
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "Cursor" / "User"
    return HOME / ".config" / "Cursor" / "User"


OPENCODE = _opencode_config()
CURSOR_USER = _cursor_user()
LIB = CONFIG / "scripts" / "lib"


def _load_libs() -> tuple:
    if str(LIB) not in sys.path:
        sys.path.insert(0, str(LIB))
    from cursor_storage import export_storage  # type: ignore  # noqa: PLC0415
    from sync_opencode_skills import cursor_skill_md_to_opencode  # type: ignore  # noqa: PLC0415

    return export_storage, cursor_skill_md_to_opencode


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []  # status, name, detail

    def ok(self, name: str, detail: str = "") -> None:
        self.rows.append(("OK", name, detail))

    def drift(self, name: str, detail: str) -> None:
        self.rows.append(("DRIFT", name, detail))

    def info(self, name: str, detail: str) -> None:
        self.rows.append(("INFO", name, detail))

    def skip(self, name: str, detail: str) -> None:
        self.rows.append(("SKIP", name, detail))

    @property
    def drifted(self) -> bool:
        return any(s == "DRIFT" for s, _, _ in self.rows)


def _files(root: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    if not root.is_dir():
        return out
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR for part in path.parts):
            continue
        if path.name in SKIP_NAMES or path.suffix in SKIP_SUFFIX:
            continue
        out[str(path.relative_to(root))] = path
    return out


def _cmp_files(a: Path, b: Path) -> bool:
    return a.is_file() and b.is_file() and filecmp.cmp(a, b, shallow=False)


def _dir_diff(repo_dir: Path, machine_dir: Path) -> list[str]:
    left, right = _files(repo_dir), _files(machine_dir)
    notes: list[str] = []
    for rel in sorted(set(left) - set(right)):
        notes.append(f"manquant machine: {rel}")
    for rel in sorted(set(right) - set(left)):
        notes.append(f"surplus machine: {rel}")
    for rel in sorted(set(left) & set(right)):
        if not filecmp.cmp(left[rel], right[rel], shallow=False):
            notes.append(f"contenu: {rel}")
    return notes


def _git(rep: Report) -> None:
    if not (CONFIG / ".git").exists():
        rep.skip("git", f"pas un repo: {CONFIG}")
        return

    def git(*args: str) -> str:
        return subprocess.check_output(["git", "-C", str(CONFIG), *args], text=True).strip()

    head = git("rev-parse", "--short", "HEAD")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    status = git("status", "--porcelain")
    try:
        origin = git("rev-parse", "--short", "@{upstream}")
        ahead = git("rev-list", "--count", "@{upstream}..HEAD")
        behind = git("rev-list", "--count", "HEAD..@{upstream}")
    except subprocess.CalledProcessError:
        origin, ahead, behind = "", "0", "0"

    bits = [f"{branch} {head}"]
    if origin:
        bits.append(f"upstream {origin}")
        if ahead != "0":
            bits.append(f"ahead {ahead}")
        if behind != "0":
            bits.append(f"behind {behind}")
        if ahead == "0" and behind == "0":
            bits.append("= upstream")
    else:
        bits.append("pas d'upstream")
    if status:
        n = len([ln for ln in status.splitlines() if ln.strip()])
        bits.append(f"worktree sale ({n})")
        rep.info("git", " · ".join(bits))
    elif behind != "0":
        rep.drift("git", " · ".join(bits) + " → git pull")
    else:
        rep.ok("git", " · ".join(bits))


def _hooks(rep: Report) -> None:
    notes: list[str] = []
    src, dst = CONFIG / "dotcursor", CURSOR
    for rel in ("hooks.json", "hooks/garde-fou.py"):
        a, b = src / rel, dst / rel
        if not a.is_file() and not b.is_file():
            continue
        if not _cmp_files(a, b):
            notes.append(rel)
    if notes:
        rep.drift("hooks", ", ".join(notes) + " → install.sh")
    else:
        rep.ok("hooks")


def _dot_dir(rep: Report, name: str) -> None:
    notes = _dir_diff(CONFIG / "dotcursor" / name, CURSOR / name)
    if notes:
        rep.drift(f"{name} Cursor", "; ".join(notes) + " → install.sh")
    else:
        rep.ok(f"{name} Cursor")


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _settings(rep: Report) -> None:
    repo = _load_json(CONFIG / "user" / "settings.json")
    machine = _load_json(CURSOR_USER / "settings.json")
    if repo is None and machine is None:
        rep.skip("settings.json", "absent des deux côtés")
        return
    if not isinstance(repo, dict) or not isinstance(machine, dict):
        rep.drift("settings.json", "un côté absent ou non-objet → export.sh / install.sh")
        return
    machine_f = {k: v for k, v in machine.items() if not str(k).startswith("remote.SSH")}
    if machine_f == repo:
        extra = sorted(set(machine) - set(machine_f))
        detail = f"remote.SSH machine-only: {', '.join(extra)}" if extra else ""
        rep.ok("settings.json", detail)
        return
    bits: list[str] = []
    only_m = sorted(set(machine_f) - set(repo))
    only_r = sorted(set(repo) - set(machine_f))
    if only_m:
        bits.append(f"only machine: {', '.join(only_m)} → export.sh")
    if only_r:
        bits.append(f"only repo: {', '.join(only_r)} → install.sh")
    for key in sorted(set(machine_f) & set(repo)):
        if machine_f[key] != repo[key]:
            bits.append(f"changed {key}")
    rep.drift("settings.json", "; ".join(bits) or "diff")


def _keybindings(rep: Report) -> None:
    a = CONFIG / "user" / "keybindings.json"
    b = CURSOR_USER / "keybindings.json"
    if not a.is_file() and not b.is_file():
        rep.skip("keybindings.json", "absent")
        return
    if _cmp_files(a, b):
        rep.ok("keybindings.json")
    else:
        hint = " → export.sh (machine) ou install.sh (repo)"
        rep.drift("keybindings.json", "contenu différent" + hint)


def _storage(rep: Report, export_storage) -> None:
    db = CURSOR_USER / "globalStorage" / "state.vscdb"
    repo = CONFIG / "user" / "cursor-storage.json"
    if not db.is_file():
        rep.skip("cursor-storage", f"DB absente: {db}")
        return
    if not repo.is_file():
        rep.skip("cursor-storage", "pas de cursor-storage.json dans le repo")
        return
    fd, tmp_name = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        with redirect_stdout(StringIO()):
            export_storage(db, tmp)
        live = json.loads(tmp.read_text(encoding="utf-8"))
        expected = json.loads(repo.read_text(encoding="utf-8"))
        live.pop("_meta", None)
        expected.pop("_meta", None)
        if live == expected:
            rep.ok("cursor-storage")
        else:
            hint = " → export.sh (machine) ou install.sh après quit Cursor"
            rep.drift("cursor-storage", "extrait state.vscdb ≠ repo" + hint)
    finally:
        tmp.unlink(missing_ok=True)


def _opencode_agents(rep: Report) -> None:
    a = CONFIG / "AGENTS.md"
    b = OPENCODE / "AGENTS.md"
    if not a.is_file():
        rep.skip("OpenCode AGENTS.md", "absent du repo")
        return
    if _cmp_files(a, b):
        rep.ok("OpenCode AGENTS.md")
    else:
        rep.drift("OpenCode AGENTS.md", "≠ repo → install.sh")


def _opencode_skills(rep: Report, cursor_skill_md_to_opencode) -> None:
    src = CONFIG / "dotcursor" / "skills"
    dst = OPENCODE / "skills"
    if not src.is_dir():
        rep.skip("OpenCode skills", "pas de dotcursor/skills")
        return
    src_names = {p.name for p in src.iterdir() if p.is_dir()}
    dst_names = {p.name for p in dst.iterdir() if p.is_dir()} if dst.is_dir() else set()
    notes: list[str] = []
    missing = sorted(src_names - dst_names)
    extra = sorted(dst_names - src_names)
    if missing:
        notes.append("manquant: " + ", ".join(missing))
    if extra:
        rep.info("OpenCode skills extra", ", ".join(extra) + " (non touchés par install.sh)")
    for name in sorted(src_names & dst_names):
        sdir, ddir = src / name, dst / name
        sfiles = _files(sdir)
        dfiles = _files(ddir)
        for rel in sorted(set(sfiles) - set(dfiles)):
            notes.append(f"{name}/{rel} manquant")
        for rel in sorted(set(sfiles) & set(dfiles)):
            stext = sfiles[rel].read_text(encoding="utf-8")
            dtext = dfiles[rel].read_text(encoding="utf-8")
            if Path(rel).name == "SKILL.md":
                try:
                    expected = cursor_skill_md_to_opencode(stext)
                except ValueError as exc:
                    notes.append(f"{name}/{rel}: transform {exc}")
                    continue
                if expected != dtext:
                    notes.append(f"{name}/{rel} (transform)")
            elif stext != dtext:
                notes.append(f"{name}/{rel}")
    if notes:
        rep.drift("OpenCode skills", "; ".join(notes) + " → install.sh")
    else:
        rep.ok("OpenCode skills")


def _lessons(rep: Report) -> None:
    canon = CONFIG / "tasks" / "lessons.md"
    if not canon.is_file():
        rep.skip("lessons.md", "pas de canon")
        return
    try:
        raw = subprocess.check_output(
            ["find", str(HOME / "Documents"), "-type", "f", "-path", "*/tasks/lessons.md"],
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        rep.skip("lessons.md", str(exc))
        return
    drifted: list[str] = []
    n = 0
    for line in raw.splitlines():
        path = Path(line)
        if path.resolve() == canon.resolve():
            continue
        n += 1
        if not filecmp.cmp(canon, path, shallow=False):
            drifted.append(str(path))
    if drifted:
        rep.drift("lessons.md", f"{len(drifted)} copie(s) ≠ canon → lessons-install.sh")
        for path in drifted:
            rep.info("lessons copie", path)
    else:
        extra = f" ({n} projet(s))" if n else " (aucun projet hors canon)"
        rep.ok("lessons.md", extra.strip())


def _snapshots(rep: Report) -> None:
    canon = CONFIG / "tasks" / "lessons.md"
    patch = LIB / "patch_lessons_snapshot.sh"
    dests = [
        OPENCODE / "skills" / "init-project" / "reference.md",
        CURSOR / "skills" / "init-project" / "reference.md",
        CONFIG / "dotcursor" / "skills" / "init-project" / "reference.md",
    ]
    if not patch.is_file() or not canon.is_file():
        rep.skip("snapshots init-project", "script ou canon absent")
        return
    stale: list[str] = []
    for dest in dests:
        if not dest.is_file():
            stale.append(f"absent: {dest}")
            continue
        fd, tmp_name = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        tmp = Path(tmp_name)
        try:
            shutil.copy2(dest, tmp)
            proc = subprocess.run(
                [str(patch), str(canon), str(tmp)],
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                stale.append(f"{dest}: patch fail")
            elif not filecmp.cmp(dest, tmp, shallow=False):
                stale.append(str(dest))
        finally:
            tmp.unlink(missing_ok=True)
    if stale:
        rep.drift("snapshots init-project", "; ".join(stale) + " → lessons-install.sh")
    else:
        rep.ok("snapshots init-project")


def _extensions(rep: Report) -> None:
    ext_json = CURSOR / "extensions" / "extensions.json"
    listing = CONFIG / "extensions.txt"
    if not ext_json.is_file() or not listing.is_file():
        rep.skip("extensions", "fichier absent")
        return
    data = json.loads(ext_json.read_text(encoding="utf-8"))
    live = sorted(
        {
            (e.get("identifier") or {}).get("id")
            for e in data
            if (e.get("identifier") or {}).get("id")
        }
    )
    repo = sorted(
        ln.strip()
        for ln in listing.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    )
    only_live = sorted(set(live) - set(repo))
    only_repo = sorted(set(repo) - set(live))
    if not only_live and not only_repo:
        rep.ok("extensions", f"{len(live)} ids")
        return
    bits: list[str] = []
    if only_live:
        bits.append("machine + " + ", ".join(only_live))
    if only_repo:
        bits.append("repo + " + ", ".join(only_repo))
    rep.info("extensions", "; ".join(bits) + " (liste indicative)")


def _cursor_running() -> bool:
    try:
        comm = subprocess.check_output(["ps", "-axo", "comm="], text=True)
    except OSError:
        return False
    for line in comm.splitlines():
        s = line.strip()
        if s in {"cursor", "Cursor"}:
            return True
        if s.endswith("/usr/share/cursor/cursor"):
            return True
        if s.endswith("Cursor.app/Contents/MacOS/Cursor"):
            return True
    return False


def main() -> int:
    if not CONFIG.is_dir():
        print(f"✗ repo introuvable: {CONFIG}", file=sys.stderr)
        return 2

    export_storage, cursor_skill_md_to_opencode = _load_libs()
    rep = Report()
    _git(rep)
    _hooks(rep)
    _dot_dir(rep, "skills")
    _dot_dir(rep, "commands")
    _dot_dir(rep, "agents")
    _settings(rep)
    _keybindings(rep)
    _storage(rep, export_storage)
    _opencode_agents(rep)
    _opencode_skills(rep, cursor_skill_md_to_opencode)
    _lessons(rep)
    _snapshots(rep)
    _extensions(rep)
    if _cursor_running():
        rep.info("Cursor", "ouvert — install.sh skipperait cursor-storage")

    print(f"Alignement  {CONFIG}")
    print("═" * 40)
    width = max(len(name) for _, name, _ in rep.rows) if rep.rows else 8
    for status, name, detail in rep.rows:
        line = f"{status:<5}  {name:<{width}}"
        if detail:
            line += f"  {detail}"
        print(line)
    print()
    if rep.drifted:
        print("Résultat: écarts inattendus  (install.sh = repo→machine, export.sh = machine→repo)")
        return 1
    print("Résultat: aligné")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
