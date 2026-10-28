# Reference — memoire

## Gabarit d’entrée ANNEXE.md

```md
- **[`NOM_ANNEXE.md`](NOM_ANNEXE.md)**
  - Triggers : <conditions de lecture>
  - Exclusions : <cas où ne pas lire>
  - Dépendances : <annexes à lire en complément>
```

## Grille rapide de décision "nouvelle annexe ?"

Créer une annexe si :

- le domaine a un vocabulaire/protocole propre ;
- les règles changent différemment du reste ;
- au moins 2 types de missions futures sont probables sur ce domaine.

Ne pas créer si :

- c’est une correction ponctuelle ;
- le contenu tient en 3-8 lignes dans `CONVENTIONS.md` ou `ARCHITECTURE.md` ;
- le sujet dépend d’une branche ou d’une date.

Appliquer aussi, s’il existe, le cycle de vie / règles du `ANNEXE.md` du projet
cible.

## Grille rapide "prune annexe / pan de spine ?"

Candidat prune si **les deux** :

- plus de code, chemin ou concept correspondant dans le repo ;
- plus de trigger plausible dans `ANNEXE.md`.

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
