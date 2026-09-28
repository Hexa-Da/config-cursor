# Commandes

Depuis la racine du repo (`~/Documents/config-cursor`) :

```bash
# Repo → machine (hooks, skills, settings, keybindings, cursor-storage)
# + miroir OpenCode (délègue à install-opencode.sh)
./scripts/install.sh

# Repo → machine OpenCode only (AGENTS.md + skills)
./scripts/install-opencode.sh

# Machine → repo (export config Cursor)
./scripts/export.sh

# Canon lessons → tous les projets sous ~/Documents
./scripts/lessons-install.sh
```

Depuis le projet en cours (`~/Documents/projet`) :

```bash
# Projet courant → canon lessons (+ commit/push)
# À lancer depuis un projet qui a tasks/lessons.md mise à jour
bash ~/Documents/config-cursor/scripts/lessons-export.sh
```
