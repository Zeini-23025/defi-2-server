# Utiliser l'image officielle de Python comme image de base
FROM python:3.10

# Définir le répertoire de travail à /app
WORKDIR /app/app

# Copier tous les fichiers du projet dans le répertoire /app
COPY . /app/

# Installer les dépendances à partir de requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exposer le port 8000 pour que l'application soit accessible
EXPOSE 8000

# Commande d'exécution du conteneur
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 app.wsgi:application"]
