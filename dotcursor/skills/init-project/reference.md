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

### Git : lecture libre, écriture interdite

Ne **jamais** faire de commit (ni de `push`, `rebase`, `reset`… — toute écriture dans l'historique) **sauf demande explicite** (« fait un commit », « committe ça ») — alors exécuter directement. Sinon : lire librement l’état git (`status` / `diff` / `log`) quand utile ; **proposer** un message en fin de tâche — l’utilisateur committe.

### Worktrees : principal si libre ; sinon un agent = un worktree = un `tasks/todo.md`

- Confirmer le **worktree actif** ; toute action reste dans ce root.
- **Toujours demander** avant de créer un worktree **ou** une branche.
- Si accordé et principal libre → changer de branche **sur place** ; worktree secondaire **seulement** si le principal est occupé ; un agent = un worktree = un `tasks/todo.md` local.

### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
- Fin de plan = Review dans `tasks/todo.md` et màj du plan (+ leçons `memoire/` si besoin) — pas de rapport à cette étape.
- Clôture = demande utilisateur → skill `cloture-session` → **nouveau** fichier ; Template dans `cloture-session/reference.md`.
- Nommage rapport : `AAAA-MM-JJ_HHmm_slug.md` (horloge locale).

### Annexes projet : appliquer le catalogue attaché

- Le bootstrap du projet doit attacher le catalogue qui porte les conditions de lecture des annexes.
- Lire immédiatement toutes les annexes dont le trigger correspond à la mission ; les triggers sont cumulatifs.
- Ne pas ouvrir les autres annexes « au cas où ».
- Les rapports de session sont historiques : les lire seulement pour reprendre explicitement un travail passé
  ou lorsqu'une annexe déclenchée y renvoie.

### Ne pas transformer une dette legacy en « convention » sans vérifier la cible à jour

- Avant d'aligner sur un pattern existant : vérifier la convention **cible** (`CONVENTIONS.md`, `ARCHITECTURE.md`) vs **dette**.
- Ne pas présenter un usage observé comme convention sans source normative récente ou exemple conforme.
- Conventions absentes / ambiguës / contradictoires → **demander** avant de propager.
- Écart cible vs legacy → aligner vers la cible et signaler la dette restante.

### Outils déterministes avant le LLM pour le texte structuré

Si le texte suit un motif répétitif : `rg` / regex / script d'abord. LLM seulement pour le flou (prose, décision, diagnostic). Ne pas dumper un fichier entier pour une recherche outil.

### Vérifier à la source avant d'affirmer

Ne jamais affirmer un fait vérifiable (contenu d'un doc ou d'une rule, version, comportement runtime) de mémoire ou par déduction : le vérifier à la source **actuelle** avant de l'écrire — une doc peut être en retard sur la réalité. Un **fait terrain** observé par l'utilisateur (log, écran, résultat de commande) prime : re-vérifier au lieu de défendre la conclusion. Une **interprétation / verdict** de l'utilisateur n'est pas un fait terrain — la leçon suivante s'applique.

### Être critique avec l'utilisateur, pas complaisant

Traiter chaque affirmation de l'utilisateur comme une **hypothèse à tester**, pas comme une vérité à valider. Ne jamais acquiescer pour faire plaisir. Chercher activement le contre-exemple (code, doc cible, autre couche, gabarit contraire) avant de conclure ; si l'utilisateur a tort ou est trop absolu, le dire clairement avec la preuve. Ne pas être contradictoire sur le trivia (typo, reformulation) — viser les claims qui orientent une décision technique.

### Mémoire projet : préférer les invariants aux inventaires

- Documenter les règles, contrats et frontières utiles à une prochaine mission.
- Éviter les compteurs, dates d'inventaire et états de branche qui deviennent faux sans signal.
- En conflit documentaire, conserver le contenu aligné sur le code actuel et supprimer les faits périmés.
- Enrichir ou pruner l'annexe spécialisée pendant la mission ; ne pas dupliquer le même fait dans une spine
  générale et une annexe.
```

---

## Copie bootstrap.mdc

Fichier cible : `.cursor/rules/bootstrap.mdc` — copier **tel quel**.

```
---
description: Contexte projet, catalogue d'annexes et méthode ;
alwaysApply: true
---

Contexte projet (source unique, attachée automatiquement) :

@memoire/PROJET.md

Catalogue projet — conditions de lecture des annexes :

@memoire/ANNEXE.md

Méthode — leçons (toujours appliquer) :

@tasks/lessons.md
```

---

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

> **Savoir projet** (domaine, stack, concepts métier). Injecté automatiquement avec [`ANNEXE.md`](ANNEXE.md) et `tasks/lessons.md` (méthode) :
> - **Cursor** : `.cursor/rules/bootstrap.mdc`
>
> Conditions de lecture des annexes : [`ANNEXE.md`](ANNEXE.md) ; `tasks/lessons.md` porte uniquement la méthode inter-projet.

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

> Source unique des conditions de lecture de `memoire/`.
> Lire immédiatement toutes les annexes déclenchées ; les triggers sont cumulatifs.
> Ne pas ouvrir une annexe « au cas où ».

Toujours chargés par le bootstrap : [`PROJET.md`](PROJET.md), ce catalogue et `tasks/lessons.md`.

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

> Annexe de [`PROJET.md`](PROJET.md). Conditions de lecture : [`ANNEXE.md`](ANNEXE.md).

<!-- Ajouter ici les conventions au fil des sessions : style de code, nommage, patterns de test, checklists, pièges connus. -->
```

---

## Template ARCHITECTURE.md

Fichier cible : `memoire/ARCHITECTURE.md`

```markdown
# [NOM_PROJET] — Architecture détaillée

> Annexe de [`PROJET.md`](PROJET.md). Conditions de lecture : [`ANNEXE.md`](ANNEXE.md).

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
