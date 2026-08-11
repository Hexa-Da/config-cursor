#!/usr/bin/env bash
# Canon bootstrap §1–3 → tous les projets sous ~/Documents (extras §4+ préservés).
set -euo pipefail

root="$HOME/Documents/config-cursor"
canon="$root/bootstrap/bootstrap-canonical.mdc"
lib="$root/scripts/lib/bootstrap_annexes.py"

cd "$root" && git pull
[[ -f "$canon" ]] || { echo "Pas de canon : $canon"; exit 1; }

synced=0
while IFS= read -r -d '' target; do
  python3 "$lib" install "$canon" "$target"
  synced=1
done < <(find "$HOME/Documents" -type f -path '*/.cursor/rules/bootstrap.mdc' -print0)

[[ "$synced" -eq 1 ]] || echo "aucun projet à sync"
