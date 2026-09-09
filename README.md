# Commandes (perso)

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
~/Documents/config-cursor/scripts/lessons-export.sh
```

## Couches de config


| Couche            | Fichier                                 | Contenu                                                                                         |
| ----------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------- |
| VS Code-like      | `user/settings.json` `keybindings.json` | Éditeur, `cursor.composer.*`, etc.                                                              |
| Cursor product    | `user/cursor-storage.json`              | Agents/Review + Layout/General (extrait filtré de `state.vscdb`)                                |
| Dotcursor         | `dotcursor/`                            | Hooks, skills, commands, agents                                                                 |
| User rules        | `AGENTS.md` (racine)                    | Cursor User Rules + OpenCode `~/.config/opencode/AGENTS.md` (via `install-opencode.sh`)         |
| OpenCode (skills) | `~/.config/opencode/skills/`            | Miroir de `dotcursor/skills/` via `install-opencode.sh` (frontmatter `compatibility: opencode`) |
| OpenCode (projet) | `opencode.jsonc` (racine du repo)       | Câblage local via skill `init-project-opencode` (`instructions` → `memoire/` + `tasks/`)         |
