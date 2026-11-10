---
name: sync
description: >-
  Syncs harness files across ~/Documents projects from init-project/reference.md:
  canonical .cursor/rules/*.mdc via scripts/sync.py; tasks/ + memoire/ templates
  agent-driven (seed if missing, form-check if present). Use when the user asks
  /sync, sync-rules, propager / aligner canons, bootstrap.mdc, context-mode,
  ponytail, or to seed/align tasks/ and memoire/ templates.
disable-model-invocation: true
---

# sync

Aligne les repos harness sous `~/Documents` sur
[`init-project/reference.md`](../init-project/reference.md).

- **`.mdc`** → script Python (écriture IDENTIQUE)
- **`tasks/` + `memoire/`** → agent (semis / forme, pas d’écrasement)

## Source

Résoudre `reference.md` dans cet ordre :

1. voisin de ce skill : `…/skills/init-project/reference.md`
2. fallback : `~/Documents/config-cursor/dotcursor/skills/init-project/reference.md`

Ne pas dupliquer les canons dans ce skill.

## Harness cible

Enfant direct de `~/Documents` (ignorer les dossiers cachés) qui a déjà :

```
memoire/   tasks/   .cursor/rules/
```

Ne pas créer de nouveaux projets ici → `init-project`.

## Périmètre et modes

| Fichier | § `reference.md` | Mode |
| ------- | ---------------- | ---- |
| `.cursor/rules/bootstrap.mdc` | Copie bootstrap.mdc | **Script** — écrire (créer / écraser) |
| `.cursor/rules/context-mode.mdc` | Copie context-mode.mdc | **Script** — écrire |
| `.cursor/rules/ponytail.mdc` | Copie ponytail.mdc | **Script** — écrire |
| `tasks/todo.md` | Copie todo | **Agent** — semer si absent ; sinon forme |
| `tasks/lessons.md` | Copie lessons | **Agent** — semer si absent ; sinon forme |
| `memoire/PROJET.md` | Template PROJET.md | **Agent** — semer si absent ; sinon forme |
| `memoire/ANNEXE.md` | Template ANNEXE.md | **Agent** — semer si absent ; sinon forme |
| `memoire/CONVENTIONS.md` | Template CONVENTIONS | **Agent** — semer si absent ; sinon forme |
| `memoire/ARCHITECTURE.md` | Template ARCHITECTURE | **Agent** — semer si absent ; sinon forme |

**Exclus** : autres `.mdc`, annexes spécialisées, `memoire/session/*`, contenu
métier déjà personnalisé (pas d’écrasement silencieux des templates présents).

Dossier `memoire/session/` : créer s’il manque (vide).

### Forme (fichiers déjà présents, agent)

Réutiliser les critères Cas B de [`init-project/SKILL.md`](../init-project/SKILL.md)
(§ Récapituler) :

- `todo.md` : H1 + sections `Tâche` / `Plan` / `Review` → `FORME_OK` /
  `FORME_ECART` (ne pas écraser le plan en cours)
- `lessons.md` : titre `# Lessons…` → `FORME_OK` / `FORME_ECART`
- templates `memoire/` : H1 gabarit + H2 attendus ; `ANNEXE.md` = catalogue +
  (si présente) `Historique` ; **pas** de § méthode « cycle de vie »
- Statuts agent : `FORME_OK` / `FORME_ECART` / `ABSENT→WROTE`
- Statuts script : `SKIPPED` / `WROTE`

Ne corriger un `FORME_ECART` que sur demande explicite.

## Workflow

```
- [ ] 1. Lancer scripts/sync.py (les 3 .mdc)
- [ ] 2. Extraire les blocs tasks/ + memoire/ depuis reference.md
- [ ] 3. Pour chaque projet harness : semer absents ; noter formes
- [ ] 4. Récap : tableau script + tableau agent ; détails FORME_ECART
```

### 1) Rules (script)

```bash
python3 ~/.cursor/skills/sync/scripts/sync.py
# ou depuis le repo :
python3 ~/Documents/config-cursor/dotcursor/skills/sync/scripts/sync.py
```

Lire le tableau `SKIPPED` / `WROTE`. Exit 0 = tous IDENTIQUES après sync.
Ne touche qu’aux trois `.mdc`.

### 2–3) tasks/ + memoire/ (agent)

Extraire les fenced blocks des § Copie todo / Copie lessons / Template *.
Pour chaque projet harness (même liste que le script) : créer les absents ;
vérifier la forme des présents. Écritures = outils d’édition natifs.

## Récap

Fusionner en un tableau (ou deux si plus lisible) :

| Projet | Fichier | Mode | Action |
| ------ | ------- | ---- | ------ |
| `name` | `path` | script / semer / forme | SKIPPED / WROTE / FORME_OK / FORME_ECART / ABSENT→WROTE |

Puis seulement les `FORME_ECART` et tout échec d’écriture / exit ≠ 0 du script.

## Règles

- Source unique = `init-project/reference.md` ; si elle change, relancer `/sync`.
- Au semis : remplacer `[NOM_PROJET]` si le nom du dossier projet est évident.
- Ne pas toucher `config-cursor` comme cible sauf demande (c’est la source).
