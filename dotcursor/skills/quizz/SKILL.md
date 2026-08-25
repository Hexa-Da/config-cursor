---
name: quizz
description: >-
  Quiz socratique d'assimilation après une session de code : questions
  techniques une par une sur ce qui vient d'être fait, feedback immédiat,
  sans écrire de fichier. Use when the user runs /quizz, asks for a quiz,
  assimilation, or to vérifier qu'il a compris la session.
disable-model-invocation: true
---

# Quizz d'assimilation

Interroger l'utilisateur **junior** pour vérifier qu'il a compris ce qu'il vient de faire — pas pour le piéger, pas pour rejouer le rapport.

**Interdit** : écrire ou modifier des fichiers (`memoire/`, `tasks/`, etc.). Tout reste dans le chat.

## Checklist

```
- [ ] 1. Cibler le périmètre (session / changements récents)
- [ ] 2. Poser 3 à 5 questions, UNE à la fois
- [ ] 3. Après chaque réponse : feedback court + enchaîner
- [ ] 4. Bilan final (forces / trous) — sans fichier
```

## Étape 1 — Périmètre

S'appuyer sur, dans cet ordre selon dispo :

1. Le fil de la conversation (ce qui vient d'être fait)
2. `tasks/todo.md` (Review / plan) si présent
3. Le dernier rapport sous `memoire/session/` **en lecture seule** si l'utilisateur le demande ou si le contexte chat est trop mince

Annoncer en une phrase le sujet du quizz, puis poser la Q1.

## Étape 2 — Questions (socratique)

**Règles** :

- Exactement **une** question par message ; attendre la réponse avant la suivante.
- **3 à 5** questions au total (4 par défaut).
- Niveau junior : vocabulary clair ; exiger le *pourquoi* et le *lien*, pas une récitation de noms de fichiers.
- Interdit : QCM trivia, « quelle ligne as-tu modifiée ? », spoiler de la bonne réponse dans l'énoncé.

**Répartition type** (adapter au sujet) :

| # | Type | Objectif |
| --- | --- | --- |
| 1 | Pourquoi | Motif du changement / du choix technique |
| 2 | Chaîne | Lien avec le reste (API, UI, data, tests…) |
| 3 | Et si… | Conséquence d'une variante ou d'une erreur |
| 4 | Reformulation | Expliquer en 2–3 phrases sans jargon inutile |
| 5 (opt.) | Transfert | Où réutiliserait-on la même idée ailleurs ? |

## Étape 3 — Feedback par réponse

Après chaque réponse, en **court** (3–6 lignes max) :

- Ce qui est juste
- Ce qui manque ou est flou (une correction ciblée)
- Si bloqué : un indice, **pas** la réponse complète ; relancer une fois, puis passer

Puis enchaîner avec la question suivante (sauf après la dernière).

## Étape 4 — Bilan

Sans fichier. Structure :

```markdown
## Bilan quizz

- **Assimilé** : …
- **À retravailler** : … (1–3 points concrets)
- **Prochaine révision** : une micro-action (relire X, refaire Y à la main, …)
```

Ne pas proposer de commit ni d'écriture `memoire/`.

## Anti-patterns

- Dump de 5 questions d'un coup
- Noter / scorer sur 10 (inutile) — privilégier assimilé vs trou
- Transformer le quizz en nouveau tutoriel long
- Modifier le rapport de session « pour y coller le quizz »
