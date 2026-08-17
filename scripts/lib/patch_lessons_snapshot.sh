#!/usr/bin/env bash
# Remplace le corps du fence ```markdown sous "## Copie lessons" dans un
# init-project/reference.md. N'écrit que si le contenu change.
# Usage: patch_lessons_snapshot.sh LESSONS.md REFERENCE.md
set -euo pipefail

lessons="${1:-}"
ref="${2:-}"

[[ -n "$lessons" && -n "$ref" ]] || {
  echo "usage: $0 LESSONS.md REFERENCE.md" >&2
  exit 1
}
[[ -f "$lessons" ]] || { echo "absent: $lessons" >&2; exit 1; }
[[ -f "$ref" ]] || { echo "absent: $ref" >&2; exit 1; }

tmp="$(mktemp)"
cleanup() { rm -f "$tmp"; }
trap cleanup EXIT

awk -v lessons_file="$lessons" '
  BEGIN {
    while ((getline line < lessons_file) > 0)
      body = body line ORS
    close(lessons_file)
  }
  /^## Copie lessons$/ { section = 1 }
  section && /^```markdown$/ {
    print
    printf "%s", body
    skip = 1
    next
  }
  skip && /^```$/ {
    print
    skip = 0
    section = 0
    replaced = 1
    next
  }
  skip { next }
  { print }
  END {
    if (!replaced) {
      print "Échec: bloc ## Copie lessons / ```markdown introuvable dans " FILENAME > "/dev/stderr"
      exit 1
    }
  }
' "$ref" > "$tmp"

if cmp -s "$tmp" "$ref"; then
  exit 0
fi

mv "$tmp" "$ref"
trap - EXIT
echo "synced → $ref"
