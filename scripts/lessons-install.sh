#!/usr/bin/env bash
set -euo pipefail
canon="$HOME/Documents/config-cursor/tasks/lessons.md"
cd "$HOME/Documents/config-cursor" && git pull
synced=0
while IFS= read -r -d '' target; do
  [[ "$target" == "$canon" ]] && continue
  cp "$canon" "$target"
  echo "synced → $target"
  synced=1
done < <(find "$HOME/Documents" -type f -path '*/tasks/lessons.md' -print0)
[[ "$synced" -eq 1 ]] || echo "aucun projet à sync (hors canon)"
