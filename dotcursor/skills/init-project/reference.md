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

Fichier cible : `tasks/lessons.md` — copier **tel quel** (socle de méthode transversal ; lecture seule pour l'agent).

```markdown
# Lessons — méthode de l'agent

### Politique git

Lecture libre ; écriture (`commit`, `push`, `rebase`…) **uniquement sur demande explicite**, en fin de tâche, **proposer** un message de commit. Dès la planification d'une nouvelle mission, verifier l'état du worktree et en discuter avec l'utilisateur. Si le sujet est assez gros, proposer demblé un découpage en **plusieurs petites MR** enchaînées.

### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
- Fin de plan = Review dans `tasks/todo.md` et leçons dans `memoire/` si besoin — pas de rapport à cette étape.
- Clôture = demande utilisateur → skill `cloture-session` → **nouveau** fichier.
- Nommage rapport : `AAAA-MM-JJ_HHmm_slug.md` (horloge locale).

### Ne pas transformer une dette legacy en « convention » sans vérifier la cible à jour

- Avant d'aligner sur un pattern existant : vérifier la convention **cible** (`CONVENTIONS.md`, `ARCHITECTURE.md`) vs **dette**.
- Ne pas présenter un usage observé comme convention sans source normative récente ou exemple conforme.
- Conventions absentes / ambiguës / contradictoires → **demander** avant de propager.
- Écart cible vs legacy → aligner vers la cible et signaler la dette restante.

### Mémoire projet : préférer les invariants aux inventaires

- Documenter les règles, contrats et frontières utiles à une prochaine mission.
- Éviter les compteurs, dates d'inventaire et états de branche qui deviennent faux sans signal.
- En conflit documentaire, conserver le contenu aligné sur le code actuel et supprimer les faits périmés.
- Enrichir ou pruner l'annexe spécialisée pendant la mission ; ne pas dupliquer le même fait dans une spine
générale et une annexe.

### Commentaires existants : conserver ou reformuler, ne pas effacer sans raison

Lors d'une réécriture : **ne pas supprimer** les commentaires métier préexistants. Si le code autour change, **reformuler** pour rester exact ; n'enlever un commentaire que s'il est faux *et* sans valeur (sinon reformuler). 

### Être critique avec l'utilisateur, pas complaisant

Traiter chaque affirmation de l'utilisateur comme une **hypothèse à tester**, pas comme une vérité à valider. Ne jamais acquiescer pour faire plaisir. Chercher activement le contre-exemple (code, doc cible, autre couche, gabarit contraire) avant de conclure ; si l'utilisateur a tort ou est trop absolu, le dire clairement avec la preuve.
```

---

## Copie bootstrap.mdc

Fichier cible : `.cursor/rules/bootstrap.mdc` — copier **tel quel**.

```
---
description: Contexte projet, catalogue d'annexes et méthode ;
alwaysApply: true
---

@memoire/PROJET.md
— Objectif : savoir projet minimal (domaine, stack, concepts métier) pour situer la mission. Pas de méthode agent.

@memoire/ANNEXE.md
— Objectif : décider quelles annexes `memoire/` lire pour chaque mission (triggers). Ne pas ouvrir le reste « au cas où ».

@tasks/lessons.md
— Objectif : contraintes opérationnelles inter-projets. Lecture seule ; write-backs sous `memoire/` uniquement.
```

---

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

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

## Template ANNEXE.md

Fichier cible : `memoire/ANNEXE.md`

Catalogue des conditions de lecture. Adapter les triggers au repo ; ajouter une entrée par annexe spécialisée.

```markdown
# [NOM_PROJET] — Catalogue des annexes

## Architecture

- **[`CONVENTIONS.md`](CONVENTIONS.md)** — Lire pour une implémentation non triviale transverse ou si
  aucune annexe spécialisée ne couvre la convention. Ignorer pour question, audit ou correction triviale.
- **[`ARCHITECTURE.md`](ARCHITECTURE.md)** — Lire pour interaction multi-modules, nouvelle frontière ou
  nouveau pattern. Ignorer si cible et pattern sont déjà identifiés.

## Cycle de vie d’une annexe

- **Créer ou scinder** si un domaine possède un trigger distinct, revient dans plusieurs missions et rend
  une annexe existante hétérogène ou conflictuelle. Ne pas créer pour un ticket, une entité isolée, un
  inventaire ou un état temporaire.
- Toute création doit déplacer le contenu sans duplication, ajouter ici ses triggers, exclusions et
  dépendances, puis mettre à jour les spines concernées.
- **Fusionner ou supprimer** si l’annexe n’a plus de trigger propre, ne contient plus de règle durable,
  duplique une autre source ou n’est plus utile après un changement d’architecture.
- Avant suppression, déplacer les seules règles encore valides vers l’annexe cible, retirer ici l’entrée
  et les liens entrants, puis vérifier qu’aucune référence au fichier ne subsiste.
- Le nom décrit un domaine stable (`CONVENTIONS.md`, `ARCHITECTURE.md`), jamais une branche, un ticket ou une date.

## Historique

`memoire/session/` n’est pas normatif : lire seulement pour reprendre explicitement un travail passé ou
suivre un lien depuis une annexe déclenchée.
```

---

## Template CONVENTIONS.md

Fichier cible : `memoire/CONVENTIONS.md`

```markdown
# [NOM_PROJET] — Conventions du projet

<!-- Ajouter ici les conventions au fil des sessions : style de code, nommage, patterns de test, checklists, pièges connus. -->
```

---

## Template ARCHITECTURE.md

Fichier cible : `memoire/ARCHITECTURE.md`

```markdown
# [NOM_PROJET] — Architecture détaillée

<!-- Ajouter ici la cartographie des packages, les patterns structurants, les flux de données. -->
```

