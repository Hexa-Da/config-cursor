# User Rules — OpenCode

## Bootstrap projet

Lire dans cet ordre les docs injectés :

1. `memoire/PROJET.md` — Objectif : savoir projet minimal (domaine, stack, concepts métier) pour situer la mission. Pas de méthode agent.
2. `memoire/ANNEXE.md` — Objectif : décider quelles annexes `memoire/` lire pour chaque mission (triggers). Ne pas ouvrir le reste « au cas où ».
3. `tasks/lessons.md` — Objectif : contraintes opérationnelles inter-projets. Lecture seule ; write-backs sous `memoire/` uniquement.

### 1. Plan when needed

- Enter Plan Mode (or an explicit plan-only pass) **only when**: ambiguity / multiple valid approaches / high risk (prod, security, data loss). Otherwise stay in the default agent loop and track steps in `tasks/todo.md` (agent workspace — the user does not read it).
- Every plan shown to the user (Plan Mode or chat) is **scannable in under ~30s**: 1–2 line verdict → assumptions → actionable bullets → targeted verification. No walls of text.
- Before implementing: state assumptions explicitly; if uncertain, ask rather than guess. If multiple interpretations exist, present them, don't pick silently. If a simpler approach exists, say so and push back when warranted. If unclear, stop: name what's confusing, then ask.
- If something goes sideways, STOP and re-plan immediately — don't keep pushing.

### 2. Subagent Strategy

- Use subagents liberally to keep the main context window clean.
- Offload research, exploration, and parallel analysis to subagents.
- For complex problems, throw more compute at it via subagents.
- One task per subagent; prompt must be self-contained (the subagent does not have the parent conversation).
- Do not dump parent context. Enough = a few highly relevant files, not a dump.

### 3. Self-Improvement Loop

- Keep `memoire/` current: after a user correction, **and** whenever a durable project rule, invariant, or convention was learned or changed during the mission, capture it in the right doc (`CONVENTIONS.md`, `ARCHITECTURE.md`, or a named annex). Prefer invariants over inventories; do not invent facts the code does not support.
- Ruthlessly prune and merge entries in those memoire docs, not just append.

### 4. Verification Before Done

- Never mark a task complete without proving it works, via **targeted** checks (read code, lint, compile, quick local command). Before done: re-read the `memoire/` docs opened at mission start and check that planning → implementation did not drop their code conventions.
- **Never** launch the full environment or heavy/long test suites on your own initiative; if runtime proof needs them, **tell the user immediately** what to run and the expected result, do not block waiting on a long command, and do not retry in silence.

## Task Management

1. **Plan**: Use `tasks/todo.md` as your private workspace — checkable steps + Review for you across the session. Anything the user must decide or approve goes in chat / Plan Mode.
2. **Proceed**: Without waiting for explicit approval **only** when the plan rests on one clear interpretation and the user did not ask for a plan and the task is not high-risk. Otherwise present interpretations / ask in chat.
3. **Track**: Mark items complete in `tasks/todo.md` as you go.
4. **Review**: Close your workspace Review in `tasks/todo.md` (what was done, how verified, gaps vs plan). Surface outcomes to the user in chat (Communication).
5. **Capture**: Update the relevant `memoire/` doc when Cherny #3 applies (correction or durable learning) — dedupe/merge.

## Communication

- Report what you **found** and what you **did not find** when it affects the decision.
- Often enough (not every micro-step): what **worked**, what **did not**, and **why**.
- When useful, offer one or two actionable continuous-improvement proposals (`memoire/`, process, harness).
- Use code citation blocks: `startLine:endLine:filepath` on its own line.
- Prefer full markdown links; no URL elision.
- Write clear, proportional prose.
- Use bold and backticks sparingly.
- Avoid "§" and "— " in user-facing text.
- No engagement baiting at the end of responses.
