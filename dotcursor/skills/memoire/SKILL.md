---
name: memoire
description: Maintains and expands memoire documentation for harness-based repositories. Use when the user asks to fill or update memoire docs, create specialized annexes, or define reading triggers in memoire/ANNEXE.md.
disable-model-invocation: true
---

# memoire

Rédige et maintient la documentation `memoire/` d’un repo (spines + annexes spécialisées), puis met à jour le catalogue de triggers dans `memoire/ANNEXE.md`.

## Entrée

Appliquer ce skill quand l’utilisateur demande par exemple :

- remplir / enrichir `memoire/`
- maintenir toutes les docs `memoire/`
- créer de nouvelles annexes spécialisées
- ajouter/ajuster les triggers de lecture dans `memoire/ANNEXE.md`

## Workflow

Copier cette checklist et la cocher pendant l’exécution :

```md
- [ ] 1. Audit initial memoire/
- [ ] 2. Extraire les invariants depuis le code
- [ ] 3. Mettre à jour les spines
- [ ] 4. Décider les annexes spécialisées à créer/mettre à jour
- [ ] 5. Mettre à jour ANNEXE.md (triggers, exclusions, dépendances)
- [ ] 6. Vérifier cohérence et récapituler
```

### 1) Audit initial memoire/

Vérifier l’existence de :

- `memoire/PROJET.md`
- `memoire/ANNEXE.md`
- `memoire/CONVENTIONS.md`
- `memoire/ARCHITECTURE.md`

Si un spine manque, le créer avec la structure du projet courant (sans inventer de techno absente).

### 2) Extraire les invariants depuis le code

Lire d’abord les points à forte valeur :

- fichier build principal (`build.gradle*`, `pom.xml`, etc.)
- dossiers source principaux
- tests
- intégration/CI

Documenter uniquement des faits vérifiables dans le repo.

### 3) Mettre à jour les spines

Mettre à jour :

- `PROJET.md` : but, stack, concepts métier, entrées clés, hors-périmètre
- `CONVENTIONS.md` : conventions de code/tests/build observées
- `ARCHITECTURE.md` : cartographie packages/modules, patterns structurants, flux

Règles :

- rester minimal et actionnable
- éviter les inventaires temporaires
- ne pas écrire de conventions non observées

### 4) Annexes spécialisées : décision

Créer (ou scinder) une annexe spécialisée si les 3 conditions sont vraies :

1. domaine avec trigger distinct ;
2. domaine récurrent dans les missions ;
3. contenu trop dense/hétérogène dans les spines.

Ne pas créer d’annexe pour un ticket isolé, un état temporaire, ou une note jetable.

### 5) Mettre à jour `ANNEXE.md`

Pour chaque annexe spécialisée, ajouter :

- **Triggers** : quand la lire
- **Exclusions** : quand ne pas la lire
- **Dépendances** : quelles autres annexes charger avec elle

Les triggers sont cumulatifs. Ne pas ouvrir d’autres annexes “au cas où”.

Utiliser le gabarit dans [reference.md](reference.md).

### 6) Vérifier et récapituler

Avant de conclure :

- vérifier que toutes les annexes référencées dans `ANNEXE.md` existent ;
- vérifier qu’aucun placeholder vide ne reste dans les docs touchées ;
- vérifier que les règles écrites correspondent au code actuel.

Puis fournir un récapitulatif :

- docs modifiées/créées ;
- nouvelles annexes spécialisées ;
- triggers ajoutés/modifiés ;
- éventuels points à compléter par l’équipe.

## Contraintes

- Ne jamais modifier `tasks/lessons.md`.
- Éviter les changements hors périmètre `memoire/` sauf demande explicite.
- Préférer des mises à jour incrémentales lisibles plutôt qu’une prose longue.
