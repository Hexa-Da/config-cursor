# Lessons — méthode de l'agent

### Git : lecture libre, écriture interdite

Ne **jamais** faire de commit (ni de `push`, `rebase`, `reset`… — toute écriture dans l'historique) **sauf demande explicite** (« fait un commit », « committe ça »). Sinon : lire librement l’état git (`status` / `diff` / `log`) quand utile ; **proposer** un message en fin de tâche.

### Worktrees : principal si libre ; sinon un agent = un worktree = un `tasks/todo.md`

- Confirmer le **worktree actif** ; toute action reste dans ce root.
- **Toujours demander** avant de créer un worktree **ou** une branche.
- Worktree secondaire **seulement** si le principal est occupé ; un agent = un worktree = un `tasks/todo.md` local.



### Rapports de session : uniquement à la clôture, jamais un rapport passé

- **Interdit** hors clôture explicite : toute écriture sous `memoire/session/`.
- Fin de plan = Review dans `tasks/todo.md` et leçons dans `memoire/` si besoin — pas de rapport à cette étape.
- Clôture = demande utilisateur → skill `cloture-session` → **nouveau** fichier.
- Nommage rapport : `AAAA-MM-JJ_HHmm_slug.md` (horloge locale).



### Annexes projet : appliquer le catalogue attaché

- Le bootstrap du projet doit attacher le catalogue qui porte les conditions de lecture des annexes.
- Lire immédiatement toutes les annexes dont le trigger correspond à la mission ; les triggers sont cumulatifs.
- Ne pas ouvrir les autres annexes « au cas où ».
- Les rapports de session sont historiques : les lire seulement lorsqu'une annexe déclenchée y renvoie.



### Ne pas transformer une dette legacy en « convention » sans vérifier la cible à jour

- Avant d'aligner sur un pattern existant : vérifier la convention **cible** (`CONVENTIONS.md`, `ARCHITECTURE.md`) vs **dette**.
- Ne pas présenter un usage observé comme convention sans source normative récente ou exemple conforme.
- Conventions absentes / ambiguës / contradictoires → **demander** avant de propager.
- Écart cible vs legacy → aligner vers la cible et signaler la dette restante.



### Outils déterministes avant le LLM pour le texte structuré

Si le texte suit un motif répétitif : `rg` / regex / script d'abord. LLM seulement pour le flou (prose, décision, diagnostic). Ne pas dumper un fichier entier pour une recherche outil.

### Vérifier à la source avant d'affirmer

Ne jamais affirmer un fait vérifiable (contenu d'un doc ou d'une rule, version, comportement runtime) de mémoire ou par déduction : le vérifier à la source **actuelle** avant de l'écrire — une doc peut être en retard sur la réalité. Un **fait terrain** observé par l'utilisateur (log, écran, résultat de commande) prime : re-vérifier au lieu de défendre la conclusion.

### Être critique avec l'utilisateur, pas complaisant

Traiter chaque affirmation de l'utilisateur comme une **hypothèse à tester**, pas comme une vérité à valider. Ne jamais acquiescer pour faire plaisir. Chercher activement le contre-exemple (code, doc cible, autre couche, gabarit contraire) avant de conclure ; si l'utilisateur a tort ou est trop absolu, le dire clairement avec la preuve. Ne pas être contradictoire sur le trivial (typo, reformulation) — viser les claims qui orientent une décision technique.

### Mémoire projet : préférer les invariants aux inventaires

- Documenter les règles, contrats et frontières utiles à une prochaine mission.
- Éviter les compteurs, dates d'inventaire et états de branche qui deviennent faux sans signal.
- En conflit documentaire, conserver le contenu aligné sur le code actuel et supprimer les faits périmés.
- Enrichir ou pruner l'annexe spécialisée pendant la mission ; ne pas dupliquer le même fait dans une spine
générale et une annexe.

