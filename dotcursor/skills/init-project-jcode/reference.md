# Référence — init-project-jcode

Templates **jcode-only**. Pour todo / lessons / ANNEXE / CONVENTIONS / ARCHITECTURE / INDEX : copier depuis [`../init-project/reference.md`](../init-project/reference.md) (snapshot lessons unique, synchronisé par `lessons-export.sh`).

Le **bootstrap générique** (lire PROJET + ANNEXE + lessons) est dans `~/.jcode/prompt-overlay.md` via `install-jcode.sh` / `config-cursor/dotjcode/AGENTS.md` — **jamais** de `./AGENTS.md` projet ni de `~/AGENTS.md`.

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
