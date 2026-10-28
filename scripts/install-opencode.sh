#!/usr/bin/env bash
# Install OpenCode-only config: AGENTS.md (depuis dotopencode/) + skills (frontmatter adapted)
# + plugin garde-fou (auto-load ~/.config/opencode/plugins/).
# Does not touch Cursor hooks/settings/storage. Project opencode.jsonc = init-project-opencode.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOT_SRC="$ROOT/dotcursor"
DOT_OC="$ROOT/dotopencode"
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

# AGENTS.md (= user rules) : variante OpenCode de dotopencode/
if [[ -f "$DOT_OC/AGENTS.md" ]]; then
  cp "$DOT_OC/AGENTS.md" "$OPENCODE_CONFIG/AGENTS.md"
  echo "→ OpenCode AGENTS.md"
else
  echo "→ OpenCode AGENTS.md: skip (absent du repo)"
fi

# Garde-fou : plugin auto-load + scripts Python côte-à-côte (base Cursor + wrapper).
# Pas de config.toml à éditer (contrairement à jcode pre_tool).
mkdir -p "$OPENCODE_CONFIG/plugins"
cp "$DOT_OC/plugins/garde-fou.js" \
  "$DOT_OC/plugins/garde-fou-opencode.py" \
  "$DOT_SRC/hooks/garde-fou.py" \
  "$OPENCODE_CONFIG/plugins/"
chmod +x "$OPENCODE_CONFIG/plugins/garde-fou.py" \
  "$OPENCODE_CONFIG/plugins/garde-fou-opencode.py"
echo "→ OpenCode plugins: garde-fou"

echo "OK — Skills → $OPENCODE_CONFIG/skills ; AGENTS.md → $OPENCODE_CONFIG/AGENTS.md"
echo "     Garde-fou → $OPENCODE_CONFIG/plugins/garde-fou.js (+ .py)"
echo "     Câblage projet (opencode.jsonc) : skill init-project-opencode, pas ce script."
