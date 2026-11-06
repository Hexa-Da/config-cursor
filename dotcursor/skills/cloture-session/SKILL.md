---
name: cloture-session
description: >-
  Procédure de clôture de session agent : rapport dans memoire/session/,
  leçons durables dans les docs memoire, frictions méthode dans tasks/lessons.md,
  reset tasks/todo.md.
  Use when the user asks to close, end, or clôturer the session.
disable-model-invocation: true
---

# Clôture de session

Procédure **générique**. Chemins repo par défaut : `memoire/session/`, `tasks/todo.md`, `tasks/lessons.md`.

## Checklist

```
- [ ] 1. Rapport de session (nouveau fichier, jamais modifier un rapport clos)
- [ ] 2. Leçons durables → memoire/
- [ ] 3. Frictions méthode / harness → tasks/lessons.md (si promuable)
- [ ] 4. Tout en français, concis
- [ ] 5. Reset tasks/todo.md au template vide
- [ ] 6. ctx purge (mémoire context-mode du projet)
```

## Étapes

1. **Rapport** : s'appuyer sur `tasks/todo.md` comme brouillon. Copier le template (voir [reference.md](reference.md) § Template rapport) vers `memoire/session/AAAA-MM-JJ_HHmm_slug.md` et remplir. `HHmm` = heure locale à la clôture (voir [reference.md](reference.md) § Nommage). **Toujours un nouveau fichier** — même en continuation d'une session précédente. Continuité → lien en en-tête (« Suite de : [titre](fichier.md) »). **Pas de retours à la ligne soft** : chaque paragraphe et chaque puce (Pourquoi / Lien / Commit) tient sur une seule ligne. **Fichiers** : chemin de package trop long → tronquer le segment intermédiaire par `.../` (garder préfixe `module/src/main|test` + suffixe parlant + fichier).
2. **Leçons durables (projet)** : reporter les leçons réutilisables dans le document cible sous `memoire/` (`CONVENTIONS.md`, `ARCHITECTURE.md`, ou annexe) avec lien `(← [session](memoire/session/….md))`. **Si la session change un état déjà documenté** (valeur de conf, statut de branche « non mergée », compteur, pattern remplacé), **mettre à jour le passage existant** — pas seulement éviter les doublons. Critères, tri, anti-doublons et état documenté → [reference.md](reference.md).
3. **Frictions méthode / harness** : uniquement à cette étape (jamais pendant la mission). Si une friction de méthode, harness, outil ou consigne a bloqué ou dégradé le travail et qu’elle est **promuable** vers `AGENTS.md` ou un skill : ajouter une entrée datée dans `tasks/lessons.md` (gabarit → [reference.md](reference.md) § Inbox frictions). **0 entrée** si rien de promuable. Pas de savoir projet, pas de récit de session. Signaler dans le chat le nombre d’entrées ajoutées (`0` ou `N`).
4. **Langue** : français, concis (économie de tokens futures sessions).
5. **Reset todo** : réinitialiser `tasks/todo.md` au template vide (voir [reference.md](reference.md) § Template todo). Ne pas vider `tasks/lessons.md` (inbox ; l’utilisateur prune / promeut).
6. **ctx purge** : appeler l’outil MCP `ctx_purge` avec `confirm: true` et `scope: "project"`. Irréversible : vide l’index FTS5 / events / stats context-mode du projet (pas les fichiers `memoire/`). Mentionner dans le chat que la purge est faite. Si le namespace MCP est absent, le signaler et ne pas bloquer la clôture.

## Référence détaillée

Nommage, critères de leçons, tableau de tri, inbox frictions, templates (rapport, todo) : [reference.md](reference.md).
