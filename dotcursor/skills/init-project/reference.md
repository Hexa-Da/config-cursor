# Référence — init-project

Templates des fichiers à générer. Copier tels quels sauf les placeholders `[…]`.

---

## Copie todo

Fichier cible : `tasks/todo.md` — copier **tel quel**.

```markdown
# Todo — tâche en cours

> Plan de travail de la session qui suit les Cherny's rules. Distinct de `memoire/`.

## Tâche

<!-- Titre court de la tâche en cours -->

## Plan

- [ ] Étape 1
- [ ] Étape 2
- [ ] Étape 3

## Review

<!-- À remplir en fin de tâche : ce qui a été fait, comment ça a été vérifié, écarts par rapport au plan. -->
```

---

## Copie lessons

Fichier cible : `tasks/lessons.md` — copier **tel quel** (socle de méthode transversal, accumulé au fil des projets).

```markdown
# Lessons — méthode de l'agent

> Leçons **de méthode** (comment l'agent travaille), valables tous projets confondus.
> Distinct de `memoire/CONVENTIONS.md` / `memoire/ARCHITECTURE.md`, qui capitalisent les leçons **propres au repo courant**.
> Une leçon ici doit survivre à un changement de projet ; sinon elle va dans `memoire/`.

**Test de tri** : retirer tout vocabulaire du domaine/repo courant de la leçon. Si elle garde un sens et éviterait la même erreur sur un projet totalement différent → ici. Si le sens disparaît sans ce vocabulaire → `memoire/`.

## Format

Fichier always-on : **titre + règle seulement** (pas de Symptôme/Cause ici — coût token).
À la capture : dériver Symptôme → Cause → Règle, puis n'écrire que la règle, concise.

---

### Git : lecture libre, écriture interdite

Ne **jamais** faire de commit (ni `commit`, `push`, `rebase`, `reset`… — toute écriture dans l'historique) **sauf demande explicite** (« fait un commit », « committe ça ») — alors exécuter directement, sans reproposer un message à valider. Sinon : lecture libre (`git status`, `git diff`, `git log`…) et **proposer** un message en fin de tâche cohérente — c'est l'utilisateur qui committe.

### Worktrees : principal si libre ; sinon un agent = un worktree = un `tasks/todo.md`

- Confirmer le **worktree actif** ; toute action reste dans ce root (pas de `tasks/todo.md` hors de ce répertoire).
- **Défaut = principal** s'il est libre (aucun autre agent + working tree propre) → changer de branche **sur place**.
- Worktree secondaire **seulement** si le principal est occupé ; un agent = un worktree = un `tasks/todo.md` local — ne pas écraser celui d'un autre.
- **Demander** avant de créer un worktree ou une branche.

### Ne pas lancer l'environnement ni les tests lourds pour « vérifier » — dire quoi tester

- Ne **jamais** lancer l'environnement complet ni les suites lourdes sans demande explicite.
- Si une vérif runtime est nécessaire : **dire tout de suite** quoi tester (commande, résultat attendu) — pas d'attente muette ni de relances en boucle.
- En fin de tâche : **checklist concise** (quoi lancer, volume, durée indicative).
- OK sans demander : lecture, lint, compile locale rapide.

### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
- Fin de plan = Review dans `tasks/todo.md` (+ leçons si besoin) — pas de nouveau rapport ni retouche d'un ancien.
- Clôture = demande utilisateur → skill `cloture-session` → **nouveau** fichier + ligne INDEX ; **jamais** modifier un rapport déjà écrit.
- Dans le rapport : message de commit complet pour chaque commit — template dans `cloture-session/reference.md`.

### Ne pas relire les annexes `memoire/` à chaque tour ni les ignorer par défaut

- `CONVENTIONS.md` — avant code **non trivial** (feature, nouveau fichier, migration, test) ou doute de pattern ; **pas** pour audit lecture seule, question, typo, fix d'une ligne. Une fois par session, sauf changement de domaine.
- `ARCHITECTURE.md` — interaction multi-composants, nouveau pattern, ou frontière de module ; lire en cours de tâche si la portée grossit.
- `memoire/session/` — seulement pour reprendre un travail passé (demande explicite).

### Ne pas transformer une dette legacy en « convention » sans vérifier la cible à jour

- Avant d'aligner sur un pattern existant : vérifier la convention **cible** (`CONVENTIONS.md`, `ARCHITECTURE.md`, annexe) vs **dette**.
- Ne pas présenter un usage observé comme convention sans source normative récente ou exemple conforme.
- Conventions absentes / ambiguës / contradictoires → **demander** avant de propager.
- Écart cible vs legacy → aligner vers la cible et signaler la dette restante.

### Outils déterministes avant le LLM pour le texte structuré

Si le texte suit un motif répétitif : `rg` / regex / script d'abord. LLM seulement pour le flou (prose, décision, diagnostic). Ne pas dumper un fichier entier pour une recherche outil.

### Sourcer toute proposition d'implémentation non triviale

Pour toute proposition non triviale, indiquer la source :
- fichier existant du projet → `path:line` ;
- doc / framework / RFC → nommer la source ;
- choix propre de l'agent → le dire.
Pas pour fixes triviaux ni changements qui suivent déjà un pattern local.
```

