# Référence — init-project-opencode

Templates **OpenCode-only**. Pour todo / lessons / PROJET / ANNEXE / CONVENTIONS /
ARCHITECTURE : copier depuis [`../init-project/reference.md`](../init-project/reference.md).

---

## Copie opencode.jsonc

Fichier cible : `opencode.jsonc` — copier **tel quel** (câblage OpenCode ; pas d’équivalent `.cursor` dans ce skill).

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Contexte injecté à chaque session (équivalent .cursor/rules/bootstrap.mdc)
  "instructions": [
    "memoire/PROJET.md",
    "memoire/ANNEXE.md"
  ]
}
```
