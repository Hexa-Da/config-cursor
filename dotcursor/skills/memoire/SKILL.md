---
name: memoire
description: >-
  Audits and maintains long-term project memoire/ (spines + annexes): freshness
  vs code, prune obsolete docs, create annexes when warranted. Use when the user
  asks /memoire, to sync or prune memoire, check docs are up to date, or annex
  a domain. Not for session-context compliance (see check-context).
disable-model-invocation: true
---

# memoire

Audit et maintenance **full** de la mémoire long terme `memoire/` (tous sujets,
sans gate de scope) : fraîcheur vs code, utilité des spines/annexes, prune du
périmé, création d’annexe si justifiée. Orthogonal à `cloture-session` (pas
d’enchaînement auto) et à `check-context` (contexte de **session**, pas le
contenu disque de `memoire/`).

## Entrée

Appliquer ce skill quand l’utilisateur demande par exemple :

- `/memoire`
- synchroniser / vérifier / pruner `memoire/`
- docs `memoire/` à jour
- annexer un domaine dans `memoire/`

Toujours en **full** — ne pas attendre une consigne de module ou de « full ».

## Workflow

Copier cette checklist et la cocher pendant l’exécution :

```md
- [ ] 1. Prérequis (spines)
- [ ] 2. Indices session (≤10 rapports)
- [ ] 3. Inventaire docs
- [ ] 4. Cohérence code → docs
- [ ] 5. Utilité / prune
- [ ] 6. Création annexe si justifiée
- [ ] 7. Catalogue ANNEXE.md
- [ ] 8. Récap
```

### 1) Prérequis

Confirmer `memoire/` et les quatre spines :

- `memoire/PROJET.md`
- `memoire/ANNEXE.md`
- `memoire/CONVENTIONS.md`
- `memoire/ARCHITECTURE.md`

Si l’un manque → **stop** ; proposer `init-project` (ou variante canal). Ne pas
bootstrapper les spines ici.

### 2) Indices session

Lister jusqu’à **10** fichiers `memoire/session/AAAA-MM-JJ_HHmm_*.md` les plus
récents (tri par nom). En extraire zones/modules touchés pour **prioriser** le
balayage. Ces rapports ne sont **pas** source normative — le code prime.

### 3) Inventaire docs

Recenser :

- les quatre spines ;
- les annexes listées dans `ANNEXE.md` ;
- les markdown orphelins sous `memoire/` (hors `session/`).

### 4) Cohérence code → docs

Croiser les invariants documentés avec le **code actuel** (prioriser les zones
des indices, puis le reste). Documenter uniquement des faits vérifiables.

Écriture **hybride** :

- **Direct** : fait contredit par le code, lien cassé, doublon spine/annexe
  évident.
- **Proposition** (liste à valider, pas d’écriture) : suppressions d’annexes,
  fusions lourdes.

Préférer les invariants aux inventaires (compteurs, dates d’état, branches).

### 5) Utilité / prune

Candidat prune si : plus de code/chemin/concept correspondant **et** plus de
trigger plausible dans `ANNEXE.md`. Edits légères en direct ; suppressions /
fusions → proposition (étape 4).

### 6) Création annexe

Si un domaine est dense/hétérogène dans les spines (ou ressort des indices +
code) : appliquer la grille « nouvelle annexe ? » dans [reference.md](reference.md)
**et**, s’il existe, le cycle de vie / règles du `ANNEXE.md` du projet.

Si OK : créer le fichier, déplacer le contenu hors spines si besoin, ajouter
l’entrée catalogue (triggers / exclusions / dépendances). Sinon laisser dans
spine. Pas d’annexe pour ticket isolé, état temporaire, ou note jetable.

### 7) Catalogue `ANNEXE.md`

Synchroniser le catalogue avec créations et prunes **validés** ; corriger les
liens cassés directement. Gabarit d’entrée : [reference.md](reference.md).

### 8) Récap

Fournir le récap (gabarit dans [reference.md](reference.md)) : docs touchées,
annexes créées, propositions en attente, points équipe.

## Contraintes

- Ne jamais modifier `tasks/lessons.md`.
- Pas d’écriture hors `memoire/` sauf demande explicite.
- Pas de rapport sous `memoire/session/` (réservé à `cloture-session`).
- Mises à jour incrémentales ; pas de prose longue.
