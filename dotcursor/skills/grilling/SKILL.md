---
name: grilling
description: >-
  Grill the user relentlessly about a plan, decision, or idea via design-tree
  rounds (frontier questions + recommended answers). Use when the user wants to
  stress-test thinking, or uses grill / grilling / challenger une idée.
disable-model-invocation: true
---

# Grilling

Interroger l'utilisateur sans relâche jusqu'à un **accord partagé**. Cartographier
en **arbre de design** : chaque décision branche vers les décisions qui en
dépendent.

Travailler l'arbre en **rounds**. La **frontier** = toute décision dont les
prérequis sont déjà réglés (questions posables *maintenant* sans deviner des
réponses non entendues). Poser **toute** la frontier dans un round : numéroter
chaque question et donner ta réponse recommandée. Attendre les réponses avant
le round suivant.

## Format d'un round

```
❓ **Q1** - **<titre>**: <corps — peut être plusieurs paragraphes / choix>

➡️ <ta réponse recommandée>

---

❓ **Q2** - **<titre>**: <corps>

➡️ <ta réponse recommandée>
```

Chaque round de réponses reshape l'arbre : les décisions réglées poussent la
frontier et débloquent les questions dépendantes. Recalculer la frontier, poser
le round suivant. Une question dont la réponse dépend d'une autre encore ouverte
*dans ce round* appartient à un round **ultérieur**, pas à celui-ci.

## Faits vs décisions

Trouver les **faits** est ton job, jamais celui de l'utilisateur. Si une question
frontier a besoin d'un fait (filesystem, outils…), lancer un sous-agent ; ne pas
demander ce que tu peux chercher. Ne pas bloquer : une exploration en cours est
un prérequis non réglé — seules les questions en aval attendent ; poser le reste
de la frontier maintenant. Les **décisions** sont à l'utilisateur : les poser et
attendre.

## Fin

Session terminée quand la frontier est vide : chaque branche visitée, rien
d'assumé en silence. **Ne pas agir** sur le plan tant que l'utilisateur n'a pas
confirmé l'accord partagé.
