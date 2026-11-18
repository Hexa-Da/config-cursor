---
name: cloture-session
description: >-
  Procédure de clôture de session agent : rapport dans memoire/session/,
  leçons durables dans les docs memoire, frictions méthode énoncées dans le chat,
  purge context-mode.
  Use when the user asks to close, end, or clôturer the session.
disable-model-invocation: true
---

# Clôture de session

Procédure **générique**. Chemin repo par défaut : `memoire/session/`.

## Checklist

```
- [ ] 1. Rapport de session (nouveau fichier, jamais modifier un rapport clos)
- [ ] 2. Leçons durables → memoire/
- [ ] 3. Frictions méthode / harness → chat seulement (si promuable)
- [ ] 4. Tout en français, concis
- [ ] 5. ctx purge (mémoire context-mode du projet)
```

## Étapes

1. **Rapport** : s'appuyer sur le fil de discussion, le diff et `memoire/` déjà touché. Copier le template (voir [reference.md](reference.md) § Template rapport) vers `memoire/session/AAAA-MM-JJ_HHmm_slug.md` et remplir. `HHmm` = heure locale à la clôture (voir [reference.md](reference.md) § Nommage). **Toujours un nouveau fichier** — même en continuation d'une session précédente. Continuité → lien en en-tête (« Suite de : [titre](fichier.md) »). **Pas de retours à la ligne soft** : chaque paragraphe et chaque puce (Pourquoi / Lien / Commit) tient sur une seule ligne. **Fichiers** : chemin de package trop long → tronquer le segment intermédiaire par `.../` (garder préfixe `module/src/main|test` + suffixe parlant + fichier).
2. **Leçons durables (projet)** : reporter les leçons réutilisables dans le document cible sous `memoire/` (`CONVENTIONS.md`, `ARCHITECTURE.md`, ou annexe) avec lien `(← [session](memoire/session/….md))`. **Si la session change un état déjà documenté** (valeur de conf, statut de branche « non mergée », compteur, pattern remplacé), **mettre à jour le passage existant** — pas seulement éviter les doublons. Critères, tri, anti-doublons et état documenté → [reference.md](reference.md).
3. **Frictions méthode / harness** : uniquement à cette étape (jamais pendant la mission). Si une friction de méthode, harness, outil ou consigne a bloqué ou dégradé le travail et qu’elle est **promuable** vers `AGENTS.md` ou un skill : l’énoncer dans le chat (gabarit → [reference.md](reference.md) § Frictions harness). **Aucune écriture de fichier inbox.** **0** si rien de promuable. Pas de savoir projet, pas de récit de session. Signaler le nombre (`0` ou `N`) et la cible proposée (`AGENTS` | `skill:<nom>`). Ne patcher `AGENTS.md` / un skill que sur demande explicite de l’utilisateur.
4. **Langue** : français, concis (économie de tokens futures sessions).
5. **ctx purge** : appeler l’outil MCP `ctx_purge` avec `confirm: true` et `scope: "project"`. Irréversible : vide l’index FTS5 / events / stats context-mode du projet (pas les fichiers `memoire/`). Mentionner dans le chat que la purge est faite. Si le namespace MCP est absent, le signaler et ne pas bloquer la clôture.

## Référence détaillée

Nommage, critères de leçons, tableau de tri, frictions chat, template rapport : [reference.md](reference.md).
