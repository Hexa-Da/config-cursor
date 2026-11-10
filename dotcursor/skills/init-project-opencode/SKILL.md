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

Équivalent OpenCode de `init-project` (Cursor). Aligné avec `install-opencode.sh` : skills / `AGENTS.md` viennent de `~/.config/opencode` (canon `config-cursor/dotopencode/AGENTS.md`), le câblage projet est ce skill.

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

Ne pas créer `.cursor/` même s'il est absent. Si `.cursor/rules/bootstrap.mdc` existe déjà (projet mixte) : ne pas le toucher ; ce skill ne gère que le câblage OpenCode.

### 2. Dossiers à créer

```
tasks/
memoire/
memoire/session/
```

### 3. Fichiers à créer

Contenu OpenCode-only : [reference.md](reference.md) (`opencode.jsonc`).
Sections partagées (todo, lessons, PROJET, ANNEXE, CONVENTIONS, ARCHITECTURE) :
[`../init-project/reference.md`](../init-project/reference.md).

**Copie canonique** — socle de méthode / câblage, copier tel quel :

| Fichier            | Source                                      | Rôle                                                                |
| ------------------ | ------------------------------------------- | ------------------------------------------------------------------- |
| `tasks/todo.md`    | init-project/reference.md → Copie todo      | Plan de travail de la session en cours                              |
| `tasks/lessons.md` | init-project/reference.md → Copie lessons   | Inbox locale frictions méthode/harness (écriture à la clôture)  |
| `opencode.jsonc`   | reference.md (ce skill) → Copie opencode.jsonc | Injecte `PROJET.md` + `ANNEXE.md` via `instructions` |

**Template à personnaliser** — savoir projet, adapter au repo cible :

| Fichier                    | Source                                         | Rôle                            |
| -------------------------- | ---------------------------------------------- | ------------------------------- |
| `memoire/PROJET.md`        | init-project/reference.md → Template PROJET.md | Savoir projet essentiel         |
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

### Adaptation OpenCode ###
opencode.jsonc
```

Ne pas ajouter `.cursor` (hors périmètre OpenCode-only).

### 6. Récapituler

**Cas A — aucun fichier cible n’existait** (tout vient d’être créé) :

Lister les fichiers créés. Rappeler brièvement :
- `opencode.jsonc` injecte `PROJET.md` + `ANNEXE.md` via `instructions` et en fixe le rôle
- Skills / `AGENTS.md` = `~/.config/opencode` (méthode) ; `memoire/` = savoir projet ; `tasks/` = workspace session ; annexes spécialisées = entrée dans `ANNEXE.md` uniquement
- Besoin Cursor → `init-project` (ajoute `.cursor/rules/bootstrap.mdc`)

**Cas B — au moins un fichier cible existait déjà** (ne pas écraser) :

À la place du rappel de câblage : comparer chaque fichier déjà présent à son § source (tableaux §3).

Méthode (obligatoire) :
1. Extraire le bloc canon du bon § (`../init-project/reference.md` pour todo/lessons/PROJET/ANNEXE/CONVENTIONS/ARCHITECTURE ; [reference.md](reference.md) pour `opencode.jsonc`).
2. **Copies canoniques** (`todo.md`, `opencode.jsonc`) : égalité textuelle **stricte** avec le bloc (trim final newline toléré uniquement). Statut `IDENTIQUE` ou `DIVERGE`. Comparer via code (`diff` unifié / `ctx_execute`) — pas à l’œil. `tasks/lessons.md` : **pas** d’égalité stricte (inbox locale qui accumule) — présence + titre `# Lessons` → `FORME_OK` / `FORME_ECART` / absent.
3. **Templates `memoire/`** (`PROJET.md`, `ANNEXE.md`, `CONVENTIONS.md`, `ARCHITECTURE.md`) : **pas** d’égalité texte. La personnalisation est attendue (nom projet à la place de `[NOM_PROJET]`, corps rempli, entrées d’annexes ajoutées). Vérifier uniquement la **forme générale** vs le template :
   - titre H1 du type `# <Nom> — …` (suffixe aligné sur le template : Contexte projet / Catalogue des annexes / Conventions / Architecture)
   - sections H2 requises présentes (mêmes intitulés que le template, ordre libre sauf si le template impose une logique claire) — `ANNEXE.md` / `CONVENTIONS.md` / `ARCHITECTURE.md` : pas de H2 obligatoires dans le template
   - pour `ANNEXE.md` : liste à puces (CONVENTIONS + ARCHITECTURE + spécialisées) ; pas de section méthode « cycle de vie » (vit dans le skill `memoire`)
   - pas de bandeau `> Annexe de [PROJET.md]…`
   - Statut `FORME_OK` ou `FORME_ECART` (écarts = section manquante / titre hors gabarit / structure cassée — pas le contenu métier)
4. Ne pas modifier les fichiers en écart dans cette étape ; seulement rapporter.

Format de sortie (un tableau, puis détails seulement pour `DIVERGE` / `FORME_ECART`) :

| Fichier | Mode | Statut | Écart |
| ------- | ---- | ------ | ----- |
| `path`  | copie / template | IDENTIQUE / DIVERGE / FORME_OK / FORME_ECART | résumé 1 ligne ou `—` |

Pour chaque `DIVERGE` : diff unifié (hunks principaux si trop long). Pour chaque `FORME_ECART` : lister les manques structurels. Pas d’overwrite sauf demande explicite ensuite.

## Séparation méthode / savoir projet

Règle fondamentale à ne **jamais** violer :
- Méthode agent = **User Rules** (`~/.config/opencode/AGENTS.md`) — pas un fichier projet injecté.
- `tasks/` = **workspace session** (`todo.md`, `lessons.md`) — propre au déroulement local.
- `memoire/` = **savoir projet** (domaine, conventions, architecture, catalogue d'annexes) — propre au repo.
- Le câblage OpenCode injecte les deux sans fusionner leur contenu : `opencode.jsonc` → `PROJET.md` + `ANNEXE.md`.
- Le **catalogue** (entrées, triggers, exclusions, dépendances) vit dans `memoire/ANNEXE.md` ; le câblage `instructions` en fixe l’objectif (quelles annexes ouvrir). Le **cycle de vie** des annexes (créer / scinder / fusionner / supprimer) vit dans le skill `memoire`. Les annexes spécifiques s'ajoutent **uniquement** dans `ANNEXE.md` (et le fichier annexe) — jamais dans le câblage ni dans le template générique au-delà de CONVENTIONS / ARCHITECTURE.
