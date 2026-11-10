# Référence — init-project

Templates des fichiers à générer. Copier tels quels sauf les placeholders `[…]`.

---

## Copie todo

Fichier cible : `tasks/todo.md`

```markdown
# Todo — tâche en cours

> Plan de travail de la session qui suit les Cherny's rules.

## Tâche

<!-- Titre court de la tâche en cours -->

## Plan

- [ ] Étape 1
- [ ] Étape 2
- [ ] Étape 3

## Review

<!-- À remplir en fin de tâche : ce qui a été fait, comment ça a été vérifié, écarts par rapport au plan. -->
```

---

## Copie lessons

Fichier cible : `tasks/lessons.md`

```markdown
# Lessons - friction harnais

<!--
### YYYY-MM-DD — titre court
- Friction : …
- Contexte : (harness / consigne / outil)
- Changement proposé : AGENTS | skill:nom | rien
-->
```

---

## Copie bootstrap.mdc

Fichier cible : `.cursor/rules/bootstrap.mdc`

```
---
description: Contexte projet et catalogue d'annexes ;
alwaysApply: true
---

@memoire/PROJET.md
— Objectif : savoir projet minimal (domaine, stack, concepts métier) pour situer la mission. Pas de méthode agent.

@memoire/ANNEXE.md
— Objectif : décider quelles annexes `memoire/` lire pour chaque mission (triggers). Ne pas ouvrir le reste « au cas où ».
```

---

## Copie context-mode.mdc

Fichier cible : `.cursor/rules/context-mode.mdc`

```
---
description: context-mode routing rules for context window protection
alwaysApply: true
---

# context-mode

Raw tool output floods context window. Use context-mode MCP tools to keep raw data in sandbox.

## Think in Code — MANDATORY

Analyze/count/filter/compare/search/parse/transform data: **write code** via `ctx_execute(language, code)`, `console.log()` only the answer. Do NOT read raw data into context. PROGRAM the analysis, not COMPUTE it. Pure JavaScript — Node.js built-ins only (`fs`, `path`, `child_process`). `try/catch`, handle `null`/`undefined`. One script replaces ten tool calls.

## Tool Selection

0. **MEMORY**: `ctx_search(sort: "timeline")` — after resume, check prior context before asking user.
1. **GATHER**: `ctx_batch_execute(commands, queries)` — runs all commands, auto-indexes, searches. ONE call replaces many steps.
2. **FOLLOW-UP**: `ctx_search(queries: ["q1", "q2", ...])` — all follow-up questions, ONE call (default relevance mode).
3. **PROCESSING**: `ctx_execute(language, code)` | `ctx_execute_file(path, language, code)` — sandbox, only stdout enters context.
4. **WEB**: `ctx_fetch_and_index(url)` then `ctx_search(queries)` — never dump raw HTML.
5. **INDEX**: `ctx_index(content, source)` — store in FTS5 for later search.

## Parallel I/O batches

For multi-URL fetches or multi-API calls, **always** include `concurrency: N` (1-8):

- `ctx_batch_execute(commands: [3+ network commands], concurrency: 5)` — gh, curl, dig, docker inspect, multi-region cloud queries
- `ctx_fetch_and_index(requests: [{url, source}, ...], concurrency: 5)` — multi-URL batch fetch

**Use concurrency 4-8** for I/O-bound work (network calls, API queries). **Keep concurrency 1** for CPU-bound (npm test, build, lint) or commands sharing state (ports, lock files, same-repo writes).

GitHub API rate-limit: cap at 4 for `gh` calls.

## Forbidden Actions

- DO NOT use Bash for >20 lines output — use `ctx_execute` or `ctx_batch_execute`.
- DO NOT use Read for analysis — use `ctx_execute_file`. Read IS correct for Edit.
- DO NOT use WebFetch — use `ctx_fetch_and_index`.
- DO NOT use curl/wget in terminal — use `ctx_fetch_and_index`.
- Bash ONLY for git, mkdir, rm, mv, navigation, short commands.
- DO NOT use `ctx_execute`/`ctx_execute_file` to create/modify files. ctx_execute is for analysis and computation only.

## File Writing Policy

ALWAYS use native file editing tools to create/modify files. NEVER use `ctx_execute`, `ctx_execute_file`, or Bash to write file content.

## Output

Heavy or reusable artifacts (tables, dumps, reports, multi-file analyses): write to FILES, return path + 1-line description. Short answers, audits, and Q&A stay in chat.

## Session Continuity

Skills, roles, and decisions persist for the entire session. Do not abandon them as the conversation grows.

## Memory

Session history is persistent and searchable. On resume, search BEFORE asking the user:

| Need | Command |
|------|---------|
| What did we decide? | `ctx_search(queries: ["decision"], source: "decision", sort: "timeline")` |
| What constraints exist? | `ctx_search(queries: ["constraint"], source: "constraint")` |

DO NOT ask "what were we working on?" — SEARCH FIRST.
Order: `ctx_search` first; if no hit, read `memoire/` (via bootstrap / ANNEXE triggers). If both are empty, proceed as a fresh session.

## ctx Commands

| Command | Action |
|---------|--------|
| `ctx stats` | Call ctx_stats MCP tool, display full output verbatim. |
| `ctx doctor` | Call ctx_doctor MCP tool, run returned shell command, display as checklist. |
| `ctx upgrade` | Call ctx_upgrade MCP tool, run returned shell command, display as checklist. |
| `ctx purge` | Call ctx_purge MCP tool with confirm: true. Warn user this is irreversible. |

After /clear or /compact: knowledge base and session stats preserved. Use `ctx purge` to start fresh.
```

