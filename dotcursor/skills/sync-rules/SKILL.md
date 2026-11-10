---
name: sync-rules
description: >-
  Syncs canonical `.cursor/rules/*.mdc` (bootstrap, context-mode, ponytail) from
  init-project/reference.md into every harness project under ~/Documents. Use
  when the user asks to sync-rules, sync / propager / aligner les rules canons,
  bootstrap.mdc, context-mode.mdc, or ponytail.mdc across projects.
disable-model-invocation: true
---

# sync-rules

Écrit les **copies canoniques** de rules dans tous les repos `~/Documents/*`
qui ont déjà le harness agent. Source unique : `init-project/reference.md`
(§ Copie `bootstrap.mdc` / `context-mode.mdc` / `ponytail.mdc`).

## Périmètre

| Inclus | Exclus |
| ------ | ------ |
| `.cursor/rules/bootstrap.mdc` | `tasks/todo.md`, `tasks/lessons.md` |
| `.cursor/rules/context-mode.mdc` | tout `memoire/*` |
| `.cursor/rules/ponytail.mdc` | autres fichiers sous `.cursor/rules/` |

## Harness cible

Enfant direct de `~/Documents` avec les trois dossiers :

```
memoire/   tasks/   .cursor/rules/
```

## Workflow

```
- [ ] 1. Lancer le script (écrit directement)
- [ ] 2. Lire le tableau SKIPPED / WROTE
- [ ] 3. Exit 0 = tous IDENTIQUES après sync
```

```bash
python3 ~/.cursor/skills/sync-rules/scripts/sync.py
# ou depuis le repo :
python3 ~/Documents/config-cursor/dotcursor/skills/sync-rules/scripts/sync.py
```

Écrit le contenu canon (crée si absent, écrase si diverge). Ne touche à rien
hors des trois `.mdc` listés.

## Règles

- Ne pas dupliquer les canons ici : toujours lire `init-project/reference.md`.
- Si `reference.md` change, relancer ce skill ; ne pas patcher les projets à la main.
