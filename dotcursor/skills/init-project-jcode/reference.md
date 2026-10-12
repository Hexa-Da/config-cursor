# Référence — init-project-jcode

Templates **jcode-only**. Pour todo / lessons / ANNEXE / CONVENTIONS / ARCHITECTURE / INDEX : copier depuis [`../init-project/reference.md`](../init-project/reference.md) (snapshot lessons unique, synchronisé par `lessons-export.sh`).

---

## Copie AGENTS.md

Fichier cible : `AGENTS.md` (racine du repo) — copier **tel quel** (câblage jcode ; équivalent de `opencode.jsonc` / `.cursor/rules/bootstrap.mdc`).

```markdown
# Agent bootstrap (jcode)

> Câblage projet pour jcode. Les règles utilisateur globales viennent de `~/AGENTS.md`
> (via `install-jcode.sh`). Ce fichier injecte uniquement le contexte **projet**.

Toujours lire au démarrage, dans cet ordre :

1. [`memoire/PROJET.md`](memoire/PROJET.md) — savoir projet essentiel
2. [`memoire/ANNEXE.md`](memoire/ANNEXE.md) — catalogue des conditions de lecture des annexes
3. [`tasks/lessons.md`](tasks/lessons.md) — méthode inter-projet (**lecture seule**)

Appliquer le catalogue `ANNEXE.md` : ouvrir immédiatement toute annexe dont le trigger correspond à la mission. Ne pas ouvrir les autres « au cas où ».

Skills installés globalement : `~/.jcode/skills/` (miroir `config-cursor` via `install-jcode.sh`).
```

---

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

> **Savoir projet** (domaine, stack, concepts métier). Injecté automatiquement avec [`ANNEXE.md`](ANNEXE.md) et `tasks/lessons.md` (méthode) :
> - **jcode** : `AGENTS.md` (racine) → lit ces trois fichiers
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
