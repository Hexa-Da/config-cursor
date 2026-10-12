#!/usr/bin/env bash
# Install jcode-only config: ~/AGENTS.md + ~/.jcode/skills (frontmatter adapted).
# Does not touch Cursor hooks/settings/storage. Bootstrap générique = ~/AGENTS.md ; ossature projet = skill init-project-jcode.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOT_SRC="$ROOT/dotcursor"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# jcode home: JCODE_HOME > ~/.jcode
detect_jcode_home() {
  if [[ -n "${JCODE_HOME:-}" ]]; then
    echo "$JCODE_HOME"
  else
    echo "$HOME/.jcode"
  fi
}

JCODE_HOME_DIR="$(detect_jcode_home)"
JCODE_SKILLS="$JCODE_HOME_DIR/skills"
echo "→ jcode    : $JCODE_HOME_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "✗ python3 requis pour sync_jcode_skills.py" >&2
  exit 1
fi

mkdir -p "$JCODE_HOME_DIR"

# Skills: miroir exact de dotcursor/skills, frontmatter adapté
# (description une ligne ; name / description / allowed-tools seulement).
# Orphelins côté jcode retirés (prune), comme rsync --delete.
if [[ -d "$DOT_SRC/skills" ]]; then
  python3 "$SCRIPT_DIR/lib/sync_jcode_skills.py" \
    "$DOT_SRC/skills" "$JCODE_SKILLS"
else
  echo "→ jcode skills: skip (pas de $DOT_SRC/skills)"
fi

# ~/AGENTS.md (= user rules globales) : miroir depuis la racine du repo
if [[ -f "$ROOT/AGENTS.md" ]]; then
  cp "$ROOT/AGENTS.md" "$HOME/AGENTS.md"
  echo "→ jcode ~/AGENTS.md"
else
  echo "→ jcode ~/AGENTS.md: skip (absent du repo)"
fi

echo "OK — Skills → $JCODE_SKILLS ; AGENTS.md → $HOME/AGENTS.md"
echo "     Bootstrap générique = ~/AGENTS.md ; ossature projet = skill init-project-jcode."
