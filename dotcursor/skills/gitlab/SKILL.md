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
- [ ] 1. Extraire iid (chiffres) ou URL MR — jamais project!iid / !iid
- [ ] 2. Un seul fetch.py avec cette cible ; lire la sortie
- [ ] 3. Signaler si HEAD ≠ source_branch (ne pas checkout)
- [ ] 4. Cibler la note demandée, sinon les discussions non résolues
- [ ] 5. Analyser / plan ; n’implémenter le code que si la demande le dit
- [ ] 6. Pas de commentaire GitLab / commit / push / branche / worktree /
        écriture memoire/session/ — sauf verbe explicite pour cet acte
```

**Piège** : « corrige », « fais », « a faire », « report develop → … » = **code / conflits seulement**.
Ça n’autorise **pas** `commit`, `push`, création de branche, ni édition de
`memoire/session/`. Pour chaque acte git ou session : demande dédiée
(« commit », « pousse », « crée la branche resolve », « mets à jour le
rapport de session », `/cloture-session`, …).

## 1. Fetch déterministe

```bash
python3 ~/.cursor/skills/gitlab/scripts/fetch.py '<url-ou-iid>'
```

**Cibles acceptées uniquement** (sinon `cible invalide` — ne pas « refetch » en improvisant) :

- URL `…/-/merge_requests/{iid}` avec `#note_{id}` optionnel
- iid **numérique seul** (`123`)
- `--note {id}` pour cibler une note sans fragment URL

**Interdit** (le parseur les refuse ; ce ne sont pas des cibles `glab mr view` non plus) :

- `group/project!iid` / `myshop/edithor!123` (markdown GitLab, pas une entrée CLI)
- `!123`, nom de branche, titre de MR
- Premier essai « shorthand » puis second essai : **choisir URL ou iid dès le premier appel**

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

Même pour une MR robot `develop` → `develop-vue3` (procédure resolve dans
`PROJET.md`) : **annoncer** la branche resolve dans le plan et **attendre
l’accord** avant `checkout -B` / `--no-track`. « Report à faire » ≠
permission de créer la branche tout seul.

## 3. Analyse puis action

- **Note isolée** : résumer l’intention (2–3 lignes), fichier:ligne, fil.
  Juger si c’est fondé (convention cible vs dette — ne pas propager un
  pattern legacy). Puis plan court.
- **MR entière** (« review de la MR N ») : lister les unresolved par
  fichier, ordre de traitement proposé. Pas un dump de tout le diff.
- **Implémenter (fichiers seulement)** si le user le demande (corrige,
  applique, fais, concentre-toi pour traiter, report à faire…). Sinon
  s’arrêter au plan. **Implémenter ≠ committer** (voir §4).
- Merge / conflits : résoudre le contenu des fichiers ; laisser l’index
  prêt si utile ; **ne pas** `git commit` pour « finir le merge » —
  proposer la commande + message, s’arrêter.
- Code **non trivial** : `CONVENTIONS.md` une fois si le domaine le
  justifie ; annexe bootstrap (ex. `VEEVALIDATE.md`) **immédiatement** si
  le commentaire concerne ce domaine. Pas d’audit lecture seule → pas
  CONVENTIONS.
- `memoire/session/` : **lecture** seulement si reprise explicite d’une
  session. **Jamais** créer / éditer un rapport de session pendant un
  fetch / fix MR — réservé à une demande explicite ou `/cloture-session`.

## 4. Interdits sauf demande explicite

- Commentaire / reply / resolve sur GitLab (`glab mr note`, API POST)
- `commit` / `push` / `rebase` / `reset` — y compris le commit qui
  finalise un `git merge` après conflits (« il faut committer pour
  sortir de MERGE_HEAD » n’est **pas** une exception)
- Création de branche / worktree / `checkout` hors worktree actif
- Écriture sous `memoire/session/`
- Lancer Bugbot ou Security Review

En fin de fix : **proposer** le message (et la commande `git commit` /
`git push` / MR) en une phrase ; **ne pas** les exécuter.

Si création de MR explicitement demandée : `glab mr create` peut renvoyer
**403** `insufficient_scope` (token sans écriture API) — alors pousser la
branche et demandeer a l'utilisayeir de créer la MR **manuellement** dans 
l’UI GitLab ; ne pas retenter ni pivoter sur un autre endpoint.

## Référence projet

Si le repo a `memoire/PROJET.md` § GitLab : s’y conformer (host, `glab`
déjà configuré). Le script reste la source pour **comment** fetcher.
