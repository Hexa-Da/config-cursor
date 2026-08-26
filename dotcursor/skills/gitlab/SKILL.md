---
name: gitlab
description: >-
  Fetches GitLab merge requests and discussion notes via glab (no MCP),
  then plans or applies the requested comment. Use when the user pastes a
  GitLab MR URL, #note_ id, asks for a revue/review MR, glab, merge_requests,
  or to work on a reviewer comment — not for Bugbot/security scans.
---

# GitLab MR (glab)

Pas de MCP GitLab. **Toujours** le script ci-dessous — ne pas inventer
`GET …/notes/{id}` (404) ni `glab mr view` sans iid (ça prend la branche
courante, souvent la mauvaise MR).

Ce skill **n’est pas** `/review-bugbot` ni `/review-security` (scan de diff
local). Ne pas les lancer sauf demande explicite de scan bugs/sécu.

## Checklist

```
- [ ] 1. Parser l’URL / iid / note_  → lancer fetch.py
- [ ] 2. Lire la sortie ; signaler si HEAD ≠ source_branch (ne pas checkout)
- [ ] 3. Cibler la note demandée, sinon les discussions non résolues
- [ ] 4. Analyser / plan ; n’implémenter que si la demande le dit
- [ ] 5. Pas de commentaire GitLab, commit, branche, worktree sans demande
```

## 1. Fetch déterministe

```bash
python3 ~/.cursor/skills/gitlab/scripts/fetch.py '<url-ou-iid>'
# depuis le repo config-cursor :
python3 ~/Documents/config-cursor/dotcursor/skills/gitlab/scripts/fetch.py '<url-ou-iid>'
```

Exemples :

```bash
python3 ~/.cursor/skills/gitlab/scripts/fetch.py \
  'https://gitlab.example.com/group/project/-/merge_requests/123#note_456'
python3 ~/.cursor/skills/gitlab/scripts/fetch.py 123
python3 ~/.cursor/skills/gitlab/scripts/fetch.py 123 --note 456
```

Le script pagine les discussions, extrait le **fil entier** d’une `note_`,
et liste les **unresolved** si aucune note n’est ciblée. Ne pas re-fetcher
à la main ce qu’il a déjà imprimé.

Si `glab` échoue : coller stderr, s’arrêter. Ne pas pivoter sur l’API notes.

## 2. Branche / worktree

Si `HEAD` ≠ `source_branch` : le dire. **Ne pas** `checkout`, créer une
branche ou un worktree sans accord (leçon worktrees). Rester dans le
worktree actif.

## 3. Analyse puis action

- **Note isolée** : résumer l’intention (2–3 lignes), fichier:ligne, fil.
  Juger si c’est fondé (convention cible vs dette — ne pas propager un
  pattern legacy). Puis plan court.
- **MR entière** (« review de la MR N ») : lister les unresolved par
  fichier, ordre de traitement proposé. Pas un dump de tout le diff.
- **Implémenter** seulement si le user le demande (corrige, applique, fais,
  concentre-toi pour traiter…). Sinon s’arrêter au plan.
- Code **non trivial** : `CONVENTIONS.md` une fois si le domaine le
  justifie ; annexe bootstrap (ex. `VEEVALIDATE.md`) **immédiatement** si
  le commentaire concerne ce domaine. Pas d’audit lecture seule → pas
  CONVENTIONS.
- `memoire/session/` : lecture seulement si reprise explicite d’une session.

## 4. Interdits sauf demande explicite

- Commentaire / reply / resolve sur GitLab (`glab mr note`, API POST)
- `commit` / `push` / `rebase` / `reset`
- Lancer Bugbot ou Security Review

En fin de fix : proposer un message de commit, ne pas le faire.

## Référence projet

Si le repo a `memoire/PROJET.md` § GitLab : s’y conformer (host, `glab`
déjà configuré). Le script reste la source pour **comment** fetcher.
