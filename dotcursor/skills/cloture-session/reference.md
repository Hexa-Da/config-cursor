# Référence — clôture de session

## Critères d'une leçon durable

**Réutilisable** : la leçon doit rester valable une fois dépouillée des noms de champs/tickets précis (ex. « migrer un champ legacy vers un nouveau modèle » plutôt que la checklist complète avec les noms de champs du ticket). Si elle ne survit pas à cette généralisation, c'est une recette ponctuelle : elle **n'est pas documentée**.

Une leçon réutilisable est promue si elle répond en plus **oui** à au moins un de ces critères :

- **Piège récurrent** : erreur ou oubli déjà rencontré, ou très probable (ex. maillon manquant dans une chaîne technique).
- **Chaîne opaque** : liste de fichiers/étapes difficile à deviner sans avoir déjà fait la tâche une fois.
- **Décision structurante** : convention, invariant ou composant pivot du projet.

## Avant de reporter : éviter doublons et dérive « journal de tickets »

`memoire/CONVENTIONS.md` / `memoire/ARCHITECTURE.md` sont lus à (presque) chaque session, quel que soit son sujet : chaque ligne ajoutée est un coût pour toutes les sessions futures, même sans rapport avec le sujet traité. Avant de reporter :

1. **Chercher un doublon** : si le sujet existe déjà (même partiellement) dans le document cible, mettre à jour la section existante au lieu d'en créer une nouvelle — jamais deux endroits pour la même notion.
2. **Rester au niveau du document cible** : dans `ARCHITECTURE.md`, s'arrêter au niveau package/pattern/flux (pas de détail composant par composant d'une seule page ou feature) ; dans `CONVENTIONS.md`, une entrée doit valoir pour n'importe quelle feature future, pas une seule.

## Où reporter une leçon durable

| Nature de la leçon                               | Document cible                    | Exemple                                                                         |
| ------------------------------------------------ | --------------------------------- | ------------------------------------------------------------------------------- |
| Checklist procédurale, convention de code, piège | `memoire/CONVENTIONS.md`          | checklist multi-couches d'ajout d'une donnée (modèle → migration → UI → export) |
| Rôle d'un package, pattern, flux technique       | `memoire/ARCHITECTURE.md`         | pattern de composants, flux de génération de code                               |
| Méthode de travail (valable tous projets)        | `tasks/lessons.md`                | test de tri en tête du fichier — jamais dans `memoire/`                         |

---

## Template rapport

Fichier cible : `memoire/session/AAAA-MM-JJ_titre-de-la-session.md`

```markdown
# [Titre de la session]

- **Date** : AAAA-MM-JJ
- **Branche** : `nom-de-la-branche` (si pertinent)

## Contexte et objectif

Pourquoi cette session ? Quel était le besoin ou le problème de départ ?
Une à trois phrases.

## Changements effectués

Pour chaque changement significatif :
1. Expliquer le pourquoi, avec assez de contexte pour qu'une future lecture reste compréhensible.
2. Expliquer le lien avec le reste de la chaîne (backend, frontend, Mongo, OpenAPI, export, tests...).
3. Lister ensuite les fichiers touchés (sans que ça prenne le dessus).
4. Si un commit existe : hash + message complet.

### [Changement 1]

- **Pourquoi** : ...
- **Lien avec le reste** : ...
- **Fichiers** :
  - `dossier/fichier1.extension`
  - `autre-dossier/fichier2.extension`
- **Commit** : `hash` — `message de commit complet`

### [Changement 2]

- **Pourquoi** : ...
- **Lien avec le reste** : ...
- **Fichiers** :
  - `dossier/fichier3.extension`
- **Commits** :
  - `hash1` — `premier message`
  - `hash2` — `second message`
```

---

## INDEX — format de ligne

Dans le fichier `memoire/session/INDEX.md`, ajouter une ligne **en première position** du tableau (sous l'en-tête) :

```markdown
| AAAA-MM-JJ | `tag1`, `tag2` | [Titre de la session](AAAA-MM-JJ_titre-de-la-session.md) | Résumé en une phrase. |
```

---

## Template todo

Fichier cible après reset : `tasks/todo.md`

```markdown
# Todo — tâche en cours

> Plan de travail de la session qui suit les Cherny's rules. Distinct de `memoire/`.

## Tâche



## Plan

- [ ] Étape 1
- [ ] Étape 2
- [ ] Étape 3

## Review

```
