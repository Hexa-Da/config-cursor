# Commandes (perso)

Depuis la racine du repo (`~/Documents/config-cursor`) :

```bash
# Repo → machine (hooks, skills, settings, keybindings, cursor-storage)
./scripts/install.sh

# Machine → repo (export config Cursor)
./scripts/export.sh

# Canon lessons → tous les projets sous ~/Documents
./scripts/lessons-install.sh

# Canon bootstrap §1–3 → tous les projets sous ~/Documents (extras §4+ préservés)
./scripts/bootstrap-install.sh
```

Depuis le projet en cours (`~/Documents/projet`) :

```bash
# Projet courant → canon lessons (+ commit/push)
# À lancer depuis un projet qui a tasks/lessons.md mise à jour
~/Documents/config-cursor/scripts/lessons-export.sh

# Projet courant → canon bootstrap §1–3 (+ commit/push)
# À lancer après modification des règles CONVENTIONS / ARCHITECTURE / session
~/Documents/config-cursor/scripts/bootstrap-export.sh
```

## Couches de config

| Couche | Fichier | Contenu |
|--------|---------|---------|
| VS Code-like | `user/settings.json` (+ `keybindings.json`) | Éditeur, `cursor.composer.*`, etc. |
| Cursor product | `user/cursor-storage.json` | Agents/Review + Layout/General (extrait filtré de `state.vscdb`) |
| Dotcursor | `dotcursor/` | Hooks, skills, plugins, commands, agents |

`state.vscdb` brut reste **gitignoré**. Seul l’extrait allowlisté est versionné.
