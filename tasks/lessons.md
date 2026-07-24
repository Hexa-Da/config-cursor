# Lessons — méthode de l'agent

> Leçons **de méthode** (comment l'agent travaille), valables tous projets confondus.
> Distinct de `memoire/CONVENTIONS.md` / `memoire/ARCHITECTURE.md`, qui capitalisent les leçons **propres au repo courant**.
> Une leçon ici doit survivre à un changement de projet ; sinon elle va dans `memoire/`.

**Test de tri** : retirer tout vocabulaire du domaine/repo courant de la leçon. Si elle garde un sens et éviterait la même erreur sur un projet totalement différent → ici. Si le sens disparaît sans ce vocabulaire → `memoire/`.

## Format

- **Symptôme** : ce qui a été corrigé par l'utilisateur
- **Cause** : pourquoi l'agent s'est trompé
- **Règle** : comment l'éviter la prochaine fois

---



### Git : lecture libre, écriture interdite

- **Symptôme** : risque qu'un agent committe (ou s'abstienne de consulter git par excès de prudence).
- **Cause** : frontière lecture/écriture non explicitée.
- **Règle** : ne **jamais** faire de commit (ni `commit`, `push`, `rebase`, `reset`... — toute écriture dans l'historique). En revanche, consulter le worktree aussi souvent qu'utile (`git status`, `git diff`, `git log`...) est libre et encouragé. Quand c'est pertinent (fin de tâche cohérente), **proposer un message de commit** à l'utilisateur — c'est lui qui committe.



### Ne pas lancer l'environnement ni les tests lourds pour « vérifier » — dire quoi tester

- **Symptôme** : l'agent démarre des services (DB, serveur dev, stack complète) ou lance des suites de tests (Gradle, TI Mongo…) de son propre chef, attend un terminal qui bloque ou time out, puis reste muet ou retente en boucle — au lieu de dire à l'utilisateur quoi lancer.
- **Cause** : réflexe de « prouver » le travail en autonomie, alors que l'environnement local de l'utilisateur (réseau interne, Gradle wrapper, IntelliJ, Mongock) n'est souvent pas fiable ni disponible pour l'agent.
- **Règle** :
  - Ne **jamais** lancer l'environnement complet ni les suites de tests lourdes de son propre chef, sauf demande explicite de l'utilisateur.
  - Si la vérification runtime est nécessaire : **dire immédiatement quoi tester** (classe ou package IntelliJ, commande Gradle ciblée, résultat attendu) — ne pas attendre passivement un terminal bloqué ni enchaîner les relances Gradle sans retour à l'utilisateur.
  - En fin de tâche, fournir une **checklist de vérif concise** : quoi lancer, combien de tests attendus, durée indicative (TU rapides vs TI Mongo).
  - Des vérifications ciblées côté agent restent OK sans demander à l'utilisateur : lecture de code, lint, compilation locale si rapide et fiable.



### Vocabulaire technique : termes courants de la communauté, pas calques ni noms de lib en prose

- **Symptôme** : l'agent parle de « test de fumée », insiste sur « MockK » dans les explications, ou invente des anglicismes / traductions littérales peu usuels.
- **Cause** : calque FR↔EN ou sur-précision (nom de lib) au lieu du terme le plus employé et compris par les devs.
- **Règle** :
  - En prose (chat, docs, rapports) : utiliser le **vocabulaire courant de la communauté** — ex. *smoke test* (pas « test de fumée »), *mock* (pas « MockK » à chaque phrase).
  - Réserver le nom de lib / d'API au moment où ça compte (import, doc de stack, snippet) : MockK, `mockk`, `mockkClass`, etc.
  - En cas de doute : préférer le terme le plus répandu chez les devs, pas la traduction littérale ni le jargon maison.



### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Symptôme** : l'agent crée ou édite `memoire/session/*.md` / `INDEX.md` en fin de plan (« Doc session »), ou met à jour un rapport clos, sans demande de clôture.
- **Cause** : confusion entre Review Cherny (`tasks/todo.md`) et skill `cloture-session` ; règle projet trop centrée sur la *lecture* des annexes.
- **Règle** :
  - **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
  - Fin de plan = section Review dans `tasks/todo.md` (+ leçons durables si besoin). Pas de nouveau rapport, pas de retouche d'un ancien.
  - Clôture = seulement si l'utilisateur le demande → skill `cloture-session` → **nouveau** fichier + ligne INDEX ; **jamais** modifier un rapport déjà écrit.
  - Dans le rapport : pour chaque commit, hash + message complet— template dans `cloture-session/reference.md`.
