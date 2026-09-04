# Lessons — méthode de l'agent

**Test de tri** : retirer tout vocabulaire du domaine/repo courant de la leçon. Si elle garde un sens et éviterait la même erreur sur un projet totalement différent → ici. Si le sens disparaît sans ce vocabulaire → `memoire/`.
Contenu : titre + règle seule (dériver Symptôme→Cause→Règle à la capture, n’écrire que la règle).

---

### Git : lecture libre, écriture interdite

Ne **jamais** faire de commit (ni de `push`, `rebase`, `reset`… — toute écriture dans l'historique) **sauf demande explicite** (« fait un commit », « committe ça ») — alors exécuter directement. Sinon : lire librement l’état git (`status` / `diff` / `log`) quand utile ; **proposer** un message en fin de tâche — l’utilisateur committe.

### Worktrees : principal si libre ; sinon un agent = un worktree = un `tasks/todo.md`

- Confirmer le **worktree actif** ; toute action reste dans ce root.
- **Toujours demander** avant de créer un worktree **ou** une branche.
- Si accordé et principal libre → changer de branche **sur place** ; worktree secondaire **seulement** si le principal est occupé ; un agent = un worktree = un `tasks/todo.md` local.

### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
- Fin de plan = Review dans `tasks/todo.md` et màj du plan (+ leçons si besoin) — pas de rapport à cette étape.
- Clôture = demande utilisateur → skill `cloture-session` → **nouveau** fichier + ligne INDEX ; **jamais** modifier un rapport déjà écrit. Template dans `cloture-session/reference.md`.

### Ne pas relire les annexes `memoire/` à chaque tour ni les ignorer par défaut

- `CONVENTIONS.md` — avant code **non trivial** (feature, nouveau fichier, migration, test) ou doute de pattern ; **pas** pour audit lecture seule, question, typo, fix d'une ligne. Une fois par session, sauf changement de domaine.
- `ARCHITECTURE.md` — interaction multi-composants, nouveau pattern, ou frontière de module.
- Annexes nommées par bootstrap (ex. `VEEVALIDATE.md`) — lecture **immédiate** si la mission les concerne (prioritaire sur CONVENTIONS seul pour ce domaine).
- `memoire/session/` — seulement pour reprendre un travail passé (demande explicite).

### Ne pas transformer une dette legacy en « convention » sans vérifier la cible à jour

- Avant d'aligner sur un pattern existant : vérifier la convention **cible** (`CONVENTIONS.md`, `ARCHITECTURE.md`) vs **dette**.
- Ne pas présenter un usage observé comme convention sans source normative récente ou exemple conforme.
- Conventions absentes / ambiguës / contradictoires → **demander** avant de propager.
- Écart cible vs legacy → aligner vers la cible et signaler la dette restante.

### Outils déterministes avant le LLM pour le texte structuré

Si le texte suit un motif répétitif : `rg` / regex / script d'abord. LLM seulement pour le flou (prose, décision, diagnostic). Ne pas dumper un fichier entier pour une recherche outil.

### Vérifier à la source avant d'affirmer

Ne jamais affirmer un fait vérifiable (contenu d'un doc ou d'une rule, version, comportement runtime) de mémoire ou par déduction : le vérifier à la source **actuelle** avant de l'écrire — une doc peut être en retard sur la réalité. Un **fait terrain** observé par l'utilisateur (log, écran, résultat de commande) prime : re-vérifier au lieu de défendre la conclusion. Une **interprétation / verdict** de l'utilisateur n'est pas un fait terrain — la leçon suivante s'applique.

### Être critique avec l'utilisateur, pas complaisant

Traiter chaque affirmation de l'utilisateur comme une **hypothèse à tester**, pas comme une vérité à valider. Ne jamais acquiescer pour faire plaisir. Chercher activement le contre-exemple (code, doc cible, autre couche, gabarit contraire) avant de conclure ; si l'utilisateur a tort ou est trop absolu, le dire clairement avec la preuve. Ne pas être contradictoire sur le trivia (typo, reformulation) — viser les claims qui orientent une décision technique.
