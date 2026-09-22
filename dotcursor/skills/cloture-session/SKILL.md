---
name: cloture-session
description: >-
  Procédure de clôture de session agent : rapport dans memoire/session/,
  mise à jour INDEX.md, leçons durables, reset tasks/todo.md.
  Use when the user asks to close, end, or clôturer the session.
disable-model-invocation: true
---

# Clôture de session

Procédure **générique**. Chemins repo par défaut : `memoire/session/`, `tasks/todo.md`.

## Checklist

```
- [ ] 1. Rapport de session (nouveau fichier, jamais modifier un rapport clos)
- [ ] 2. Ligne en tête de memoire/session/INDEX.md
- [ ] 3. Leçons durables → memoire/
- [ ] 4. Tout en français, concis
- [ ] 5. Reset tasks/todo.md au template vide
```

## Étapes

1. **Rapport** : s'appuyer sur `tasks/todo.md` comme brouillon. Copier le template (voir [reference.md](reference.md) § Template rapport) vers `memoire/session/AAAA-MM-JJ_HHmm_slug.md` et remplir. `HHmm` = heure locale à la clôture (voir [reference.md](reference.md) § Nommage). **Toujours un nouveau fichier** — même en continuation d'une session précédente. Continuité → lien en en-tête (« Suite de : [titre](fichier.md) »).
2. **Index** : ajouter une ligne **en haut** du tableau de `memoire/session/INDEX.md` (date, tags — voir légende dans l'INDEX, titre lien, résumé une phrase). Ne pas modifier les lignes existantes.
3. **Leçons durables** : reporter les leçons réutilisables dans le document cible sous `memoire/` (`CONVENTIONS.md`, `ARCHITECTURE.md`, ou annexe) avec lien `(← [session](memoire/session/….md))`. **Ne jamais modifier** `tasks/lessons.md` (lecture seule ; méthode transversale → noter dans le rapport / signaler à l'utilisateur). **Si la session change un état déjà documenté** (valeur de conf, statut de branche « non mergée », compteur, pattern remplacé), **mettre à jour le passage existant** — pas seulement éviter les doublons. Critères, tri, anti-doublons et état documenté → [reference.md](reference.md).
4. **Langue** : français, concis (économie de tokens futures sessions).
5. **Reset todo** : réinitialiser `tasks/todo.md` au template vide (voir [reference.md](reference.md) § Template todo).

## Référence détaillée

Nommage, critères de leçons, tableau de tri, templates (rapport, index, todo) : [reference.md](reference.md).