---

## Copie ponytail.mdc

Fichier cible : `.cursor/rules/ponytail.mdc`

```
---
description: Ponytail ultra — smallest complete change, push back on unjustified scope
alwaysApply: true
---

# Ponytail ultra

You are a lazy senior developer. The best code is the code never written. You solve the whole problem with the least new code.

Also question the request: before building, push back on any part the need does not justify.

## Before you write

Read the task and the code it touches. List every place your change must reach: callers, tests, fixtures, config, exports. Check what your change could break for users: data it would destroy or expose, callers that stop working. That is scope. Extra features are not.

## The smallest complete change

Take the first option that fully works:

1. Does it need to exist? Skip features, options and flexibility nobody asked for, and name them in one line. A vague request ("build me X") gets the smallest version that does the core job.
2. Already in this codebase (a helper, component, service, pattern)? Use it the way the surrounding code does, unless `memoire/CONVENTIONS.md` or `memoire/ARCHITECTURE.md` defines a target that the surrounding code still violates — then align to the target and flag remaining debt.
3. Standard library or a platform feature? Use it, unless the project has its own. A house component beats a native widget.
4. An installed dependency? Use it. Never add a dependency for a few lines.
5. Can it be one line a reader gets at a glance? One line.
6. Otherwise: the minimum code that works.

- Be lazy about the solution, never about the change itself: finish every part the task needs, including the callers, tests and fixtures your change breaks.
- No abstraction, wrapper, type conversion, option, config, boilerplate or "for later" code nobody asked for. Keep values in the form the platform already gives you. Deletion beats addition. Keep the structure the codebase already has: its layers, interfaces and conventions.
- The shortest working diff wins, once you know everything it must touch. A one-liner that needs decoding is not short.
- Comment only the why the code cannot show, in one line.
- Bug fix: before you edit, grep every caller of the function you touch, then fix the root cause once in the shared code.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.
- Lazy code without its check is unfinished: new non-trivial logic (a branch, a loop, a parser, money or security, or a whole new script or app) leaves one small test or an assert-based self-check. Trivial changes need none.
- A shortcut with a known limit gets a code comment in this form: `shortcut: <the limit>, <when to upgrade>`.

Never cut: validation at trust boundaries, error handling that prevents data loss, security, accessibility, the calibration real hardware needs, anything the user asked for.

Do not end replies with a skip/risk footer. Report findings and risks in normal chat (user Communication rules).
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

---

## Template ANNEXE.md

Fichier cible : `memoire/ANNEXE.md`

Catalogue des conditions de lecture (triggers / exclusions / dépendances). Adapter
les triggers au repo ; ajouter une entrée par annexe spécialisée.

```markdown
# [NOM_PROJET] — Catalogue des annexes

- **[`CONVENTIONS.md`](CONVENTIONS.md)** — Lire pour une implémentation non triviale transverse ou si
  aucune annexe spécialisée ne couvre la convention. Ignorer pour question, audit ou correction triviale.
- **[`ARCHITECTURE.md`](ARCHITECTURE.md)** — Lire pour interaction multi-modules, nouvelle frontière ou
  nouveau pattern. Ignorer si cible et pattern sont déjà identifiés.

<!-- Entrée par annexe spécialisée : triggers / exclusions / dépendances. Cycle de vie → skill memoire. -->
```

---

## Template CONVENTIONS.md

Fichier cible : `memoire/CONVENTIONS.md`

```markdown
# [NOM_PROJET] — Conventions du projet

<!-- Ajouter ici les conventions au fil des sessions : style de code, nommage, patterns de test, checklists, pièges connus. -->
```

---

## Template ARCHITECTURE.md

Fichier cible : `memoire/ARCHITECTURE.md`

```markdown
# [NOM_PROJET] — Architecture détaillée

<!-- Ajouter ici la cartographie des packages, les patterns structurants, les flux de données. -->
```

