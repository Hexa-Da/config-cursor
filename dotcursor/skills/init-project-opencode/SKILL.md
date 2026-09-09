---
name: init-project-opencode
description: >-
  Initialise un repo OpenCode avec tasks/, memoire/ et opencode.jsonc
  (sans .cursor). Crée et prérempli les fichiers méthodologiques.
  Use when bootstrapping an OpenCode-only project, initializing
  opencode.jsonc / tasks/ memoire/ without Cursor, or when the user
  asks for the OpenCode agent workflow structure.
disable-model-invocation: true
---

# Initialisation projet OpenCode

Crée l'ossature `tasks/`, `memoire/` et `opencode.jsonc` à la racine du repo, avec les fichiers préremplis pour le workflow agent (Cherny's rules, séparation méthode/savoir projet, clôture de session). **Ne crée pas** `.cursor/`.

Équivalent OpenCode de `init-project` (Cursor). Aligné avec `install-opencode.sh` : skills / `AGENTS.md` viennent de `~/.config/opencode`, le câblage projet est ce skill.

## Prérequis

- Le repo cible existe déjà (même vide).

## Workflow

Copier la checklist et la cocher au fil de l'exécution :

```
- [ ] 1. Audit : vérifier ce qui existe déjà
- [ ] 2. Créer les dossiers manquants
- [ ] 3. Créer les fichiers depuis les templates
- [ ] 4. Personnaliser PROJET.md si possible
- [ ] 5. Ajouter les entrées .gitignore
- [ ] 6. Récapituler à l'utilisateur
```

### 1. Audit

Vérifier l'existence de chaque dossier/fichier cible. Ne jamais écraser un fichier existant — signaler les conflits à l'utilisateur.

Ne pas créer `.cursor/` même s'il est absent. Si `.cursor/rules/bootstrap.mdc` existe déjà (projet mixte) : ne pas le toucher ; ce skill ne gère que le câblage OpenCode.

### 2. Dossiers à créer

```
tasks/
memoire/
memoire/session/
```

### 3. Fichiers à créer

Contenus OpenCode-only dans [reference.md](reference.md). Sections partagées (todo, lessons, CONVENTIONS, ARCHITECTURE, INDEX) : lire [`../init-project/reference.md`](../init-project/reference.md).

**Copie canonique** — socle de méthode / câblage, copier tel quel :

| Fichier            | Source                                      | Rôle                                                      |
| ------------------ | ------------------------------------------- | --------------------------------------------------------- |
| `tasks/todo.md`    | init-project/reference.md → Copie todo      | Plan de travail de la session en cours                    |
| `tasks/lessons.md` | init-project/reference.md → Copie lessons   | Leçons de méthode accumulées (transversal)                |
| `opencode.jsonc`   | reference.md (ce skill) → Copie opencode.jsonc | Injecte `PROJET.md` + `lessons.md` via `instructions` |

**Template à personnaliser** — savoir projet, adapter au repo cible :

| Fichier                    | Source                                         | Rôle                       |
| -------------------------- | ---------------------------------------------- | -------------------------- |
| `memoire/PROJET.md`        | reference.md (ce skill) → Template PROJET.md   | Savoir projet essentiel    |
| `memoire/CONVENTIONS.md`   | init-project/reference.md → Template CONVENTIONS | Conventions code/test    |
| `memoire/ARCHITECTURE.md`  | init-project/reference.md → Template ARCHITECTURE | Structure / patterns    |
| `memoire/session/INDEX.md` | init-project/reference.md → Template INDEX     | Index des sessions agent   |

### 4. Personnalisation

Demander à l'utilisateur (ou déduire du repo) :
- **Nom du projet** → remplacer `[NOM_PROJET]` dans `PROJET.md` (et annexes si présentes).
- **Stack technique** → compléter le tableau dans `PROJET.md`.

### 5. `.gitignore`

Ajouter les entrées suivantes si absentes (câblage agent local, pas versionné) :

```
### Docs Perso ###
memoire
tasks

### Adaptation OpenCode ###
opencode.jsonc
```

Ne pas ajouter `.cursor` (hors périmètre OpenCode-only).

### 6. Récapituler

Lister les fichiers créés et rappeler à l'utilisateur :
- `opencode.jsonc` est le point d'entrée OpenCode : `instructions` → `memoire/PROJET.md` et `tasks/lessons.md`.
- Skills / `AGENTS.md` viennent de `~/.config/opencode` (via `install-opencode.sh` ou `install.sh`), pas de ce skill.
- `memoire/PROJET.md` est la source de vérité projet.
- `memoire/CONVENTIONS.md` : lecture avant code **non trivial** (pas pour l'audit/lecture seule ni les fix triviaux) — via `tasks/lessons.md`.
- `memoire/ARCHITECTURE.md` : lecture si la tâche touche l'**interaction entre composants/modules**, un nouveau pattern, ou si la portée dépasse l'estimation initiale — via `tasks/lessons.md`.
- Les annexes **spécifiques au projet** ne font **pas** partie du template : les ajouter à la main dans `opencode.jsonc` et `PROJET.md` si le repo en a besoin.
- `tasks/todo.md` est rempli à chaque session, reset à la clôture (skill `cloture-session`).
- `tasks/lessons.md` accumule les leçons de méthode transversales (contraintes dures, pas un survol).
- Besoin Cursor plus tard → skill `init-project` (ajoute `.cursor/rules/bootstrap.mdc`).

## Séparation méthode / savoir projet

Règle fondamentale à ne **jamais** violer :
- `tasks/` = **méthode** (comment l'agent travaille) — portable entre projets.
- `memoire/` = **savoir projet** (domaine, conventions, architecture) — propre au repo.
- Le câblage OpenCode injecte les deux sans fusionner leur contenu : `opencode.jsonc` → `instructions`.
- Les règles de lecture des annexes génériques (CONVENTIONS, ARCHITECTURE, session) sont **transversales** : elles vivent dans `tasks/lessons.md` (synchronisé entre projets), pas dans le câblage. `opencode.jsonc` ne porte que l'injection (`PROJET.md` + `tasks/lessons.md`) et, si besoin, les annexes **vraiment propres au repo**, qui s'ajoutent **uniquement** dans le câblage et le `PROJET.md` de ce repo — jamais dans le template de ce skill.
