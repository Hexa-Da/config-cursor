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

- **Symptôme** : ce qui a été corrigé par l'utilisateur
- **Cause** : pourquoi l'agent s'est trompé
- **Règle** : comment l'éviter la prochaine fois

---



### Git : lecture libre, écriture interdite

- **Symptôme** : risque qu'un agent committe (ou s'abstienne de consulter git par excès de prudence).
- **Cause** : frontière lecture/écriture non explicitée.
- **Règle** : ne **jamais** faire de commit (ni `commit`, `push`, `rebase`, `reset`... — toute écriture dans l'historique) **sauf demande explicite de l'utilisateur** (« fait un commit », « committe ça ») — dans ce cas, exécuter directement plutôt que de reproposer un message à valider. En dehors de toute demande explicite : consulter le worktree aussi souvent qu'utile (`git status`, `git diff`, `git log`...) est libre et encouragé, et **proposer un message de commit** à l'utilisateur en fin de tâche cohérente — c'est lui qui committe.




### Worktrees parallèles : un agent = un worktree = un `tasks/todo.md`

- **Symptôme** : plusieurs agents lancés sur des missions/branches différentes se marchent dessus — reprise du plan d'un autre agent, écrasement de `tasks/todo.md`, mélange de contexte entre le worktree principal et un worktree secondaire.
- **Cause** : l'agent suppose un repo unique et réutilise le `tasks/todo.md` ou le fil de travail d'une autre session, sans ancrage explicite sur **le worktree courant**.
- **Règle** :
  - Au démarrage d'une mission non triviale : confirmer le **worktree actif** (`Workspace Path`, `git rev-parse --show-toplevel`, branche courante). Toute action reste **strictement** dans ce répertoire — ne jamais lire/éditer un `tasks/todo.md` hors de ce root.
  - Si l'agent est lancé dans un **worktree distinct du principal** (autre branche, autre mission parallèle) : **créer ou réinitialiser** un `tasks/todo.md` **local à ce worktree**, dédié à **cette** mission. **Ne pas** reprendre, compléter ni écraser le `tasks/todo.md` du worktree principal ni celui d'un autre agent.
  - En tête du todo : rappeler branche + objectif de la mission (ex. `# tech/foo — …`) pour éviter toute confusion inter-agents.
  - Ne pas fusionner plans, reviews ni todos entre agents/worktrees parallèles ; chaque agent clôt sa propre section Review dans **son** todo.
  - En cas de doute sur quel worktree/todo utiliser : **questionner l'utilisateur** avant d'écrire dans `tasks/`.




### Ne pas lancer l'environnement ni les tests lourds pour « vérifier » — dire quoi tester

- **Symptôme** : l'agent démarre des services (DB, serveur dev, stack complète) ou lance des suites de tests lourdes de son propre chef, attend un terminal qui bloque ou time out, puis reste muet ou retente en boucle — au lieu de dire à l'utilisateur quoi lancer.
- **Cause** : réflexe de « prouver » le travail en autonomie, alors que l'environnement local de l'utilisateur (réseau interne, outillage IDE, dépendances lourdes) n'est souvent pas fiable ni disponible pour l'agent.
- **Règle** :
  - Ne **jamais** lancer l'environnement complet ni les suites de tests lourdes de son propre chef, sauf demande explicite de l'utilisateur.
  - Si la vérification runtime est nécessaire : **dire immédiatement quoi tester** (commande ciblée du projet, test ou script précis, résultat attendu) — ne pas attendre passivement un terminal bloqué ni enchaîner les relances sans retour à l'utilisateur.
  - En fin de tâche, fournir une **checklist de vérif concise** : quoi lancer, combien de tests attendus, durée indicative (tests rapides vs intégration lourde).
  - Des vérifications ciblées côté agent restent OK sans demander à l'utilisateur : lecture de code, lint, compilation locale si rapide et fiable.



### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Symptôme** : l'agent crée ou édite `memoire/session/*.md` / `INDEX.md` en fin de plan (« Doc session »), ou met à jour un rapport clos, sans demande de clôture.
- **Cause** : confusion entre Review Cherny (`tasks/todo.md`) et skill `cloture-session` ; règle projet trop centrée sur la *lecture* des annexes.
- **Règle** :
  - **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
  - Fin de plan = section Review dans `tasks/todo.md` (+ leçons durables si besoin). Pas de nouveau rapport, pas de retouche d'un ancien.
  - Clôture = seulement si l'utilisateur le demande → skill `cloture-session` → **nouveau** fichier + ligne INDEX ; **jamais** modifier un rapport déjà écrit.
  - Dans le rapport : pour chaque commit, message de commit complet — template dans `cloture-session/reference.md`.



### Ne pas relire les annexes `memoire/` à chaque tour ni les ignorer par défaut

- **Symptôme** : l'agent relit `memoire/CONVENTIONS.md` / `ARCHITECTURE.md` à chaque tour même pour un fix trivial (coût token inutile), ou au contraire ne les ouvre jamais avant du code non trivial, faute de critère de déclenchement clair.
- **Cause** : pas de règle explicite distinguant les cas où lire vs ne pas lire ; ces conditions sont génériques donc relèvent de la méthode, pas du savoir projet.
- **Règle** :
  - `memoire/CONVENTIONS.md` — lecture avant d'écrire ou modifier du code **non trivial** (nouvelle fonctionnalité, nouveau fichier, migration, test) ou en cas de doute sur un pattern existant. **Ne pas lire** pour : audit / analyse en lecture seule, question ponctuelle, discussion, fix d'une ligne, typo, valeur de config. Une fois lue dans la session, ne pas la relire à chaque tour — seulement si la tâche change de domaine.
  - `memoire/ARCHITECTURE.md` — lecture si la tâche implique de comprendre l'**interaction entre plusieurs composants/modules**, d'ajouter un **nouveau composant ou pattern**, ou de traverser une **frontière de module** — indépendamment du nombre de fichiers estimé au départ. Si la portée réelle dépasse l'estimation initiale en cours de tâche, la lire à ce moment-là plutôt que d'avoir tranché trop tôt.
  - `memoire/session/` (INDEX + rapports) — à lire seulement pour reprendre un travail passé (sur demande explicite).



### Ne pas transformer une dette legacy en « convention » sans vérifier la cible à jour

- **Symptôme** : l'agent justifie un choix d'implémentation en s'appuyant sur un composant existant ou un pattern répandu, alors que ce code peut justement être de la dette en cours de résorption.
- **Cause** : confusion entre « usage courant dans le codebase » et « convention cible à jour » ; absence de vérification explicite de la source normative avant de propager le pattern.
- **Règle** :
  - Avant d'aligner un composant legacy sur un autre composant, **vérifier d'abord** si la convention projet à jour est documentée (`memoire/CONVENTIONS.md`, `ARCHITECTURE.md`, annexe pertinente) et distinguer clairement **cible** vs **dette existante**.
  - Ne pas présenter un pattern observé dans le code comme une convention sans pouvoir le rattacher à une source normative récente ou à un exemple explicitement conforme.
  - Si les conventions paraissent absentes, ambiguës, contradictoires, ou possiblement dépassées, **questionner l'utilisateur** avant de propager ce pattern à d'autres fichiers.
  - En cas d'écart entre convention cible et implémentation legacy, privilégier l'alignement vers la cible et signaler explicitement la dette restante plutôt que de la faire persister.
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
