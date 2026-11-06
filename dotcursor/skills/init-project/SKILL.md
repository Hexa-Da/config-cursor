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
- [ ] 6. Récap : créés → câblage ; déjà présents → copies = strict, templates memoire/ = forme
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

| Fichier                            | § dans reference.md        | Rôle                                                                     |
| ---------------------------------- | -------------------------- | ------------------------------------------------------------------------ |
| `tasks/todo.md`                    | Copie todo                 | Plan de travail de la session en cours                                   |
| `tasks/lessons.md`                 | Copie lessons              | Socle méthode transversal (lecture seule agent)                          |
| `.cursor/rules/bootstrap.mdc`      | Copie bootstrap.mdc        | Always-on Cursor : attache `PROJET.md` + `ANNEXE.md`                     |
| `.cursor/rules/context-mode.mdc`   | Copie context-mode.mdc     | Always-on Cursor : routing MCP context-mode (sandbox contexte)           |

**Template à personnaliser** — savoir projet, adapter au repo cible :

| Fichier                    | § dans reference.md  | Rôle                                  |
| -------------------------- | -------------------- | ------------------------------------- |
| `memoire/PROJET.md`        | Template PROJET.md   | Savoir projet essentiel               |
| `memoire/ANNEXE.md`        | Template ANNEXE.md   | Catalogue des conditions de lecture   |
| `memoire/CONVENTIONS.md`   | Template CONVENTIONS | Conventions code/test du repo         |
| `memoire/ARCHITECTURE.md`  | Template ARCHITECTURE| Structure packages, patterns, flux    |

### 4. Personnalisation

Demander à l'utilisateur (ou déduire du repo) :
- **Nom du projet** → remplacer `[NOM_PROJET]` dans `PROJET.md`, `ANNEXE.md` et annexes si présentes.
- **Stack technique** → compléter le tableau dans `PROJET.md`.
- **Triggers d'annexes** → adapter `ANNEXE.md` (et y ajouter une entrée par annexe spécialisée créée plus tard).

### 5. `.gitignore`

Ajouter les entrées suivantes si absentes (câblage agent local, pas versionné) :

```
### Agentic Workflow ###
.cursor
memoire
tasks
```

### 6. Récapituler

**Cas A — aucun fichier cible n’existait** (tout vient d’être créé) :

Lister les fichiers créés. Rappeler brièvement :
- `.cursor/rules/bootstrap.mdc` injecte `PROJET.md` + `ANNEXE.md` et en fixe le rôle
- `.cursor/rules/context-mode.mdc` route les analyses vers le MCP context-mode (sandbox)
- Méthode agent = `AGENTS.md` ; `memoire/` = savoir projet ; `tasks/` = workspace session ; annexes spécialisées = entrée dans `ANNEXE.md` uniquement

**Cas B — au moins un fichier cible existait déjà** (ne pas écraser) :

À la place du rappel de câblage : comparer chaque fichier déjà présent à son § dans [reference.md](reference.md).

Méthode (obligatoire) :
1. Extraire le bloc canon du bon § de `reference.md` (tableaux §3).
2. **Copies canoniques** (`todo.md`, `lessons.md`, `bootstrap.mdc`, `context-mode.mdc`) : égalité textuelle **stricte** avec le bloc (trim final newline toléré uniquement). Statut `IDENTIQUE` ou `DIVERGE`. Comparer via code (`diff` unifié / `ctx_execute`) — pas à l’œil.
3. **Templates `memoire/`** (`PROJET.md`, `ANNEXE.md`, `CONVENTIONS.md`, `ARCHITECTURE.md`) : **pas** d’égalité texte. La personnalisation est attendue (nom projet à la place de `[NOM_PROJET]`, corps rempli, entrées d’annexes ajoutées). Vérifier uniquement la **forme générale** vs le template :
   - titre H1 du type `# <Nom> — …` (suffixe aligné sur le template : Contexte projet / Catalogue des annexes / Conventions / Architecture)
   - sections H2 requises présentes (mêmes intitulés que le template, ordre libre sauf si le template impose une logique claire)
   - pour `ANNEXE.md` : bloc d’intro catalogue + section « Cycle de vie d’une annexe » + section « Historique » (ou équivalent) ; entrées supplémentaires d’annexes = OK
   - pour `CONVENTIONS.md` / `ARCHITECTURE.md` : lien vers `PROJET.md` / `ANNEXE.md` en tête si le template en a un
   - Statut `FORME_OK` ou `FORME_ECART` (écarts = section manquante / titre hors gabarit / structure cassée — pas le contenu métier)
4. Ne pas modifier les fichiers en écart dans cette étape ; seulement rapporter.

Format de sortie (un tableau, puis détails seulement pour `DIVERGE` / `FORME_ECART`) :

| Fichier | Mode | Statut | Écart |
| ------- | ---- | ------ | ----- |
| `path`  | copie / template | IDENTIQUE / DIVERGE / FORME_OK / FORME_ECART | résumé 1 ligne ou `—` |

Pour chaque `DIVERGE` : diff unifié (hunks principaux si trop long). Pour chaque `FORME_ECART` : lister les manques structurels. Pas d’overwrite sauf demande explicite ensuite.

## Séparation méthode / savoir projet

Règle fondamentale à ne **jamais** violer :
- Méthode agent = **User Rules** (`AGENTS.md`) — pas un fichier projet injecté.
- `tasks/` = **workspace session** (`todo.md`, `lessoms.md`) — propre au déroulement local.
- `memoire/` = **savoir projet** (domaine, conventions, architecture, catalogue d'annexes) — propre au repo.
- Le câblage injecte les deux sans fusionner leur contenu : `.cursor/rules/bootstrap.mdc` → `PROJET.md` + `ANNEXE.md`.
- Le **catalogue** (mode d’emploi, entrées, triggers, cycle de vie) vit dans `memoire/ANNEXE.md` ; le bootstrap en fixe l’objectif (quelles annexes ouvrir). Les annexes spécifiques s'ajoutent **uniquement** dans `ANNEXE.md` (et le fichier annexe) — jamais dans le câblage ni dans le template générique au-delà de CONVENTIONS / ARCHITECTURE.
