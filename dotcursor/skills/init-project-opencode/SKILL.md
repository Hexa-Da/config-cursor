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

Contenus OpenCode-only dans [reference.md](reference.md). Sections partagées (todo, lessons, ANNEXE, CONVENTIONS, ARCHITECTURE) : lire [`../init-project/reference.md`](../init-project/reference.md).

**Copie canonique** — socle de méthode / câblage, copier tel quel :

| Fichier            | Source                                      | Rôle                                                                |
| ------------------ | ------------------------------------------- | ------------------------------------------------------------------- |
| `tasks/todo.md`    | init-project/reference.md → Copie todo      | Plan de travail de la session en cours                              |
| `tasks/lessons.md` | init-project/reference.md → Copie lessons   | Socle méthode transversal (lecture seule agent)                     |
| `opencode.jsonc`   | reference.md (ce skill) → Copie opencode.jsonc | Injecte `PROJET.md` + `ANNEXE.md` + `lessons.md` via `instructions` |

**Template à personnaliser** — savoir projet, adapter au repo cible :

| Fichier                    | Source                                         | Rôle                            |
| -------------------------- | ---------------------------------------------- | ------------------------------- |
| `memoire/PROJET.md`        | reference.md (ce skill) → Template PROJET.md   | Savoir projet essentiel         |
| `memoire/ANNEXE.md`        | init-project/reference.md → Template ANNEXE.md | Catalogue conditions de lecture |
| `memoire/CONVENTIONS.md`   | init-project/reference.md → Template CONVENTIONS | Conventions code/test         |
| `memoire/ARCHITECTURE.md`  | init-project/reference.md → Template ARCHITECTURE | Structure / patterns         |

### 4. Personnalisation

Demander à l'utilisateur (ou déduire du repo) :
- **Nom du projet** → remplacer `[NOM_PROJET]` dans `PROJET.md`, `ANNEXE.md` et annexes si présentes.
- **Stack technique** → compléter le tableau dans `PROJET.md`.
- **Triggers d'annexes** → adapter `ANNEXE.md` (et y ajouter une entrée par annexe spécialisée créée plus tard).

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
- `opencode.jsonc` est le point d'entrée OpenCode : `instructions` → `memoire/PROJET.md`, `memoire/ANNEXE.md` et `tasks/lessons.md`.
- Skills / `AGENTS.md` viennent de `~/.config/opencode` (via `install-opencode.sh` ou `install.sh`), pas de ce skill.
- `memoire/PROJET.md` est la source de vérité projet.
- `memoire/ANNEXE.md` est le catalogue des conditions de lecture des annexes `memoire/` ; `tasks/lessons.md` impose d'appliquer ce catalogue.
- Les annexes **spécifiques au projet** ne font **pas** partie du template générique : les créer sous `memoire/` et **ajouter une entrée dans `ANNEXE.md`** — le câblage `opencode.jsonc` reste fixe (3 injections).
- `tasks/todo.md` est rempli à chaque session, reset à la clôture (skill `cloture-session`).
- `tasks/lessons.md` : socle de méthode transversal (contraintes dures) — **lecture seule** pour l'agent ; `lessons-install.sh`.
- Besoin Cursor plus tard → skill `init-project` (ajoute `.cursor/rules/bootstrap.mdc`).

## Séparation méthode / savoir projet

Règle fondamentale à ne **jamais** violer :
- `tasks/` = **méthode** (comment l'agent travaille) — portable entre projets.
- `memoire/` = **savoir projet** (domaine, conventions, architecture, catalogue d'annexes) — propre au repo.
- Le câblage OpenCode injecte les trois sans fusionner leur contenu : `opencode.jsonc` → `PROJET.md` + `ANNEXE.md` + `tasks/lessons.md`.
- Les **conditions de lecture** des annexes vivent dans `memoire/ANNEXE.md` (savoir projet). `tasks/lessons.md` ne porte que la méthode : appliquer le catalogue attaché. Les annexes spécifiques s'ajoutent **uniquement** dans `ANNEXE.md` (et le fichier annexe) — jamais dans le câblage ni dans le template générique au-delà de CONVENTIONS / ARCHITECTURE.
