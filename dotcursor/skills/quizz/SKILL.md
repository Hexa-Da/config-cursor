---
name: quizz
description: >-
  Quiz socratique d'assimilation après une session de code : questions
  techniques (mécanismes, API, data, UI) une par une sur ce qui vient d'être
  fait, feedback immédiat, sans écrire de fichier. Use when the user runs
  /quizz, asks for a quiz, assimilation, or to vérifier qu'il a compris la
  session.
disable-model-invocation: true
---

# Quizz d'assimilation

Interroger l'utilisateur **junior** pour vérifier qu'il a compris les
**mécanismes du code** qu'il vient de toucher — pas pour le piéger, pas pour
rejouer le rapport, pas pour un cours d'architecture.

**Interdit** : écrire ou modifier des fichiers (`memoire/`, `tasks/`, etc.).
Tout reste dans le chat.

## Checklist

```
- [ ] 1. Cibler le périmètre (session / changements récents)
- [ ] 2. Extraire 3–5 *mécanismes* concrets du diff / rapport
- [ ] 3. Poser 3 à 5 questions, UNE à la fois (priorité code)
- [ ] 4. Après chaque réponse : feedback court + enchaîner
- [ ] 5. Bilan final (forces / trous) — sans fichier
```

## Étape 1 — Périmètre + inventaire technique

S'appuyer sur, dans cet ordre selon dispo :

1. Le fil de la conversation (ce qui vient d'être fait)
2. `tasks/todo.md` (Review / plan) si présent
3. Le dernier rapport sous `memoire/session/` **en lecture seule** si
   l'utilisateur le demande ou si le contexte chat est trop mince
4. Au besoin : **lire 1–3 fichiers** du diff (DAO, search, composant, test)
   pour ancrer les questions dans le code réel — lecture seule

Avant Q1, lister mentalement **3–5 mécanismes** touchés (ex. lambda DAO,
projection minimale, curseur `lastId`/`lastLabel`, prédicat filtre,
`migratedEntities`, prop `withoutValidation`). Annoncer le sujet en une
phrase, puis poser la Q1.

## Étape 2 — Questions (socratique, niveau code)

**Règles** :

- Exactement **une** question par message ; attendre la réponse avant la suivante.
- **3 à 5** questions au total (4 par défaut).
- Niveau junior : vocabulaire clair ; exiger le *rôle du mécanisme* et le
  *lien data/API/UI*, pas une récitation de chemins de fichiers.
- Interdit : QCM trivia, « quelle ligne as-tu modifiée ? », spoiler de la
  bonne réponse dans l'énoncé.

### Priorité : technique concrète (obligatoire)

Au moins **3 questions sur 4** portent sur un **mécanisme** visible dans le
code ou le rapport technique — pas sur la stratégie git / le « pourquoi
métier de haut niveau » seuls.

Exemples de cibles (adapter au sujet, ne pas inventer ce qui n'était pas
dans le périmètre) :

| Couche | Exemples de questions |
| --- | --- |
| Backend data | À quoi sert une **lambda** passée à un search partagé dans les DAO ? Que transporte une **projection minimale** vs l'entité complète ? |
| Search / filtre | Que font `lastId` / `lastLabel` ? Pourquoi `.onEditos()` pour auteur/date ? Différence prédicat plat vs `searchEquipments` ? |
| API | Pourquoi un endpoint `…/authors` séparé ? Que renvoie `remainingCount` ? |
| Front | Que décide `migratedEntities` ? Pourquoi pas `useForm` sur une barre de filtre ? Rôle d'un cache de pages côté client ? |
| Tests | Qu'est-ce qu'un test de search vérifie vraiment (curseur, filtre, mapping) ? |

**Formulations qui marchent** :

- « Dans le search X, à quoi sert Y — que se passe-t-il si on l'omet ? »
- « La lambda Z injectée dans le DAO : que doit-elle faire / retourner ? »
- « Entre le champ A du modèle et le param query B, quel est le lien ? »

### À éviter / reléguer

- Questions **uniquement** archi / process / git : merge de branches, « pourquoi
  une MR séparée », « explique la crémaillère en 3 phrases » **sans** ancrage
  code — sauf si l'utilisateur le demande explicitement.
- Une seule question « stratégie » max, et seulement en **5e** (opt.), jamais
  en Q1–Q2.
- Reformulation floue type « explique le sujet à un junior » → préférer
  « explique **ce mécanisme** en 2 phrases ».

**Répartition type** (adapter ; rester concret) :

| # | Type | Objectif |
| --- | --- | --- |
| 1 | Mécanisme | Rôle d'un artefact code touché (lambda, projection, curseur, gate…) |
| 2 | Chaîne data | Lien backend ↔ API ↔ UI / store (un flux précis) |
| 3 | Et si… | Conséquence d'une omission ou mauvaise variante **dans le code** |
| 4 | Reformulation | Expliquer **ce** mécanisme en 2–3 phrases simples |
| 5 (opt.) | Transfert ou stratégie | Où réutiliser le même pattern — ou, si vraiment utile, un choix process |

## Étape 3 — Feedback par réponse

Après chaque réponse, en **court** (3–6 lignes max) :

- Ce qui est juste
- Ce qui manque ou est flou (une correction ciblée, éventuellement un
  symbole / signature sans dump de fichier)
- Si bloqué : un indice **code** (nom de param, type de retour, appel
  voisin), **pas** la réponse complète ; relancer une fois, puis passer

Puis enchaîner avec la question suivante (sauf après la dernière).

## Étape 4 — Bilan

Sans fichier. Structure :

```markdown
## Bilan quizz

- **Assimilé** : … (mécanismes)
- **À retravailler** : … (1–3 points concrets, préférer symboles / flux)
- **Prochaine révision** : une micro-action (relire X, tracer Y dans le
  debugger, réécrire le prédicat à la main, …)
```

Ne pas proposer de commit ni d'écriture `memoire/`.

## Anti-patterns

- Dump de 5 questions d'un coup
- Noter / scorer sur 10 — privilégier assimilé vs trou
- Tutoriel long à la place d'un feedback court
- Quizz « culture projet / archi globale » sans ouvrir le code
- Q1 sur branches / merge / process alors que le diff est du search/DAO/UI
- Modifier le rapport de session « pour y coller le quizz »
