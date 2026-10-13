#!/usr/bin/env python3
"""Garde-fou sécurité pour le hook jcode `pre_tool`.

Réutilise la classification de garde-fou.py (même dossier).
Contrat jcode : exit 0 = autorisé, exit 2 = bloqué (stderr renvoyé au modèle).
jcode n'a pas de "ask" : les cas ask sont bloqués avec un message demandant
à l'agent de obtenir l'accord explicite de l'utilisateur.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

_TIP_JCODE: str = (
    "Borne la commande (sous-dossier précis, -maxdepth 1..3, `rg PAT .`) "
    "ou utilise l'outil agentgrep."
)
_SHELL_TOOLS: frozenset[str] = frozenset({"bash"})
_WRITE_TOOLS: frozenset[str] = frozenset(
    {"write", "edit", "multiedit", "apply_patch", "replace"}
)


def _load_base() -> Any:
    here: Path = Path(__file__).resolve()
    path: Path = here.with_name("garde-fou.py")
    if not path.is_file():
        # Exécution depuis le repo : la source vit dans dotcursor/hooks/
        path = here.parents[2] / "dotcursor" / "hooks" / "garde-fou.py"
    spec = importlib.util.spec_from_file_location("garde_fou_base", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"garde-fou.py introuvable : {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _block(message: str) -> int:
    sys.stderr.write(message + "\n")
    return 2


def main() -> int:
    tool: str = os.environ.get("JCODE_HOOK_TOOL_NAME", "")
    cwd: str = os.environ.get("JCODE_HOOK_CWD", "")
    try:
        tool_input: Any = json.load(sys.stdin)
    except json.JSONDecodeError:
        tool_input = {}
    if not isinstance(tool_input, dict):
        tool_input = {}

    base = _load_base()

    if tool in _SHELL_TOOLS:
        command: str = str(tool_input.get("command") or "")
        decision, reason, tip = base._classify_shell(command, cwd)
        if decision == "deny":
            advice: str = _TIP_JCODE if tip else (
                "N'insiste pas et ne contourne pas. Explique le risque à l'utilisateur ; "
                "s'il veut vraiment, il doit l'exécuter lui-même dans son terminal."
            )
            return _block(f"Garde-fou DENY : {reason}. {advice} Commande : {command}")
        if decision == "ask":
            return _block(
                f"Garde-fou ASK : {reason}. Explique à l'utilisateur pourquoi cette commande "
                "est nécessaire et attends son accord explicite avant de relancer "
                "(ou demande-lui de la lancer lui-même). Ne contourne pas le hook. "
                f"Commande : {command}"
            )
        return 0

    if tool in _WRITE_TOOLS:
        home: str = os.path.expanduser("~")
        paths: list[str] = [
            p for p in os.environ.get("JCODE_HOOK_TOUCHED_PATHS", "").splitlines() if p
        ]
        raw: str = base._extract_tool_path(tool_input)
        if raw:
            paths.append(raw)
        for raw_path in paths:
            resolved: str = base._resolve_path(raw_path, cwd)
            if base._is_critical_path(resolved, home):
                return _block(
                    "Garde-fou DENY : modification d'un chemin critique "
                    f"« {resolved or raw_path} ». N'insiste pas ; "
                    "l'utilisateur doit le faire lui-même."
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
