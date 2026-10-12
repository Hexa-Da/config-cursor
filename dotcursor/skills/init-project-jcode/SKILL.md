---
name: init-project-jcode
description: >-
  Initialise un repo jcode avec tasks/, memoire/ et AGENTS.md
  (sans .cursor). Crée et prérempli les fichiers méthodologiques.
  Use when bootstrapping a jcode-only project, initializing
  AGENTS.md / tasks/ memoire/ without Cursor, or when the user
  asks for the jcode agent workflow structure.
disable-model-invocation: true
---

# Initialisation projet jcode

Crée l'ossature `tasks/`, `memoire/` et `AGENTS.md` à la racine du repo, avec les fichiers préremplis pour le workflow agent (Cherny's rules, séparation méthode/savoir projet, clôture de session). **Ne crée pas** `.cursor/` ni `opencode.jsonc`.

Équivalent jcode de `init-project` (Cursor) / `init-project-opencode` (OpenCode). Aligné avec `install-jcode.sh` : skills / `~/AGENTS.md` viennent de `~/.jcode`, le câblage projet est ce skill (`AGENTS.md` racine).

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

Ne pas créer `.cursor/` ni `opencode.jsonc` même s'ils sont absents. Si `.cursor/rules/bootstrap.mdc` ou `opencode.jsonc` existent déjà (projet mixte) : ne pas les toucher ; ce skill ne gère que le câblage jcode (`AGENTS.md` racine).

### 2. Dossiers à créer

```
tasks/
memoire/
memoire/session/
```

### 3. Fichiers à créer

Contenus jcode-only dans [reference.md](reference.md). Sections partagées (todo, lessons, ANNEXE, CONVENTIONS, ARCHITECTURE) : lire [`../init-project/reference.md`](../init-project/reference.md).

**Copie canonique** — socle de méthode / câblage, copier tel quel :

| Fichier            | Source                                      | Rôle                                                                |
| ------------------ | ------------------------------------------- | ------------------------------------------------------------------- |
| `tasks/todo.md`    | init-project/reference.md → Copie todo      | Plan de travail de la session en cours                              |
| `tasks/lessons.md` | init-project/reference.md → Copie lessons   | Socle méthode transversal (lecture seule agent)                     |
| `AGENTS.md`        | reference.md (ce skill) → Copie AGENTS.md   | Injecte `PROJET.md` + `ANNEXE.md` + `lessons.md` (bootstrap jcode)  |

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

### Adaptation jcode ###
AGENTS.md
```

Ne pas ajouter `.cursor` ni `opencode.jsonc` (hors périmètre jcode-only).

### 6. Récapituler

Lister les fichiers créés et rappeler à l'utilisateur :
- `AGENTS.md` (racine) est le point d'entrée jcode : lit `memoire/PROJET.md`, `memoire/ANNEXE.md` et `tasks/lessons.md`.
- Skills / `~/AGENTS.md` viennent de `~/.jcode` (via `install-jcode.sh` ou `install.sh`), pas de ce skill.
- `memoire/PROJET.md` est la source de vérité projet.
- `memoire/ANNEXE.md` est le catalogue des conditions de lecture des annexes `memoire/` ; `tasks/lessons.md` impose d'appliquer ce catalogue.
- Les annexes **spécifiques au projet** ne font **pas** partie du template générique : les créer sous `memoire/` et **ajouter une entrée dans `ANNEXE.md`** — le câblage `AGENTS.md` reste fixe (3 lectures).
- `tasks/todo.md` est rempli à chaque session, reset à la clôture (skill `cloture-session`).
- `tasks/lessons.md` : socle de méthode transversal (contraintes dures) — **lecture seule** pour l'agent ; `lessons-install.sh`.
- Besoin Cursor plus tard → skill `init-project` (ajoute `.cursor/rules/bootstrap.mdc`).
- Besoin OpenCode plus tard → skill `init-project-opencode` (ajoute `opencode.jsonc`).

## Séparation méthode / savoir projet

Règle fondamentale à ne **jamais** violer :
- `tasks/` = **méthode** (comment l'agent travaille) — portable entre projets.
- `memoire/` = **savoir projet** (domaine, conventions, architecture, catalogue d'annexes) — propre au repo.
- Le câblage jcode injecte les trois sans fusionner leur contenu : `AGENTS.md` → lire `PROJET.md` + `ANNEXE.md` + `tasks/lessons.md`.
- Les **conditions de lecture** des annexes vivent dans `memoire/ANNEXE.md` (savoir projet). `tasks/lessons.md` ne porte que la méthode : appliquer le catalogue attaché. Les annexes spécifiques s'ajoutent **uniquement** dans `ANNEXE.md` (et le fichier annexe) — jamais dans le câblage ni dans le template générique au-delà de CONVENTIONS / ARCHITECTURE.
