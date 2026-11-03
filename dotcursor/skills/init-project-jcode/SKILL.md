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
- [ ] 6. Récap : créés → câblage ; déjà présents → copies = strict, templates memoire/ = forme
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

**Cas A — aucun fichier cible n’existait** (tout vient d’être créé) :

Lister les fichiers créés. Rappeler brièvement :
- Bootstrap jcode = `~/.jcode/prompt-overlay.md` (via `install-jcode.sh`) : lit `PROJET.md` + `ANNEXE.md` + `tasks/lessons.md`
- Skills = `~/.jcode/skills/` (à la demande) ; `memoire/` = savoir projet ; `tasks/` = méthode ; annexes spécialisées = entrée dans `ANNEXE.md` uniquement
- Besoin Cursor → `init-project` ; OpenCode → `init-project-opencode`

**Cas B — au moins un fichier cible existait déjà** (ne pas écraser) :

À la place du rappel de câblage : comparer chaque fichier déjà présent à son § source (tableaux §3).

Méthode (obligatoire) :
1. Extraire le bloc canon du bon § (`../init-project/reference.md` pour todo/lessons/ANNEXE/CONVENTIONS/ARCHITECTURE ; [reference.md](reference.md) pour `PROJET.md`).
2. **Copies canoniques** (`todo.md`, `lessons.md`) : égalité textuelle **stricte** avec le bloc (trim final newline toléré uniquement). Statut `IDENTIQUE` ou `DIVERGE`. Comparer via code (`diff` unifié / `ctx_execute`) — pas à l’œil.
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
- `tasks/` = **méthode** (comment l'agent travaille) — portable entre projets.
- `memoire/` = **savoir projet** — propre au repo.
- Le câblage jcode générique vit dans `~/.jcode/prompt-overlay.md` : lire `PROJET.md` + `ANNEXE.md` + `tasks/lessons.md`.
- Le **catalogue** (mode d’emploi, entrées, triggers, cycle de vie) vit dans `memoire/ANNEXE.md` ; le bootstrap global en fixe l’objectif (quelles annexes ouvrir). Les annexes spécifiques s'ajoutent **uniquement** dans `ANNEXE.md` (et le fichier annexe) — jamais dans le bootstrap global ni dans le template générique au-delà de CONVENTIONS / ARCHITECTURE.
