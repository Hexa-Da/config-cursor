# Commandes

Depuis la racine du repo (`~/Documents/config-cursor`) :

```bash
# Repo → machine (hooks, skills, settings, keybindings, cursor-storage)
# + miroir OpenCode (délègue à install-opencode.sh)
# + miroir jcode (délègue à install-jcode.sh)
./scripts/install.sh

# Repo → machine OpenCode only (user-rules/opencode/AGENTS.md + skills)
./scripts/install-opencode.sh

# Repo → machine jcode only (AGENTS.md, system-prompt.md, skills → ~/.jcode)
./scripts/install-jcode.sh

# Machine → repo (export config Cursor)
./scripts/export.sh

# Canon lessons → tous les projets sous ~/Documents
./scripts/lessons-install.sh
```

## User rules

Une variante par harness dans `user-rules/` :

| Fichier | Destination |
| --- | --- |
| `user-rules/cursor/AGENTS.md` | Cursor → Settings → Rules (copier-coller, non scriptable) |
| `user-rules/opencode/AGENTS.md` | `~/.config/opencode/AGENTS.md` (`install-opencode.sh`) |
| `user-rules/jcode/AGENTS.md` | `~/AGENTS.md` (`install-jcode.sh`) |
| `user-rules/jcode/system-prompt.md` | `~/.jcode/system-prompt.md` (`install-jcode.sh`) |

Depuis le projet en cours (`~/Documents/projet`) :

```bash
# Projet courant → canon lessons (+ commit/push)
# À lancer depuis un projet qui a tasks/lessons.md mise à jour
bash ~/Documents/config-cursor/scripts/lessons-export.sh
```
