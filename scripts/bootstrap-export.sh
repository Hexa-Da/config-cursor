#!/usr/bin/env bash
# Export bootstrap.mdc §1–3 du projet courant → canon config-cursor
# (+ sync du snapshot embarqué dans init-project/reference.md).
set -euo pipefail

root="$HOME/Documents/config-cursor"
canon="$root/bootstrap/bootstrap-canonical.mdc"
ref="$root/dotcursor/skills/init-project/reference.md"
src="$(pwd)/.cursor/rules/bootstrap.mdc"
lib="$root/scripts/lib/bootstrap_annexes.py"

[[ -f "$src" ]] || { echo "Pas de .cursor/rules/bootstrap.mdc ici"; exit 1; }
[[ -f "$canon" ]] || { echo "Pas de canon : $canon"; exit 1; }
[[ -f "$ref" ]] || { echo "Pas de reference.md : $ref"; exit 1; }

python3 "$lib" export "$src" "$canon" "$ref"

cd "$root"
git add bootstrap/bootstrap-canonical.mdc dotcursor/skills/init-project/reference.md
git commit -m "update bootstrap annexes (§1–3)" || { echo "Rien à committer"; exit 0; }
git push
