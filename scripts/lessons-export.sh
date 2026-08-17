#!/usr/bin/env bash
# Export tasks/lessons.md du projet courant → canon config-cursor
# (+ sync du snapshot embarqué dans init-project/reference.md).
set -euo pipefail

root="$HOME/Documents/config-cursor"
canon="$root/tasks/lessons.md"
ref="$root/dotcursor/skills/init-project/reference.md"
src="$(pwd)/tasks/lessons.md"

[[ -f "$src" ]] || { echo "Pas de tasks/lessons.md ici"; exit 1; }
[[ -f "$ref" ]] || { echo "Pas de reference.md: $ref"; exit 1; }

cp "$src" "$canon"

# Remplace le corps du fence ```markdown sous "## Copie lessons"
"$root/scripts/lib/patch_lessons_snapshot.sh" "$canon" "$ref"

cd "$root"
git add tasks/lessons.md dotcursor/skills/init-project/reference.md
git commit -m "update lessons.md" || { echo "Rien à committer"; exit 0; }
git push
