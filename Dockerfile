# Utiliser une image officielle de Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tout le contenu du répertoire local dans le répertoire /app dans le conteneur
COPY . /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Exécuter les migrations et collecter les fichiers statiques avant de lancer le serveur
CMD ["sh", "-c", "python /app/app/manage.py migrate && python /app/app/manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 app.wsgi:application"]
