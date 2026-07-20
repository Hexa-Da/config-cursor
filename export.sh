#!/usr/bin/env bash
# Export machine Cursor config → this repo (miroir de install.sh).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DOT_DST="$ROOT/dotcursor"
USER_DST="$ROOT/user"

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

echo "→ Export depuis"
echo "  User dir : $CURSOR_USER"
echo "  Dotcursor: $CURSOR_DOT"
echo "→ Vers     : $ROOT"

mkdir -p "$DOT_DST/hooks" "$USER_DST"

# Hooks
if [[ -f "$CURSOR_DOT/hooks.json" ]]; then
  cp "$CURSOR_DOT/hooks.json" "$DOT_DST/hooks.json"
fi
if [[ -f "$CURSOR_DOT/hooks/garde-fou.py" ]]; then
  cp "$CURSOR_DOT/hooks/garde-fou.py" "$DOT_DST/hooks/garde-fou.py"
  chmod +x "$DOT_DST/hooks/garde-fou.py" 2>/dev/null || true
fi

export_dot_dir() {
  local name="$1"
  if [[ -d "$CURSOR_DOT/$name" ]]; then
    python3 - "$CURSOR_DOT/$name" "$DOT_DST/$name" <<'PY'
import shutil, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
real = [p for p in dst.rglob("*") if p.is_file() and p.name != ".gitkeep"]
if not real:
    (dst / ".gitkeep").write_text("")
PY
  fi
}

export_dot_dir skills
export_dot_dir plugins
export_dot_dir commands
export_dot_dir agents

[[ -f "$CURSOR_USER/settings.json" ]] && cp "$CURSOR_USER/settings.json" "$USER_DST/settings.json"
[[ -f "$CURSOR_USER/keybindings.json" ]] && cp "$CURSOR_USER/keybindings.json" "$USER_DST/keybindings.json"

# Extensions IDs
EXT_JSON="$HOME/.cursor/extensions/extensions.json"
if [[ -f "$EXT_JSON" ]] && command -v python3 >/dev/null 2>&1; then
  python3 - "$EXT_JSON" "$ROOT/extensions.txt" <<'PY'
import json, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
data = json.loads(src.read_text(encoding="utf-8"))
ids = sorted({
    (e.get("identifier") or {}).get("id")
    for e in data
    if (e.get("identifier") or {}).get("id")
})
header = (
    "# Extensions Cursor à réinstaller (marketplace)\n"
    "# Usage: cursor --install-extension <id>\n\n"
)
dst.write_text(header + "\n".join(ids) + ("\n" if ids else ""), encoding="utf-8")
print(f"→ extensions.txt ({len(ids)} ids)")
PY
fi

# mcp : ne jamais écraser l'exemple avec des secrets — exporte seulement si absent
if [[ -f "$CURSOR_DOT/mcp.json" && ! -f "$DOT_DST/mcp.json.example" ]]; then
  cp "$CURSOR_DOT/mcp.json" "$DOT_DST/mcp.json.example"
  echo "→ mcp.json.example créé (vérifie qu'il n'y a pas de secrets)"
fi

echo "OK — revue git status, puis commit si tu veux figer l'export."
