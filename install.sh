#!/usr/bin/env bash
# Install this Cursor config onto the current machine (macOS / Linux / Windows+Git Bash).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
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

CURSOR_USER="$(detect_user_dir)"
CURSOR_DOT="$HOME/.cursor"

echo "→ User dir : $CURSOR_USER"
echo "→ Dotcursor: $CURSOR_DOT"

mkdir -p "$CURSOR_DOT/hooks" "$CURSOR_USER/snippets"

# ~/.cursor (hooks) — ne pas écraser mcp.json s'il existe déjà
cp "$DOT_SRC/hooks.json" "$CURSOR_DOT/hooks.json"
cp "$DOT_SRC/hooks/garde-fou.py" "$CURSOR_DOT/hooks/garde-fou.py"
chmod +x "$CURSOR_DOT/hooks/garde-fou.py" 2>/dev/null || true

if [[ -d "$DOT_SRC/skills" ]] && [[ -n "$(find "$DOT_SRC/skills" -type f ! -name '.DS_Store' 2>/dev/null | head -1)" ]]; then
  mkdir -p "$CURSOR_DOT/skills"
  rsync -a --exclude '.DS_Store' "$DOT_SRC/skills/" "$CURSOR_DOT/skills/" 2>/dev/null \
    || cp -R "$DOT_SRC/skills/." "$CURSOR_DOT/skills/"
fi

if [[ ! -f "$CURSOR_DOT/mcp.json" && -f "$DOT_SRC/mcp.json.example" ]]; then
  cp "$DOT_SRC/mcp.json.example" "$CURSOR_DOT/mcp.json"
  echo "→ mcp.json créé depuis l'exemple (vide)"
fi

# settings / keybindings / snippets
[[ -f "$USER_SRC/settings.json" ]] && cp "$USER_SRC/settings.json" "$CURSOR_USER/settings.json"
[[ -f "$USER_SRC/keybindings.json" ]] && cp "$USER_SRC/keybindings.json" "$CURSOR_USER/keybindings.json"
if [[ -d "$USER_SRC/snippets" ]]; then
  cp -R "$USER_SRC/snippets/." "$CURSOR_USER/snippets/" 2>/dev/null || true
fi

# Extensions (IDs dans extensions.txt)
if [[ -f "$ROOT/extensions.txt" ]]; then
  if command -v cursor >/dev/null 2>&1; then
    echo "→ Installation des extensions…"
    while IFS= read -r line || [[ -n "$line" ]]; do
      [[ -z "$line" || "$line" =~ ^# ]] && continue
      cursor --install-extension "$line" || echo "  ! échec: $line"
    done < "$ROOT/extensions.txt"
  else
    echo "→ CLI 'cursor' introuvable — installe manuellement les IDs de extensions.txt"
  fi
fi

echo "OK — redémarre Cursor si les hooks ne se rechargent pas."
echo "Repo privé recommandé (settings.json peut contenir des hosts SSH)."
