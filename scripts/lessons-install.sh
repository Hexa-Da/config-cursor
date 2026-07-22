#!/usr/bin/env bash
set -euo pipefail
canon="$HOME/Documents/config-cursor/tasks/lessons.md"
cd "$HOME/Documents/config-cursor" && git pull
find "$HOME/Documents" -type f -path '*/tasks/lessons.md' -print0 |
while IFS= read -r -d '' target; do
  cp "$canon" "$target"
  echo "synced → $target"
done