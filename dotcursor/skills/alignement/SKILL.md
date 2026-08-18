---
name: alignement
description: >-
  Checks config-cursor repo vs this machine (hooks, skills, settings,
  cursor-storage, OpenCode, lessons). Use when the user asks to verify
  alignment, alignement, repo vs machine, or whether install.sh / export.sh
  is needed.
disable-model-invocation: true
---

# Alignement repo ↔ machine

Vérif **en lecture**. Ne pas lancer `install.sh` / `export.sh` /
`lessons-install.sh` sauf demande explicite.

## Checklist

```
- [ ] 1. Lancer scripts/check.py
- [ ] 2. Lire OK / DRIFT / INFO (ne pas re-diff à la main)
- [ ] 3. Rapporter ; proposer le script de sync selon le sens, sans l'exécuter
```

```bash
python3 ~/.cursor/skills/alignement/scripts/check.py
# ou depuis le repo :
python3 ~/Documents/config-cursor/dotcursor/skills/alignement/scripts/check.py
```

Exit 0 = pas de `DRIFT`. Exit 1 = écart inattendu.

## Lecture du rapport

| Statut | Sens |
| --- | --- |
| **OK** | Couche identique |
| **DRIFT** | Écart à corriger. Le détail indique `install.sh` (repo → machine) ou `export.sh` (machine → repo) ou `lessons-install.sh` |
| **INFO** | Attendu : extensions indicatives, skills OpenCode-only, Cursor ouvert, worktree sale |
| **SKIP** | Fichier / couche absente |

- OpenCode `SKILL.md` : le script compare au **transform** (`sync_opencode_skills.py`), pas au brut Cursor.
- `extensions.txt` n'est **pas** une source de vérité (`install.sh` ne les installe pas).
- `__pycache__` / `.gitkeep` ignorés.
- Cursor ouvert → ne pas conclure qu'il faut `install.sh` pour `cursor-storage` (overwrite au quit).

Ne pas réimplémenter les diffs. Si le script manque une couche, l'ajouter au script, pas dans le chat.
