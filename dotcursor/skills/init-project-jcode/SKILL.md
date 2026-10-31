---
name: init-project-jcode
description: >-
  Initialise un repo jcode avec tasks/ et memoire/ (sans .cursor).
  Crée et prérempli les fichiers méthodologiques. Bootstrap générique
  dans ~/.jcode/prompt-overlay.md via install-jcode.sh. Use when bootstrapping a
  jcode-only project, initializing tasks/ memoire/ without Cursor, or
  when the user asks for the jcode agent workflow structure.
disable-model-invocation: true
---

# Initialisation projet jcode

Crée l'ossature `tasks/` et `memoire/` à la racine du repo, avec les fichiers préremplis pour le workflow agent (Cherny's rules, séparation méthode/savoir projet, clôture de session). **Ne crée pas** `.cursor/`, `opencode.jsonc`, ni `./AGENTS.md`.

Équivalent jcode de `init-project` (Cursor) / `init-project-opencode` (OpenCode). Aligné avec `install-jcode.sh` : skills + bootstrap générique + user rules viennent de `~/.jcode/prompt-overlay.md` (canon `config-cursor/dotjcode/AGENTS.md`) et `~/.jcode/skills/`.

## Prérequis

- Le repo cible existe déjà (même vide).
- `install-jcode.sh` a déjà été joué au moins une fois (sinon le bootstrap générique n’est pas dans `~/.jcode/prompt-overlay.md`).

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

Ne pas créer `.cursor/`, `opencode.jsonc`, ni `./AGENTS.md` même s'ils sont absents. Si `.cursor/rules/bootstrap.mdc` ou `opencode.jsonc` existent déjà (projet mixte) : ne pas les toucher ; ce skill ne gère que l’ossature `tasks/` + `memoire/` pour jcode.

Le bootstrap (lire `PROJET` + `ANNEXE` + `lessons`) est **générique** et vit uniquement dans `~/.jcode/prompt-overlay.md` — **jamais** de `./AGENTS.md` projet ni de `~/AGENTS.md`.

### 2. Dossiers à créer

```
tasks/
memoire/
memoire/session/
```

### 3. Fichiers à créer

Contenus jcode-only dans [reference.md](reference.md). Sections partagées (todo, lessons, ANNEXE, CONVENTIONS, ARCHITECTURE) : lire [`../init-project/reference.md`](../init-project/reference.md).

**Copie canonique** — socle de méthode, copier tel quel :

| Fichier            | Source                                      | Rôle                                            |
| ------------------ | ------------------------------------------- | ----------------------------------------------- |
| `tasks/todo.md`    | init-project/reference.md → Copie todo      | Plan de travail de la session en cours          |
| `tasks/lessons.md` | init-project/reference.md → Copie lessons   | Socle méthode transversal (lecture seule agent) |

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
### Agentic Workflow ###
memoire
tasks
```

Ne pas ajouter `.cursor`, `opencode.jsonc`, ni `AGENTS.md` (le bootstrap jcode est global ; pas de `./AGENTS.md` projet).

### 6. Récapituler

Lister les fichiers créés et rappeler à l'utilisateur :
- Bootstrap jcode = `~/.jcode/prompt-overlay.md` (via `install-jcode.sh`) : lit `memoire/PROJET.md`, `memoire/ANNEXE.md` et `tasks/lessons.md`.
- Skills viennent de `~/.jcode/skills/` (même install), pas de ce skill.
- Sous jcode, les skills sont **à la demande** (`/nom-du-skill` ou injection embedding).
- `memoire/PROJET.md` est la source de vérité projet.
- `memoire/ANNEXE.md` est le catalogue des conditions de lecture ; `tasks/lessons.md` impose d’appliquer ce catalogue.
- Les annexes **spécifiques au projet** : sous `memoire/` + entrée dans `ANNEXE.md` — jamais dans le bootstrap global.
- `tasks/todo.md` : rempli à chaque session, reset à la clôture (`/cloture-session`).
- `tasks/lessons.md` : lecture seule agent ; `lessons-install.sh`.
- Besoin Cursor → `init-project` ; OpenCode → `init-project-opencode`.

## Séparation méthode / savoir projet

Règle fondamentale à ne **jamais** violer :
- `tasks/` = **méthode** (comment l'agent travaille) — portable entre projets.
- `memoire/` = **savoir projet** — propre au repo.
- Le câblage jcode générique vit dans `~/.jcode/prompt-overlay.md` : lire `PROJET.md` + `ANNEXE.md` + `tasks/lessons.md`.
- Les **conditions de lecture** des annexes vivent dans `memoire/ANNEXE.md`. `tasks/lessons.md` ne porte que la méthode : appliquer le catalogue attaché.
