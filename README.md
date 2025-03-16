
# Hassaniya - Dictionnaire Collaboratif

Ce projet est une application web pour la gestion collaborative du dictionnaire Hassaniya. Elle permet aux utilisateurs de proposer des mots, des définitions, et d'interagir via des commentaires.

## Prérequis

- **Git** pour cloner le projet.
- **Docker** pour exécuter l'application dans un conteneur.
- **Python 3.13+** (si vous choisissez d'exécuter le projet localement sans Docker).
- **Docker Compose** (optionnel, si vous souhaitez utiliser Docker pour la gestion complète de l'environnement).

## Installation du projet

### 1. Cloner le projet avec Git

Si vous ne l'avez pas encore, commencez par cloner le projet avec Git :

```bash
git clone https://github.com/Zeini-23025/defi-2-server.git
cd defi-2-server
```

### Résumé des étapes :

#### 1. **Avec Docker** :

- **Télécharger l'image Docker** :
  ```bash
  docker pull zeini/docker-server-dev
  ```

- **Exécuter l'application avec Docker** :
  ```bash
  docker run -p 8000:8000 zeini/docker-server-dev
  ```

#### 2. **Exécuter le projet localement avec Git & Python** :

Si vous souhaitez exécuter le projet localement sans Docker, suivez ces étapes :

- **Cloner le projet depuis GitHub** :
  ```bash
  git clone https://github.com/Zeini-23025/defi-2-server.git
  ```

- **Installer les dépendances Python** :
  ```bash
  pip install -r requirements.txt
  ```

- **Appliquer les migrations de la base de données** :
  ```bash
  python manage.py migrate
  ```

- **Démarrer le serveur de développement Django** :
  ```bash
  python manage.py runserver
  ```

L'application sera accessible à l'adresse `http://localhost:8000`.

## Liens utiles

- **Dépôt GitHub** : [https://github.com/Zeini-23025/defi-2-server.git](https://github.com/Zeini-23025/defi-2-server.git)
- **Image Docker** : [https://hub.docker.com/r/zeini/docker-server-dev](https://hub.docker.com/r/zeini/docker-server-dev)

Ce fichier `README.md` est maintenant prêt et contient toutes les instructions nécessaires pour cloner et exécuter votre projet, à la fois localement et via Docker.
