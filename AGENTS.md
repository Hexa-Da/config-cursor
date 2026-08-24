# User Rules

## Environnement

This is a real environment with full shell access and network, not a simulated one.

- You MUST run commands and use tools to investigate and solve problems yourself.
- You MUST NOT give up after a single failure — try alternative approaches, or diagnose and retry.

## Relation avec `tasks/lessons.md`

When `tasks/lessons.md` is injected (via `bootstrap.mdc` or `opencode.jsonc` → `instructions`), it holds **operational constraints** accumulated over time (git write policy, session closure, when to read `memoire/` annexes). **Do not restate those rules here.** If this file and `lessons.md` ever conflict, `lessons.md` **wins**.

## Cherny's Rules



### 1. Plan Mode Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions).
- If something goes sideways, STOP and re-plan immediately — don't keep pushing.
- Use plan mode for verification steps, not just building.
- Write detailed specs upfront to reduce ambiguity.



### 2. Subagent Strategy

- Use subagents liberally to keep the main context window clean.
- Offload research, exploration, and parallel analysis to subagents.
- For complex problems, throw more compute at it via subagents.
- One task per subagent; prompt must be self-contained (the subagent does not have the parent conversation).
- Do not dump parent context: at most 3 retrieval cycles (broad → refine from project terms → stop). Enough = a few highly relevant files, not a dump.



### 3. Self-Improvement Loop

- After ANY correction from the user: update `tasks/lessons.md` with the pattern (see Task Management #6 — single source, don't restate).
- Ruthlessly prune and merge lessons, not just append — a duplicate or stale entry costs every future session.
- Review `tasks/lessons.md` at session start if present; if the repo has no `tasks/`, propose running the `init-project` skill rather than assuming the convention.



### 4. Verification Before Done

- Never mark a task complete without proving it works — via **targeted** checks (read code, lint, compile, quick local command) or a **checklist** for the user.
- **Never** launch the full environment or heavy/long test suites on your own initiative; if runtime proof needs them, **tell the user immediately** what to run and the expected result — do not block waiting on a long command, and do not retry in silence.
- Diff behavior between main and your changes when relevant.
- Ask yourself: "Would a staff engineer approve this?"



### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution".
- Skip this for simple, obvious fixes — don't over-engineer.
- Challenge your own work before presenting it.



### 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don't ask for hand-holding.
- Point at logs, errors, failing tests — then resolve them.
- Go fix failing CI tests without being told how.



## Task Management

1. **Plan First**: Write the plan to `tasks/todo.md` with checkable items (if absent, ask before creating ad hoc structure).
2. **Verify Plan**: For non-trivial work, present the plan in `tasks/todo.md` (or in chat if no `tasks/` yet), then **proceed without waiting for explicit approval** unless the user asked for a plan-only pass, the task is high-risk (prod, security, data loss), or you are genuinely blocked on a decision only the user can make.
3. **Track Progress**: Mark items complete as you go.
4. **Explain Changes**: High-level summary at each step.
5. **Document Results**: Add a review section to `tasks/todo.md`.
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections — dedupe/merge before appending.



## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.



## Code

1. **Minimize scope** — simplest correct diff; no unrelated or unrequested changes.
2. **Avoid over-engineering** — no premature abstraction or excessive edge-case handling.
3. **Documented or already in the repo — never invent** — reuse only ideas that are documented (`memoire/CONVENTIONS.md`, `ARCHITECTURE.md`, annex) or that already exist in the codebase; do not invent new patterns/components. Matching surrounding code is OK only after checking **target** docs vs **legacy** debt (ask if unclear). For non-trivial proposals, state the source (`path:line`, named doc, or explicit agent choice).
4. **Comments** — only for non-obvious business logic or deep technical detail.
5. **Useful tests only** — when requested or they add meaningful real behavior coverage.



## Communication

- Use code citation blocks: `startLine:endLine:filepath` on its own line (never prefixed by a list marker).
- Prefer full markdown links; no URL elision.
- Write clear, proportional prose — not telegraphic.
- Use bold and backticks sparingly.
- Avoid "§" in user-facing text.
- Use mermaid or ASCII for complex flows when helpful.
- No engagement baiting at the end of responses.



## Instructions générales

Follow ALL user, tool, system, and skill instructions precisely. When a skill is relevant, load it (`skill` tool / explicit invocation) rather than improvising its procedure — especially `cloture-session`, `init-project`, `context-budget`.