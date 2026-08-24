# Lessons — méthode de l'agent

> Leçons **de méthode** (comment l'agent travaille), valables tous projets confondus.
> Distinct de `memoire/CONVENTIONS.md` / `memoire/ARCHITECTURE.md`, qui capitalisent les leçons **propres au repo courant**.
> Une leçon ici doit survivre à un changement de projet ; sinon elle va dans `memoire/`.

**Test de tri** : retirer tout vocabulaire du domaine/repo courant de la leçon. Si elle garde un sens et éviterait la même erreur sur un projet totalement différent → ici. Si le sens disparaît sans ce vocabulaire → `memoire/`.

## Format

Fichier always-on : **titre + règle seulement** (pas de Symptôme/Cause ici — coût token).
À la capture : dériver Symptôme → Cause → Règle, puis n'écrire que la règle, concise.

---

### Git : lecture libre, écriture interdite

Ne **jamais** faire de commit (ni `commit`, `push`, `rebase`, `reset`… — toute écriture dans l'historique) **sauf demande explicite** (« fait un commit », « committe ça ») — alors exécuter directement, sans reproposer un message à valider. Sinon : lecture libre (`git status`, `git diff`, `git log`…) et **proposer** un message en fin de tâche cohérente — c'est l'utilisateur qui committe.

### Worktrees : principal si libre ; sinon un agent = un worktree = un `tasks/todo.md`

- Confirmer le **worktree actif** ; toute action reste dans ce root (pas de `tasks/todo.md` hors de ce répertoire).
- **Défaut = principal** s'il est libre (aucun autre agent + working tree propre) → changer de branche **sur place**.
- Worktree secondaire **seulement** si le principal est occupé ; un agent = un worktree = un `tasks/todo.md` local — ne pas écraser celui d'un autre.
- **Demander** avant de créer un worktree ou une branche.


### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
- Fin de plan = Review dans `tasks/todo.md` (+ leçons si besoin) — pas de nouveau rapport ni retouche d'un ancien.
- Clôture = demande utilisateur → skill `cloture-session` → **nouveau** fichier + ligne INDEX ; **jamais** modifier un rapport déjà écrit.
- Dans le rapport : message de commit complet pour chaque commit — template dans `cloture-session/reference.md`.

### Ne pas relire les annexes `memoire/` à chaque tour ni les ignorer par défaut

- `CONVENTIONS.md` — avant code **non trivial** (feature, nouveau fichier, migration, test) ou doute de pattern ; **pas** pour audit lecture seule, question, typo, fix d'une ligne. Une fois par session, sauf changement de domaine.
- `ARCHITECTURE.md` — interaction multi-composants, nouveau pattern, ou frontière de module ; lire en cours de tâche si la portée grossit.
- `memoire/session/` — seulement pour reprendre un travail passé (demande explicite).

### Ne pas transformer une dette legacy en « convention » sans vérifier la cible à jour

- Avant d'aligner sur un pattern existant : vérifier la convention **cible** (`CONVENTIONS.md`, `ARCHITECTURE.md`, annexe) vs **dette**.
- Ne pas présenter un usage observé comme convention sans source normative récente ou exemple conforme.
- Conventions absentes / ambiguës / contradictoires → **demander** avant de propager.
- Écart cible vs legacy → aligner vers la cible et signaler la dette restante.

### Outils déterministes avant le LLM pour le texte structuré

Si le texte suit un motif répétitif : `rg` / regex / script d'abord. LLM seulement pour le flou (prose, décision, diagnostic). Ne pas dumper un fichier entier pour une recherche outil.

### Sourcer toute proposition d'implémentation non triviale

Pour toute proposition non triviale, indiquer la source :
- fichier existant du projet → `path:line` ;
- doc / framework / RFC → nommer la source ;
- choix propre de l'agent → le dire.
Pas pour fixes triviaux ni changements qui suivent déjà un pattern local.
