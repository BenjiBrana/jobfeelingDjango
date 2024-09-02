# Utiliser une image Python officielle
FROM python:3.11

# Installer Node.js et npm
RUN apt-get update && apt-get install -y nodejs npm

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des exigences et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers package.json et package-lock.json (si présent)
COPY package*.json /app/

# Installer les dépendances Node.js
RUN npm install

# Copier tout le code source dans le conteneur
COPY . /app/

# Construire les fichiers CSS avec Tailwind
RUN npm run build:css

# Exposer le port que Django utilisera
EXPOSE 8000

# Commande de lancement de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
