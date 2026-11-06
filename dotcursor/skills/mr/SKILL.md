---
name: mr
description: >-
  Genere un titre et une description de Merge Request a partir des
  changements realises. Use when the user asks for "titre MR",
  "description MR", "redige la MR", "ajoute a la description de la MR",
  or "merge request".
---

# MR Writer

Genere un titre et/ou une description de MR, en francais, a partir du
travail reellement effectue. Sortie = texte **a coller** dans GitLab.
Ne pas pousser via `glab` / API (souvent 403) sauf demande explicite
« mets a jour la MR » *et* token OK ; en cas d’echec API, revenir au
texte a coller.

## Checklist

```
- [ ] 1. Detecter le ticket (MSHADM-xxxx) ou [TECH]
- [ ] 2. Lire diff / commits pour resumer fidelement
- [ ] 3. Produire fence(s) prets a coller
- [ ] 4. Pas d’ecriture GitLab sauf demande explicite
```

## Detection du ticket (ordre)

1. Ticket explicitement donne par l’utilisateur.
2. Nom de branche (pattern MSHADM-\d+).
3. Messages de commit recents (pattern MSHADM-\d+).
4. Sinon `[TECH]`.

Ne jamais inventer de ticket.

## Contenu

- **Titre** : court, oriente action ; prefixe `[MSHADM-xxxx]` ou `[TECH]`.
- **Description** : factuelle ; markdown GitLab OK (listes, backticks).
  Resume + guide commit par commit si l’historique le justifie.
- Description existante a completer → reprendre le texte et n’ajouter
  que les lignes manquantes.

## Format de sortie (obligatoire)

1. Scope flou → une question **avant** les fences.
2. Sinon : **aucun** texte hors des fences.
3. Contenu du fence = texte colle **tel quel** dans GitLab (pas de
   wrappers `**Titre:**` / `**Description:**` a l’interieur).

### Mise a jour / corps de description seul

Fence **sans** language tag (comme l’UI GitLab description) :

````
```
<resume une phrase>

Guide de lecture commit par commit :

1. …
2. …
```
````

### MR neuve (titre + description)

Deux fences : titre dans un fence `markdown` court, description dans un
fence sans language tag :

````
```markdown
[MSHADM-xxxx] …
```

```
<description>
```
````

## Exemple (description)

````
```
Ajoute le dépôt d’une vidéo MP4 (max 400 Mo) sur les fiches complémentaires (Options, Internet et Mobile) : stockage plat `video: MongoVisual?` (type `ADDITIONAL_DOCUMENT_VIDEO`), export `video: ProxyMediaVisualExport`, UI transverse (`VideoSelector`, sans titre ni description). Bump `export-api` 3.53.0.

Guide de lecture commit par commit :

1. fondations : `VisualTypesEnum` `ADDITIONAL_DOCUMENT_VIDEO` (409600 Ko), enregistrement OPTIONS, Mongock `ChangeLogsSprint202623` (sprint 3.53), champs plats initiaux sur `AdditionalDocumentEdito` + `extractVisuals`, factorisation `visualTypeDefinitionsForVideo`.
2. export : mapping `toHostedImageExport` / `toProxyMediaVisual`, omit si média absent, tests mapper (forme nestée temporaire avec title/description à ce stade).
3. front : bloc après l’image principale dans `AdditionalDocumentPresentationSection` (`v-if` Options), `VideoSelector` + titre/description (état intermédiaire).
4. docs + rapport de session.
5. fix rendu UI (marge basse `VideoSelector`).
6. mini review (constante Options, com taille vidéo).
7. retour MR : regroupement temporaire en bloc nesté `AdditionalDocumentVideo` (edito aligné sur l’export), UI `edito.video.*` + init si null, `MODEL_API_CONTRACTS`.
8. docs session — retour nesté.
9. décision finale : aplatir `video: MongoVisual?`, retirer titre/description (UI + modèle + export), supprimer `AdditionalDocumentVideo` / `AdditionalDocumentVideoExport`.
10. retour MR — transverse : retirer le filtre Options côté UI ; enregistrer `ADDITIONAL_DOCUMENT_VIDEO` sur tous les univers avec fiches complémentaires ; élargir Mongock `202623-001` (Options + Internet/Mobile) ; bump `export-api` 3.52.0 → 3.53.0 ; doc + rapport de session.
```
````
