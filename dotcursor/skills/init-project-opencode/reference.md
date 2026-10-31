# Référence — init-project-opencode

Templates **OpenCode-only**. Pour todo / lessons / ANNEXE / CONVENTIONS / ARCHITECTURE / INDEX : copier depuis [`../init-project/reference.md`](../init-project/reference.md) (snapshot lessons unique, synchronisé par `lessons-export.sh`).

---

## Copie opencode.jsonc

Fichier cible : `opencode.jsonc` — copier **tel quel** (câblage OpenCode ; pas d’équivalent `.cursor` dans ce skill).

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Contexte injecté à chaque session (équivalent .cursor/rules/bootstrap.mdc)
  "instructions": [
    "memoire/PROJET.md",
    "memoire/ANNEXE.md",
    "tasks/lessons.md"
  ]
}
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
