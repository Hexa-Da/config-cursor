---
name: jira
description: >-
  Drafts Jira tickets (summary + description with context and How to test)
  for MyShop Admin / MSHADM on portail.agir.orange.com. Use when the user
  asks for a ticket, US, story, bug Jira, rédaction Jira, How to test /
  qualif, or to turn work / a MR into a ticket — not for GitLab MR fetch.
---

# Jira ticket (rédaction)

Rédaction **à coller** dans Jira. Ne pas créer / éditer via API ou CLI 

Projet Jira : **MSHADM** (MyShop Admin) —
https://portail.agir.orange.com

## Checklist

```
- [ ] 1. Clarifier type (Story / Technical Story / Bug) et périmètre
- [ ] 2. Proposer Summary + Description (markdown prêt à coller)
- [ ] 3. How to test : smoke qualif, pas un plan technique
- [ ] 4. Pas de création Jira / API 
```

## Structure attendue

### Summary

- Court, verbe d’action, objet métier ou technique clair.
- **Préfixe** selon la mission réalisée :
  1. **`[Univers]`** — l’univers métier touché (ex. Mobile Ornage, 
     Internet Sosh, TV, Équipements…) ;
  2. **`[Transverse]`** — plusieurs univers ou socle partagé ;
  3. **`[TECH]`** — purement technique / refactor / dette outillage,
     sans angle métier dominant.
- Si le périmètre est ambigu : demander avant de choisir le préfixe.
- Exemples : `[Mobile Orange] …` ; `[Transverse] …` ;
  `[TECH] remplacer InputDate par InputDateTime`

### Description

1. **Contexte / objectif** — 1–3 phrases : quoi + pourquoi (lecteur =
   PO / qualif / collègue dev et archi).
2. **`## How to test`** — smoke pour la qualif :
   - familles d’écrans / parcours représentatifs (pas tout le catalogue) ;
   - puces observables (activer → résultat, enregistrer / recharger,
     message d’erreur, sync visible) ;
   - peu de jargon de code ; noms de composants OK s’ils apparaissent
     à l’UI ou sont déjà connus de la qualif ;
   - ne pas oublier les test de non rgeression si pertinent.

Ne pas remplir Acceptance Criteria / DoD / story points sauf demande.

## Format de sortie

Proposer **exactement** ce bloc (copier-coller) :

```markdown
**Summary:** …

**Description:**

…

*How to test*

1. …
   - …
2. …
   - …
```

Si des infos manquent (périmètre, écrans, critère d’acceptation) :
poser 1–3 questions ciblées avant de finaliser — ne pas inventer des
parcours faux.

## Exemple

```markdown
**Summary:** [TECH] remplacer InputDate par InputDateTime

**Description:**

Remplacement du composant legacy `InputDate` par `InputDateTime` sur
tous les call sites frontend

*How to test*

Smoke sur une famille d’écrans (pas tout le catalogue) :

1. Countdown — Promo, Teaser, Tag
   - Activer le timer → fin préremplie à 23:59 si vide
   - Enregistrer / recharger → valeur conservée
2. Périodes start/end — Segment, ODR commercial
   - Fin avant début → validation existante
3. Régression légère
   - Label timezone visible ; règle `future` plus stricte qu’avant
```
