---
name: context-budget
description: >-
  Audits always-on vs on-demand token overhead of the Cursor agent harness
  (user rules, AGENTS.md, alwaysApply rules, skills catalog, MCP). Produces a
  classified report and prioritized cuts. Use when the user asks for a
  context-budget audit, token budget of the workflow, or why the context
  window fills too fast.
disable-model-invocation: true
---

# Context Budget

Audit ponctuel du harness Cursor. Ne pas laisser cette skill always-on : elle
mesure ce qui est déjà chargé.

## Checklist

```
- [ ] 1. Lancer scripts/estimate.py sur le workspace
- [ ] 2. Classer chaque composant (keep / on-demand / trop gros)
- [ ] 3. Produire le rapport + top 3 coupes
```

## 1. Inventaire

Depuis la racine du projet audité :

```bash
python3 ~/.cursor/skills/context-budget/scripts/estimate.py
```

Le script compte les fichiers présents (skip silencieux si absents). Heuristique :
prose `mots × 1.3`, code/JSON `chars / 4`.

**Always-on (chaque session Agent)**

| Composant | Où |
| --- | --- |
| User Rules | Customize → Rules (pas un fichier). Canon versionné : `AGENTS.md` à la racine de config-cursor — le script le prend comme proxy (**1×**). OpenCode lit le même texte via `~/.config/opencode/AGENTS.md` (miroir `install.sh`) : autre runtime, **ne pas compter** dans un audit Cursor. |
| `AGENTS.md` workspace | Seulement si **distinct** du canon (chemin ou contenu projet). Dans config-cursor, le fichier racine *est* le canon → déjà compté en User Rules. Imbriqués = on-demand. Voir aussi `CLAUDE.md` / `.cursorrules`. |
| Rules Always Apply | `.cursor/rules/**/*.mdc` avec `alwaysApply: true`, plus les fichiers `@attachés` dans le corps |
| Attachés bootstrap | Seulement s'ils sont `@` depuis une rule always-on (ex. `memoire/PROJET.md`, `tasks/lessons.md`) |
| Skill catalog | `name` + `description` des skills **sans** `disable-model-invocation: true`, plus le catalogue built-in `~/.cursor/skills-cursor/` (descriptions seulement ; les corps built-in ne sont pas listés) |
| MCP | `~/.cursor/mcp.json` **et** `.cursor/mcp.json` — ~500 tokens par outil ; sans liste live le script estime 4 outils / serveur |

**Pas dans le prompt (ne pas compter en always-on)**

- `AGENTS.md` canon sur disque dans config-cursor — versioning + miroir OpenCode, pas une seconde couche Cursor si User Rules sont à jour
- `hooks.json` / scripts de hooks — exécutés hors LLM (sauf hook qui *injecte* du contexte)
- Corps des skills `disable-model-invocation: true` tant qu'elles ne sont pas invoquées (`/` ou `@`)
- Rules glob / Apply Intelligently / manuelles
- `memoire/CONVENTIONS.md`, `ARCHITECTURE.md`, annexes, `memoire/session/`

Skills découvertes : `~/.cursor/skills`, `~/.agents/skills`, `.cursor/skills/`, `.agents/skills/` (y compris imbriqués dans un monorepo).

## 2. Classification

| Seau | Critère | Action |
| --- | --- | --- |
| **Keep always-on** | Contrainte de méthode ou contexte projet minimal | Garder |
| **On-demand** | Procédure / savoir de domaine | Skill `disable-model-invocation: true`, rule glob / intelligente, ou lecture conditionnelle (`lessons.md`) |
| **Trop gros** | Rule >100 lignes, skill >400 lignes, MCP qui wrappe un CLI déjà là (`git`, `gh`/`glab`, `npm`) | Couper, scinder, ou retirer |

Signaux d'alerte :

- Rule / User Rules qui répètent `tasks/lessons.md` (AGENTS.md dit déjà : ne pas restater)
- User Rules (UI) **≠** contenu du canon `AGENTS.md` (dérive après edit repo sans resync)
- Annexe `memoire/` relue alors que la leçon « ne pas relire à chaque tour » s'applique
- Skill **sans** `disable-model-invocation` alors qu'elle n'est utile que sur demande (son `description` reste dans le catalogue)
- MCP avec beaucoup d'outils : souvent le plus gros levier

## 3. Rapport

```
Context Budget
══════════════
Always-on estimé : ~X tokens
Plus gros postes : …

Classification
- Keep : …
- On-demand : …
- Trop gros : …

Top 3 coupes (économie estimée)
1. …
2. …
3. …
```

Ne pas modifier de fichiers pendant l'audit sauf demande explicite. Proposer les
coupes, ne pas les appliquer.

## Exemple

Workspace avec `bootstrap.mdc` (`alwaysApply: true`) qui attache `PROJET.md` +
`lessons.md`, User Rules distinctes, 2 skills perso `disable-model-invocation:
true`, MCP vide → always-on dominé par PROJET.md / lessons.md / AGENTS.md ; les
corps de skills et le catalogue perso ne comptent pas. Coupe typique :
raccourcir PROJET.md, pas ajouter une skill permanente.
