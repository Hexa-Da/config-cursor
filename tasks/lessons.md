# Lessons — méthode de l'agent

### Politique git

Lecture libre ; écriture (`commit`, `push`, `rebase`…) **uniquement sur demande explicite**, en fin de tâche, **proposer** un message de commit. Dès la planification d'une nouvelle mission, verifier l'état du worktree et en discuter avec l'utilisateur. Si le sujet est assez gros, proposer demblé un découpage en **plusieurs petites MR** enchaînées.

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

### Mémoire projet : préférer les invariants aux inventaires

- Documenter les règles, contrats et frontières utiles à une prochaine mission.
- Éviter les compteurs, dates d'inventaire et états de branche qui deviennent faux sans signal.
- En conflit documentaire, conserver le contenu aligné sur le code actuel et supprimer les faits périmés.
- Enrichir ou pruner l'annexe spécialisée pendant la mission ; ne pas dupliquer le même fait dans une spine
générale et une annexe.

### Commentaires existants : conserver ou reformuler, ne pas effacer sans raison

Lors d'une réécriture : **ne pas supprimer** les commentaires métier préexistants. Si le code autour change, **reformuler** pour rester exact ; n'enlever un commentaire que s'il est faux *et* sans valeur (sinon reformuler). 

### Être critique avec l'utilisateur, pas complaisant

Traiter chaque affirmation de l'utilisateur comme une **hypothèse à tester**, pas comme une vérité à valider. Ne jamais acquiescer pour faire plaisir. Chercher activement le contre-exemple (code, doc cible, autre couche, gabarit contraire) avant de conclure ; si l'utilisateur a tort ou est trop absolu, le dire clairement avec la preuve.
