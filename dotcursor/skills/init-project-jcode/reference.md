# Référence — init-project-jcode

Templates **jcode-only**. Pour todo / lessons / ANNEXE / CONVENTIONS / ARCHITECTURE / INDEX : copier depuis [`../init-project/reference.md`](../init-project/reference.md) (snapshot lessons unique, synchronisé par `lessons-export.sh`).

Le **bootstrap générique** (lire PROJET + ANNEXE + lessons) est dans `~/AGENTS.md` via `install-jcode.sh` / `config-cursor/dotjcode/AGENTS.md` — **pas** dans un `./AGENTS.md` projet par défaut.

---

## Copie AGENTS.md (optionnel — exceptions projet seulement)

Fichier cible : `AGENTS.md` (racine) — **ne pas créer** sauf demande explicite d’overrides locaux. Le bootstrap standard est déjà global.

```markdown
# Overrides projet (jcode)

> Complément **local** à `~/AGENTS.md`. Ne pas y recopier le bootstrap générique
> (PROJET / ANNEXE / lessons) — il est déjà injecté globalement.

<!-- Exceptions propres à ce repo uniquement. -->
```

---

## Template PROJET.md

Fichier cible : `memoire/PROJET.md`

```markdown
# [NOM_PROJET] — Contexte projet pour agent IA

> **Savoir projet** (domaine, stack, concepts métier). Lu au démarrage avec [`ANNEXE.md`](ANNEXE.md) et `tasks/lessons.md` (méthode) :
> - **jcode** : bootstrap générique dans `~/AGENTS.md` (via `install-jcode.sh`)
> - **Cursor** : `.cursor/rules/bootstrap.mdc` · **OpenCode** : `opencode.jsonc` → `instructions`
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
