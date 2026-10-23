# Reference — memoire-docs-maintainer

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

## Gabarit de review final (réponse utilisateur)

```md
Changements réalisés :
- Spines mis à jour : ...
- Annexes spécialisées créées/mises à jour : ...
- Catalogue ANNEXE.md : triggers/exclusions/dépendances ajoutés pour ...

Vérifications :
- Références ANNEXE.md -> fichiers existants : OK/KO
- Cohérence avec le code : OK/KO
- Points à compléter équipe : ...
```
