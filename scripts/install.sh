#!/usr/bin/env bash
# Install this Cursor config onto the current machine (macOS / Linux / Windows+Git Bash).
# Also mirrors portable skills into OpenCode (frontmatter adapted).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOT_SRC="$ROOT/dotcursor"
USER_SRC="$ROOT/user"

detect_user_dir() {
  case "$(uname -s)" in
    Darwin)
      echo "$HOME/Library/Application Support/Cursor/User"
      ;;
    Linux)
      echo "$HOME/.config/Cursor/User"
      ;;
    MINGW*|MSYS*|CYGWIN*|Windows_NT)
      echo "${APPDATA:-}/Cursor/User"
      ;;
    *)
      echo "OS non supporté: $(uname -s)" >&2
      exit 1
      ;;
  esac
}

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

CURSOR_USER="$(detect_user_dir)"
CURSOR_DOT="$HOME/.cursor"
OPENCODE_CONFIG="$(detect_opencode_config_dir)"

echo "→ User dir : $CURSOR_USER"
echo "→ Dotcursor: $CURSOR_DOT"
echo "→ OpenCode : $OPENCODE_CONFIG"

mkdir -p "$CURSOR_DOT/hooks" "$CURSOR_USER"

# ~/.cursor (hooks, skills, plugins, commands, agents)
# — ne pas écraser mcp.json s'il existe déjà
cp "$DOT_SRC/hooks.json" "$CURSOR_DOT/hooks.json"
cp "$DOT_SRC/hooks/garde-fou.py" "$CURSOR_DOT/hooks/garde-fou.py"
chmod +x "$CURSOR_DOT/hooks/garde-fou.py" 2>/dev/null || true

# Miroir exact du repo : --delete retire le surplus local (ex. skills orphelins).
sync_dot_dir() {
  local name="$1"
  if [[ -d "$DOT_SRC/$name" ]]; then
    mkdir -p "$CURSOR_DOT/$name"
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --delete --exclude '.DS_Store' --exclude '.gitkeep' "$DOT_SRC/$name/" "$CURSOR_DOT/$name/"
    else
      rm -rf "$CURSOR_DOT/$name"
      mkdir -p "$CURSOR_DOT/$name"
      cp -R "$DOT_SRC/$name/." "$CURSOR_DOT/$name/"
    fi
  fi
}

sync_dot_dir skills
sync_dot_dir plugins
sync_dot_dir commands
sync_dot_dir agents

# OpenCode skills: même contenu que dotcursor/skills, frontmatter adapté
# (description une ligne + compatibility: opencode). Skills OpenCode-only
# hors du repo ne sont pas effacés.
if [[ -d "$DOT_SRC/skills" ]]; then
  python3 "$ROOT/scripts/lib/sync_opencode_skills.py" \
    "$DOT_SRC/skills" "$OPENCODE_CONFIG/skills"
fi

# OpenCode AGENTS.md (= user rules) : install-only, ne pas écraser s'il existe.
# Source repo à la racine (aussi utilisée comme Cursor User Rules).
if [[ -f "$ROOT/AGENTS.md" ]]; then
  mkdir -p "$OPENCODE_CONFIG"
  if [[ ! -f "$OPENCODE_CONFIG/AGENTS.md" ]]; then
    cp "$ROOT/AGENTS.md" "$OPENCODE_CONFIG/AGENTS.md"
    echo "→ OpenCode AGENTS.md créé"
  else
    echo "→ OpenCode AGENTS.md: déjà présent — skip (pas d'écrasement)"
  fi
fi

if [[ ! -f "$CURSOR_DOT/mcp.json" && -f "$DOT_SRC/mcp.json.example" ]]; then
  cp "$DOT_SRC/mcp.json.example" "$CURSOR_DOT/mcp.json"
  echo "→ mcp.json créé depuis l'exemple (vide)"
fi

[[ -f "$USER_SRC/settings.json" ]] && cp "$USER_SRC/settings.json" "$CURSOR_USER/settings.json"
[[ -f "$USER_SRC/keybindings.json" ]] && cp "$USER_SRC/keybindings.json" "$CURSOR_USER/keybindings.json"

# Agents/Review + Layout (state.vscdb) — skip si Cursor tourne (sinon overwrite au quit)
STATE_DB="$CURSOR_USER/globalStorage/state.vscdb"
STORAGE_JSON="$USER_SRC/cursor-storage.json"
cursor_running=0
# Prefer ps (reliable on macOS Electron); fall back to pgrep.
if ps -axo comm= 2>/dev/null | grep -qE '/Cursor\.app/Contents/MacOS/Cursor$|^/usr/share/cursor/cursor$|^cursor$'; then
  cursor_running=1
elif command -v pgrep >/dev/null 2>&1; then
  if pgrep -f 'Cursor.app/Contents/MacOS/Cursor' >/dev/null 2>&1 \
    || pgrep -xq Cursor >/dev/null 2>&1 \
    || pgrep -xq cursor >/dev/null 2>&1; then
    cursor_running=1
  fi
fi
if [[ "$cursor_running" -eq 1 ]]; then
  echo "⚠ cursor-storage: Cursor semble ouvert — import storage skippé."
  echo "  Quitte Cursor, relance ./scripts/install.sh, puis redémarre."
elif [[ -f "$STORAGE_JSON" ]]; then
  python3 "$ROOT/scripts/lib/cursor_storage.py" import "$STORAGE_JSON" "$STATE_DB"
else
  echo "→ cursor-storage: skip (pas de $STORAGE_JSON)"
fi

# Extensions : pas d'install auto — liste indicative dans extensions.txt seulement.

echo "OK — redémarre Cursor si les hooks / cursor-storage ne se rechargent pas."
echo "     Vérifie Settings → General (layout) + Agents/Review après restart."
echo "     Skills OpenCode mis à jour dans $OPENCODE_CONFIG/skills (si applicable)."
echo "     AGENTS.md OpenCode : créé seulement s'il était absent."
