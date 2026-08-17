#!/usr/bin/env bash
set -euo pipefail

root="$HOME/Documents/config-cursor"
canon="$root/tasks/lessons.md"
patch="$root/scripts/lib/patch_lessons_snapshot.sh"

detect_opencode_config_dir() {
  if [[ -n "${OPENCODE_CONFIG_DIR:-}" ]]; then
    echo "$OPENCODE_CONFIG_DIR"
  elif [[ -n "${XDG_CONFIG_HOME:-}" ]]; then
    echo "$XDG_CONFIG_HOME/opencode"
  else
    echo "$HOME/.config/opencode"
  fi
}

cd "$root" && git pull

synced=0
while IFS= read -r -d '' target; do
  [[ "$target" == "$canon" ]] && continue
  cp "$canon" "$target"
  echo "synced → $target"
  synced=1
done < <(find "$HOME/Documents" -type f -path '*/tasks/lessons.md' -print0)
[[ "$synced" -eq 1 ]] || echo "aucun projet à sync (hors canon)"

# Snapshot lessons dans les skills déjà installés — évite un install.sh
# juste pour recaler init-project/reference.md.
sync_installed_snapshot() {
  local dest="$1"
  if [[ ! -f "$dest" ]]; then
    echo "skip snapshot (absent): $dest"
    return 0
  fi
  "$patch" "$canon" "$dest"
}

sync_installed_snapshot "$(detect_opencode_config_dir)/skills/init-project/reference.md"
sync_installed_snapshot "$HOME/.cursor/skills/init-project/reference.md"