---

## Copie bootstrap.mdc

Fichier cible : `.cursor/rules/bootstrap.mdc` — copier **tel quel**.

```
---
description: Contexte projet et Méthode — attache PROJET.md + lessons.md ;
alwaysApply: true
---

Contexte projet (source unique, attachée automatiquement) :

@memoire/PROJET.md

Méthode — leçons (toujours appliquer) :

@tasks/lessons.md
```

---

## Copie opencode.jsonc

Fichier cible : `opencode.jsonc` — copier **tel quel** (équivalent OpenCode de `bootstrap.mdc`).

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Contexte injecté à chaque session (équivalent .cursor/rules/bootstrap.mdc)
  "instructions": [
    "memoire/PROJET.md",
    "tasks/lessons.md"
  ]
}
```

---

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

> **Savoir projet** (domaine, stack, concepts métier). Injecté automatiquement avec `tasks/lessons.md` (méthode) :
> - **Cursor** : `.cursor/rules/bootstrap.mdc`
> - **OpenCode** : `opencode.jsonc` → `instructions`
>
> Règles de lecture des annexes [`CONVENTIONS.md`](CONVENTIONS.md) / [`ARCHITECTURE.md`](ARCHITECTURE.md) : voir `tasks/lessons.md`.

## But du projet

<!-- Décrire en quelques phrases : quoi, pour qui, quel problème résolu. -->

## Stack technique

| Couche          | Technologie |
| --------------- | ----------- |
| Backend         |             |
| Base de données |             |
| Frontend        |             |
| Tests           |             |
| Build           |             |

## Concepts métier essentiels

<!-- Lister les 3-5 concepts clés du domaine que l'agent doit connaître pour travailler efficacement. -->
```

---

## Template CONVENTIONS.md

Fichier cible : `memoire/CONVENTIONS.md`

```markdown
# [NOM_PROJET] — Conventions du projet

> Annexe de [`PROJET.md`](PROJET.md). Conditions de lecture : voir `tasks/lessons.md`.

<!-- Ajouter ici les conventions au fil des sessions : style de code, nommage, patterns de test, checklists, pièges connus. -->
```

---

## Template ARCHITECTURE.md

Fichier cible : `memoire/ARCHITECTURE.md`

```markdown
# [NOM_PROJET] — Architecture détaillée

> Annexe de [`PROJET.md`](PROJET.md). Conditions de lecture : voir `tasks/lessons.md`.

<!-- Ajouter ici la cartographie des packages, les patterns structurants, les flux de données. -->
```

---

## Template INDEX

Fichier cible : `memoire/session/INDEX.md`

Adapter la légende de tags au domaine du projet.

```markdown
# Index des sessions

> Une ligne par session, la plus récente en haut.

**Tags** (plusieurs par session, séparés par des virgules) :

| Tag           | Signification                              |
| ------------- | ------------------------------------------ |
| `backend`     | API, services, modèles, base de données    |
| `frontend`    | UI, composants, routing                    |
| `tests`       | Tests unitaires, intégration, CI           |
| `docs`        | Documentation, mémoire, règles agent       |
| `infra-agent` | Outils et workflow agent IA                |

| Date       | Tags | Session | Résumé |
| ---------- | ---- | ------- | ------ |
```
