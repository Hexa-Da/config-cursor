---
name: check-memoire
description: >-
  Audits memoire bootstrap + ANNEXE compliance for the current mission and
  reports gaps without remediating. Use when the user asks check-memoire,
  /check-memoire, audit memoire, docs memoire chargés, or whether the right
  annexes are loaded for this session.
disable-model-invocation: true
---

# check-memoire — audit conformité

Vérifie que les docs `memoire/` **requis pour la mission courante** sont
présents et lus. **Pas** d’introspection du context window : conformité
(docs requises vs lues), pas contenu résiduel du prompt.

Lecture seule. **Ne comble pas les GAP** (ne pas ouvrir les docs manquants
pour « corriger » la session). Aucune écriture sous `memoire/` ni rapport
de session. Distinct de `alignement` (repo ↔ machine).

## Checklist

```
- [ ] 1. Prérequis harness
- [ ] 2. Toujours-on (PROJET / ANNEXE / lessons)
- [ ] 3. Mission courante
- [ ] 4. Annexes attendues (ANNEXE.md)
- [ ] 5. Écarts OK | GAP | EXTRA
- [ ] 6. Rapport
```

## Étapes

1. **Prérequis harness** — confirmer `memoire/` et `tasks/lessons.md`.
   Détecter le câblage bootstrap :
   - Cursor : `.cursor/rules/bootstrap.mdc`
   - OpenCode : `opencode.jsonc` → `instructions`
   - jcode : bootstrap global `~/AGENTS.md` (pas d’exigence d’`./AGENTS.md` projet)
   Si harness / fichiers absents → **bloqué** ; proposer `init-project` /
   `init-project-opencode` / `init-project-jcode` selon le canal. Stop.

2. **Toujours-on** — `memoire/PROJET.md`, `memoire/ANNEXE.md`,
   `tasks/lessons.md`. S’ils n’existent pas → **bloqué**. S’ils n’ont pas
   encore été lus dans la session → **GAP** (ne pas relire pour combler).

3. **Mission** — déduire depuis le fil de discussion et `tasks/todo.md`
   s’il existe. Si ambiguë → **une** question, pas de guess.

4. **Annexes attendues** — appliquer `ANNEXE.md` (triggers cumulatifs,
   exclusions). Produire l’ensemble attendu (`CONVENTIONS.md`,
   `ARCHITECTURE.md`, annexes nommées…). Ne pas inventer d’annexes hors
   catalogue. `memoire/session/` seulement si une annexe déclenchée y renvoie
   ou reprise explicite. Si `ANNEXE.md` est GAP → ne pas l’ouvrir ; indiquer
   les attendues comme indéterminées.

5. **Écarts** — pour chaque attendu : `OK` (déjà lu dans cette session) ou
   `GAP` (non lu — **ne pas ouvrir**). `EXTRA` uniquement si une annexe hors
   trigger a été ouverte dans *cette* session (pas un inventaire disque).

6. **Rapport** — utiliser le format ci-dessous. Une ligne de disclaimer
   suffit ; pas de prose longue.

## Format de rapport

```text
check-memoire — <mission en 1 ligne>
Toujours-on : PROJET / ANNEXE / lessons  → OK|GAP
Attendues   : <fichier> → OK|GAP ; … | indéterminées (ANNEXE GAP)
Extra       : <fichier> ; … | —
Verdict     : conforme | écarts | bloqué (<raison>)
Conformité docs requises vs lues — pas le context window.
```

## Verdicts

| Verdict | Sens |
| --- | --- |
| **conforme** | Toujours-on + attendues OK, aucun GAP |
| **écarts** | Au moins un GAP (non comblé) |
| **bloqué** | Harness / fichiers manquants, ou mission trop ambiguë |
