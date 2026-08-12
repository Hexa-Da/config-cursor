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
- **Règle** : ne **jamais** faire de commit (ni `commit`, `push`, `rebase`, `reset`... — toute écriture dans l'historique). En revanche, consulter le worktree aussi souvent qu'utile (`git status`, `git diff`, `git log`...) est libre et encouragé. Quand c'est pertinent (fin de tâche cohérente), **proposer un message de commit** à l'utilisateur — c'est lui qui committe.



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

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

> **Instructions agent** : point d'entrée unique pour comprendre le projet, attaché automatiquement via `.cursor/rules/bootstrap.mdc` (qui attache aussi `tasks/lessons.md`, qui fixe les règles de lecture de [`CONVENTIONS.md`](CONVENTIONS.md) / [`ARCHITECTURE.md`](ARCHITECTURE.md)).

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
