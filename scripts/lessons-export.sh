#!/usr/bin/env bash
set -euo pipefail
canon="$HOME/Documents/config-cursor/tasks/lessons.md"
src="$(pwd)/tasks/lessons.md"
[[ -f "$src" ]] || { echo "Pas de tasks/lessons.md ici"; exit 1; }
cp "$src" "$canon"
cd "$HOME/Documents/config-cursor"
git add tasks/lessons.md
git commit -m "update lessons.md" || { echo "Rien à committer"; exit 0; }
git push