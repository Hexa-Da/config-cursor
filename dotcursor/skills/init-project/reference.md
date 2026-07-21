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



### Ne pas lancer l'environnement ni les tests lourds pour « vérifier »

- **Symptôme** : l'agent démarre des services (DB, serveur dev, stack complète) ou lance des suites de tests lourdes de son propre chef, sans que l'utilisateur l'ait demandé.
- **Cause** : réflexe de « prouver » le travail en autonomie, alors que l'environnement local de l'utilisateur (ports, secrets, données) n'est pas fiable ni disponible pour l'agent.
- **Règle** : ne jamais lancer l'environnement complet ni les suites de tests lourdes de son propre chef. En fin de tâche, **expliquer à l'utilisateur comment tester** : commande(s) à lancer, comportement attendu à observer. Des vérifications ciblées restent possibles (lecture de code, lint, compilation, un test unitaire précis déjà identifié).
```

---

## Template projet.mdc

Fichier cible : `.cursor/rules/projet.mdc`

```
---
description: Contexte projet — attache memoire/PROJET.md et fixe quand lire les annexes memoire/
alwaysApply: true
---

Contexte projet (source unique, attachée automatiquement) :

@memoire/PROJET.md

## Annexes `memoire/` — lecture à la demande, jamais par défaut

- `memoire/CONVENTIONS.md` : à lire **avant d'écrire du code, des migrations ou des tests**.
- `memoire/ARCHITECTURE.md` : à lire quand la tâche touche à la **structure** (packages, patterns, flux).
- `memoire/session/` (INDEX + rapports) : historique, seulement pour reprendre un travail passé (sur demande).
```

---

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

> **Instructions agent** : point d'entrée unique pour comprendre le projet, attaché automatiquement via `.cursor/rules/projet.mdc` (qui fixe aussi quand lire les annexes `[CONVENTIONS.md](CONVENTIONS.md)` / `[ARCHITECTURE.md](ARCHITECTURE.md)`).

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

> Annexe de [`PROJET.md`](PROJET.md). À lire avant d'écrire du code, des migrations ou des tests.

<!-- Ajouter ici les conventions au fil des sessions : style de code, nommage, patterns de test, checklists, pièges connus. -->
```

---

## Template ARCHITECTURE.md

Fichier cible : `memoire/ARCHITECTURE.md`

```markdown
# [NOM_PROJET] — Architecture détaillée

> Annexe de [`PROJET.md`](PROJET.md). À lire quand une mission touche à la structure du projet.

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
