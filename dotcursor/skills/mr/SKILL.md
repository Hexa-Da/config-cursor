---
name: mr
description: >-
  Genere un titre et une description de Merge Request a partir des
  changements realises. Use when the user asks for "titre MR",
  "description MR", "redige la MR", or "merge request".
---

# MR Writer

Genere un Titre et une Description de MR, en francais, a partir du travail reellement effectue.

## Sortie attendue (copier-coller GitLab)

Repondre uniquement avec ce bloc, sans texte avant/apres :

Titre :
[TECH] <titre concis et clair>

Description :
<description concise et claire, expliquant ce qui a ete fait, pourquoi, et l'impact fonctionnel/technique>

Si un ticket existe, remplacer [TECH] par [MSHADM-xxxx].

## Regle de sortie stricte

- Sortie = uniquement 2 sections : Titre : puis Description :
- Aucun markdown supplementaire (pas de puces, pas de sous-titres, pas d'emojis)
- Pas de phrase d'introduction ni de conclusion

## Regles

- Ne jamais inventer de ticket.
- Si un ticket existe (MSHADM-xxxx), l'utiliser comme prefixe.
- Sinon utiliser [TECH].
- Le titre doit rester court, oriente action, sans jargon inutile.
- La description doit etre factuelle, comprehensible par un reviewer.

## Detection du ticket (ordre)

1. Ticket explicitement donne par l'utilisateur.
2. Nom de branche (pattern MSHADM-\d+).
3. Messages de commit recents (pattern MSHADM-\d+).
4. Sinon [TECH].

## Verification minimale avant redaction

- Lire les fichiers modifies et le diff pour resumer fidelement.
- Si le scope n'est pas clair, poser une seule question ciblee.
- Si c'est clair, produire directement le resultat final.
