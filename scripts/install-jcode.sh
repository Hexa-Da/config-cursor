#!/usr/bin/env bash
# Install jcode-only config: ~/.jcode/prompt-overlay.md + system-prompt.md (depuis dotjcode/)
# + merge config.policy.toml → ~/.jcode/config.toml + ~/.jcode/skills.
# Does not touch Cursor hooks/settings/storage.
# Bootstrap générique = ~/.jcode/prompt-overlay.md (pas ~/AGENTS.md : Cursor le charge en doublon des User Rules).
# Ossature projet = skill init-project-jcode.
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

# User rules globales → prompt-overlay (couche jcode) : variante jcode de dotjcode/
# Pas ~/AGENTS.md : Cursor remonte les parents et le charge en doublon des User Rules.
if [[ -f "$ROOT/dotjcode/AGENTS.md" ]]; then
  cp "$ROOT/dotjcode/AGENTS.md" "$JCODE_HOME_DIR/prompt-overlay.md"
  echo "→ jcode prompt-overlay.md"
else
  echo "→ jcode prompt-overlay.md: skip (absent du repo)"
fi
if [[ -e "$HOME/AGENTS.md" ]]; then
  rm -f "$HOME/AGENTS.md"
  echo "→ purge legacy ~/AGENTS.md"
fi

# Base system prompt (couche Identity embarquée : remplacement complet, voir docs/SYSTEM_PROMPT_CONFIG.md)
if [[ -f "$ROOT/dotjcode/system-prompt.md" ]]; then
  cp "$ROOT/dotjcode/system-prompt.md" "$JCODE_HOME_DIR/system-prompt.md"
  echo "→ jcode system-prompt.md"
else
  echo "→ jcode system-prompt.md: skip (absent du repo)"
fi

# Hook pre_tool (garde-fou) : scripts + câblage via config.policy.toml merge
mkdir -p "$JCODE_HOME_DIR/hooks"
cp "$DOT_SRC/hooks/garde-fou.py" "$ROOT/dotjcode/hooks/garde-fou-jcode.py" "$JCODE_HOME_DIR/hooks/"
chmod +x "$JCODE_HOME_DIR/hooks/garde-fou.py" "$JCODE_HOME_DIR/hooks/garde-fou-jcode.py"
echo "→ jcode hooks: garde-fou-jcode.py"

POLICY="$ROOT/dotjcode/config.policy.toml"
if [[ -f "$POLICY" ]]; then
  python3 "$SCRIPT_DIR/lib/merge_jcode_config_policy.py" \
    "$POLICY" "$JCODE_HOME_DIR/config.toml"
else
  echo "→ jcode config.policy: skip (absent du repo)"
fi

echo "OK — Skills → $JCODE_SKILLS ; overlay → $JCODE_HOME_DIR/prompt-overlay.md ; system-prompt → $JCODE_HOME_DIR/system-prompt.md"
echo "     config.policy → $JCODE_HOME_DIR/config.toml (merge) ; bootstrap = prompt-overlay.md."
