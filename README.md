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
```
