---
name: init-project
description: >-
  Initialise un repo Cursor avec la structure tasks/, memoire/ et .cursor/rules/
  pour le workflow agent. Crée et prérempli les fichiers méthodologiques.
  Use when bootstrapping a new project, initializing tasks/ memoire/ .cursor/,
  or when the user asks to set up the agent workflow structure.
disable-model-invocation: true
---

# Initialisation projet Cursor

Crée l'ossature `tasks/`, `memoire/` et `.cursor/rules/` à la racine du repo, avec les fichiers préremplis pour le workflow agent (Cherny's rules, séparation méthode/savoir projet, clôture de session).

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

Si un ancien `.cursor/rules/projet.mdc` existe : ne pas l'écraser ; proposer de le renommer / remplacer par `bootstrap.mdc` (nouveau nom canonique).

### 2. Dossiers à créer

```
tasks/
memoire/
memoire/session/
.cursor/
.cursor/rules/
```

### 3. Fichiers à créer

Tous les contenus sont dans [reference.md](reference.md). Deux modes :

**Copie canonique** — socle de méthode / câblage, copier tel quel (capital transversal entre projets) :

| Fichier                       | § dans reference.md    | Rôle                                                        |
| ----------------------------- | ---------------------- | ----------------------------------------------------------- |
| `tasks/todo.md`               | Copie todo             | Plan de travail de la session en cours                      |
| `tasks/lessons.md`            | Copie lessons          | Leçons de méthode accumulées (transversal)                  |
| `.cursor/rules/bootstrap.mdc` | Copie bootstrap.mdc    | Always-on : attache `PROJET.md` + `lessons.md` + annexes    |

**Template à personnaliser** — savoir projet, adapter au repo cible :

| Fichier                    | § dans reference.md  | Rôle                                  |
| -------------------------- | -------------------- | ------------------------------------- |
| `memoire/PROJET.md`        | Template PROJET.md   | Savoir projet essentiel               |
| `memoire/CONVENTIONS.md`   | Template CONVENTIONS | Conventions code/test du repo         |
| `memoire/ARCHITECTURE.md`  | Template ARCHITECTURE| Structure packages, patterns, flux    |
| `memoire/session/INDEX.md` | Template INDEX       | Index des sessions agent              |

### 4. Personnalisation

Demander à l'utilisateur (ou déduire du repo) :
- **Nom du projet** → remplacer `[NOM_PROJET]` dans `PROJET.md` (et annexes si présentes).
- **Stack technique** → compléter le tableau dans `PROJET.md`.

### 5. `.gitignore`

Ajouter les entrées suivantes si absentes (ces dossiers sont personnels, pas versionnés) :

```
### Docs Perso ###
.cursor
memoire
tasks
```

### 6. Récapituler

Lister les fichiers créés et rappeler à l'utilisateur :
- `.cursor/rules/bootstrap.mdc` est le point d'entrée always-on : injecte `memoire/PROJET.md` et `tasks/lessons.md`.
- `memoire/PROJET.md` est la source de vérité projet.
- `memoire/CONVENTIONS.md` et `memoire/ARCHITECTURE.md` sont lus à la demande (via `bootstrap.mdc`).
- `tasks/todo.md` est rempli à chaque session, reset à la clôture (skill `cloture-session`).
- `tasks/lessons.md` accumule les leçons de méthode transversales (contraintes dures, pas un survol).

## Séparation méthode / savoir projet

Règle fondamentale à ne **jamais** violer :
- `tasks/` = **méthode** (comment l'agent travaille) — portable entre projets.
- `memoire/` = **savoir projet** (domaine, conventions, architecture) — propre au repo.
- `bootstrap.mdc` **câble** les deux (injection) sans fusionner leur contenu.
