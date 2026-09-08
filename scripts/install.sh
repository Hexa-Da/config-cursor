#!/usr/bin/env bash
# Install this Cursor config onto the current machine (macOS / Linux / Windows+Git Bash).
# OpenCode mirror (AGENTS.md + skills) : délégué à install-opencode.sh.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOT_SRC="$ROOT/dotcursor"
USER_SRC="$ROOT/user"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

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

CURSOR_USER="$(detect_user_dir)"
CURSOR_DOT="$HOME/.cursor"

echo "→ User dir : $CURSOR_USER"
echo "→ Dotcursor: $CURSOR_DOT"

mkdir -p "$CURSOR_DOT/hooks" "$CURSOR_USER"

# ~/.cursor (hooks, skills, commands, agents)
# Plugins marketplace : liés au compte Cursor, pas versionnés ici
# (et ~/.cursor/plugins/ n'est qu'un cache de clones).
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
sync_dot_dir commands
sync_dot_dir agents

# OpenCode only (AGENTS.md + skills) — source unique
"$SCRIPT_DIR/install-opencode.sh"

if [[ ! -f "$CURSOR_DOT/mcp.json" && -f "$DOT_SRC/mcp.json.example" ]]; then
  cp "$DOT_SRC/mcp.json.example" "$CURSOR_DOT/mcp.json"
  echo "→ mcp.json créé depuis l'exemple (vide)"
fi

# Prefer ps (reliable on macOS Electron); fall back to pgrep.
cursor_running=0
if ps -axo comm= 2>/dev/null | grep -qE '/Cursor\.app/Contents/MacOS/Cursor$|^/usr/share/cursor/cursor$|^cursor$'; then
  cursor_running=1
elif command -v pgrep >/dev/null 2>&1; then
  if pgrep -f 'Cursor.app/Contents/MacOS/Cursor' >/dev/null 2>&1 \
    || pgrep -xq Cursor >/dev/null 2>&1 \
    || pgrep -xq cursor >/dev/null 2>&1; then
    cursor_running=1
  fi
fi

install_user_file() {
  local name="$1"
  local src="$USER_SRC/$name"
  local dst="$CURSOR_USER/$name"
  if [[ ! -f "$src" ]]; then
    return 0
  fi
  cp "$src" "$dst"
  if cmp -s "$src" "$dst"; then
    echo "→ $name OK (identique au repo)"
  else
    echo "⚠ $name: copie divergente après cp — vérifie $dst" >&2
    return 1
  fi
}

if [[ "$cursor_running" -eq 1 ]]; then
  echo "⚠ Cursor semble ouvert — settings/keybindings seront copiés, mais :"
  echo "  si keybindings.json (ou settings.json) est ouvert en dirty (M), Discard / ferme sans sauver,"
  echo "  puis Command Palette → Developer: Reload Window."
fi

install_user_file settings.json
install_user_file keybindings.json

# Agents/Review + Layout (state.vscdb) — skip si Cursor tourne (sinon overwrite au quit)
STATE_DB="$CURSOR_USER/globalStorage/state.vscdb"
STORAGE_JSON="$USER_SRC/cursor-storage.json"
if [[ "$cursor_running" -eq 1 ]]; then
  echo "⚠ cursor-storage: Cursor semble ouvert — import storage skippé."
  echo "  Quitte Cursor, relance ./scripts/install.sh, puis redémarre."
elif [[ -f "$STORAGE_JSON" ]]; then
  python3 "$ROOT/scripts/lib/cursor_storage.py" import "$STORAGE_JSON" "$STATE_DB"
else
  echo "→ cursor-storage: skip (pas de $STORAGE_JSON)"
fi

# Extensions : pas d'install auto — liste indicative dans extensions.txt seulement.

echo "OK — Reload Window si settings/keybindings / hooks ne se rechargent pas."
echo "     Vérifie Settings → General (layout) + Agents/Review après restart (storage)."
echo "     OpenCode : voir sortie de install-opencode.sh ci-dessus."
