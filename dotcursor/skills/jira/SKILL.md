---
name: jira
description: >-
  Drafts Jira tickets (summary + description with context and How to test)
  for MyShop Admin / MSHADM on portail.agir.orange.com. Use when the user
  asks for a ticket, US, story, bug Jira, rédaction Jira, How to test /
  qualif, commentaire Jira, or to turn work / a MR into a ticket — not for
  GitLab MR fetch.
---

# Jira ticket (rédaction)

Rédaction **à coller** dans Jira. Ne pas créer / éditer via API ou CLI.

Projet Jira : **MSHADM** (MyShop Admin) —
https://portail.agir.orange.com

## Checklist

```
- [ ] 1. Clarifier type (Story / Technical Story / Bug) et périmètre
- [ ] 2. Produire le corps (et le Summary si ticket neuf) en markdown à coller
- [ ] 3. How to test : smoke qualif, pas un plan technique
- [ ] 4. Pas de création Jira / API
```

## Structure du contenu

### Summary (ticket neuf seulement)

- Court, verbe d’action, objet métier ou technique clair.
- **Préfixe** :
  1. **`[Univers]`** — univers métier (ex. Mobile Orange, Internet Sosh…) ;
  2. **`[Transverse]`** — plusieurs univers ou socle partagé ;
  3. **`[TECH]`** — purement technique / refactor / dette.
- Périmètre ambigu → demander avant de choisir le préfixe.

### Corps (description ou commentaire)

1. **Contexte / objectif** — 1–3 phrases (PO / qualif / collègue).
2. ***How to test*** — smoke qualif :
   - parcours représentatifs (pas tout le catalogue) ;
   - puces observables (déposer → résultat, enregistrer / recharger,
     erreur métier) ;
   - peu de jargon ; non-régression si pertinent.

Pas d’Acceptance Criteria / DoD / story points sauf demande.

## Format de sortie (obligatoire)

1. Infos manquantes → 1–3 questions **avant** les fences (pas d’invention).
2. Sinon : **aucun** texte hors des fences.
3. Sortie = fence(s) prêts à copier-coller, **contenu = texte collé tel quel**
   dans le champ Jira (pas de wrappers `**Summary:**` / `**Description:**`
   à l’intérieur du fence).

### Commentaire ou mise à jour de description

Un seul fence `markdown` avec le corps :

````
```markdown
<1–3 phrases contexte>

*How to test*

1. …
   - …
2. …
   - …
```
````

### Ticket neuf (Summary + Description)

Deux fences séparés (un collé dans Summary, un dans Description) :

````
```markdown
[Transverse] …
```

```markdown
<corps + How to test>
```
````

## Exemple (commentaire / description)

````
```markdown
Sur les fiches complémentaires (Options, Internet et Mobile), permettre le dépôt d’une vidéo MP4 facultative (max 400 Mo) dans la section Présentation, sans titre ni description associés. La vidéo est exportée pour Katalog (consommation côté Katalog : MSHADM-5365).

*How to test*

1. Univers Options — fiche complémentaire existante
   - Ouvrir une fiche → section Présentation → bloc « Vidéo » visible après l’image principale
   - Déposer un MP4 ≤ 400 Mo → prévisualisation / fichier pris en compte
   - Enregistrer / recharger → la vidéo est conservée

2. Univers Internet ou Mobile — fiche complémentaire
   - Ouvrir une fiche hors Options → le bloc « Vidéo » est aussi présent après l’image principale
   - Déposer un MP4 ≤ 400 Mo, enregistrer / recharger → la vidéo est conservée

3. Limite de taille
   - Tenter un fichier > 400 Mo → message d’erreur métier, pas de dépôt

4. Non-régression Présentation
   - Titre, image principale, sections, complément d’info inchangés (Options et hors Options)
```
````
