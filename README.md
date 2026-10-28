# Commandes

Depuis la racine du repo (`~/Documents/config-cursor`) :

```bash
# Repo → machine (hooks, skills, settings, keybindings, cursor-storage)
# + miroir OpenCode (délègue à install-opencode.sh)
# + miroir jcode (délègue à install-jcode.sh)
./scripts/install.sh

# Repo → machine OpenCode only (AGENTS.md + skills + plugin garde-fou)
./scripts/install-opencode.sh

# Repo → machine jcode only (prompt-overlay, system-prompt, config.policy merge, skills → ~/.jcode)
./scripts/install-jcode.sh

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
