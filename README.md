# Commandes (perso)

Depuis la racine du repo (`~/Documents/config-cursor`) :

```bash
# Repo → machine (hooks, skills, settings, keybindings)
./scripts/install.sh

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