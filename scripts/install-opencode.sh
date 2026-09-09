#!/usr/bin/env bash
# Install OpenCode-only config: AGENTS.md + skills (frontmatter adapted).
# Does not touch Cursor hooks/settings/storage. Project opencode.jsonc = init-project-opencode.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOT_SRC="$ROOT/dotcursor"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# OpenCode uses XDG-style paths on every OS (including Windows):
#   OPENCODE_CONFIG_DIR > XDG_CONFIG_HOME/opencode > ~/.config/opencode
detect_opencode_config_dir() {
  if [[ -n "${OPENCODE_CONFIG_DIR:-}" ]]; then
    echo "$OPENCODE_CONFIG_DIR"
  elif [[ -n "${XDG_CONFIG_HOME:-}" ]]; then
    echo "$XDG_CONFIG_HOME/opencode"
  else
    echo "$HOME/.config/opencode"
  fi
}

OPENCODE_CONFIG="$(detect_opencode_config_dir)"
echo "→ OpenCode : $OPENCODE_CONFIG"

if ! command -v python3 >/dev/null 2>&1; then
  echo "✗ python3 requis pour sync_opencode_skills.py" >&2
  exit 1
fi

mkdir -p "$OPENCODE_CONFIG"

# Skills: miroir exact de dotcursor/skills, frontmatter adapté
# (description une ligne + compatibility: opencode). Orphelins côté
# OpenCode retirés (prune), comme rsync --delete pour ~/.cursor/skills.
if [[ -d "$DOT_SRC/skills" ]]; then
  python3 "$SCRIPT_DIR/lib/sync_opencode_skills.py" \
    "$DOT_SRC/skills" "$OPENCODE_CONFIG/skills"
else
  echo "→ OpenCode skills: skip (pas de $DOT_SRC/skills)"
fi

# AGENTS.md (= user rules) : miroir depuis la racine du repo
if [[ -f "$ROOT/AGENTS.md" ]]; then
  cp "$ROOT/AGENTS.md" "$OPENCODE_CONFIG/AGENTS.md"
  echo "→ OpenCode AGENTS.md"
else
  echo "→ OpenCode AGENTS.md: skip (absent du repo)"
fi

echo "OK — Skills → $OPENCODE_CONFIG/skills ; AGENTS.md → $OPENCODE_CONFIG/AGENTS.md"
echo "     Câblage projet (opencode.jsonc) : skill init-project-opencode, pas ce script."
