# Reference — memoire

## Gabarit d’entrée ANNEXE.md

```md
- **[`NOM_ANNEXE.md`](NOM_ANNEXE.md)**
  - Triggers : <conditions de lecture>
  - Exclusions : <cas où ne pas lire>
  - Dépendances : <annexes à lire en complément>
```

## Cycle de vie d’une annexe

Méthode du skill `memoire` (pas du catalogue projet). `ANNEXE.md` du repo ne
contient que les entrées (triggers / exclusions / dépendances).

### Créer ou scinder

Créer ou scinder si **toutes** ces conditions :

- le domaine a un vocabulaire / protocole propre ou un trigger de lecture distinct ;
- les règles changent différemment du reste, ou une annexe existante devient
  hétérogène / conflictuelle ;
- au moins 2 types de missions futures sont probables sur ce domaine.

Ne pas créer pour : ticket isolé, entité isolée, inventaire, état temporaire,
correction ponctuelle, contenu qui tient en 3-8 lignes dans `CONVENTIONS.md` ou
`ARCHITECTURE.md`, sujet lié à une branche ou une date.

Toute création doit déplacer le contenu sans duplication, ajouter dans
`ANNEXE.md` ses triggers / exclusions / dépendances, puis mettre à jour les
spines concernées. Le nom décrit un domaine stable (`CONVENTIONS.md`,
`ARCHITECTURE.md`, ou `FOO.md` métier), jamais une branche, un ticket ou une date.

### Fusionner ou supprimer

Fusionner ou supprimer si l’annexe n’a plus de trigger propre, ne contient plus
de règle durable, duplique une autre source, n’est plus utile après un
changement d’architecture, **ou** n’a plus de code / chemin / concept
correspondant **et** plus de trigger plausible dans `ANNEXE.md`.

Avant suppression : déplacer les seules règles encore valides vers l’annexe (ou
spine) cible, retirer l’entrée catalogue et les liens entrants, vérifier qu’aucune
référence au fichier ne subsiste.

Écriture : edits légères / faits faux → direct. Suppressions d’annexes et
fusions lourdes → **proposition** à valider (pas d’écriture silencieuse).

## Gabarit de review final (réponse utilisateur)

```md
Changements réalisés :
- Spines mis à jour : ...
- Annexes créées / mises à jour : ...
- Catalogue ANNEXE.md : ...
- Propositions en attente (prune / fusion) : ... | —

Vérifications :
- Références ANNEXE.md -> fichiers existants : OK/KO
- Cohérence avec le code : OK/KO
- Indices session utilisés (≤10) : ...
- Points à compléter équipe : ...
```
