# Référence — init-project-opencode

Templates **OpenCode-only**. Pour todo / lessons / CONVENTIONS / ARCHITECTURE / INDEX : copier depuis [`../init-project/reference.md`](../init-project/reference.md) (snapshot lessons unique, synchronisé par `lessons-export.sh`).

---

## Copie opencode.jsonc

Fichier cible : `opencode.jsonc` — copier **tel quel** (câblage OpenCode ; pas d’équivalent `.cursor` dans ce skill).

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Contexte injecté à chaque session
  "instructions": [
    "memoire/PROJET.md",
    "tasks/lessons.md"
  ]
}
```

---

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

> **Savoir projet** (domaine, stack, concepts métier). Injecté automatiquement avec `tasks/lessons.md` (méthode) :
> - **OpenCode** : `opencode.jsonc` → `instructions`
>
> Règles de lecture des annexes [`CONVENTIONS.md`](CONVENTIONS.md) / [`ARCHITECTURE.md`](ARCHITECTURE.md) : voir `tasks/lessons.md`.

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
