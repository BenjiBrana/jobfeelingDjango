# JobFeeling - Projet Django
## 1. Description

JobFeeling est une application web développée avec Django, permettant de connecter des utilisateurs à des services de conseils et d'agences. Le projet utilise Django pour le backend et TailwindCSS pour le style frontend.

## 2. Prérequis

- Python 3.11+ (Vérifiez avec `python3 --version`)
- Django 3.x+ (Installez via `pip install django`)
- MySQL pour la base de données
- Node.js et npm (pour TailwindCSS)
- Git (pour le contrôle de version)

## 3. Installation

1. **Clonez le dépôt** :

   ```bash
   git clone https://github.com/votreutilisateur/jobfeeling.git
   cd jobfeeling

    python3 -m venv env
    source env/bin/activate  # Sur Windows utilisez `env\Scripts\activate`
    pip install -r requirements.txt

## 4. Configurez les variables d'environnement :

DJANGO_SECRET_KEY='votre_cle_secrete'
DJANGO_DEBUG=True
MYSQL_DATABASE='nom_de_votre_base'
MYSQL_USER='votre_utilisateur'
MYSQL_PASSWORD='votre_mot_de_passe'
MYSQL_HOST='localhost'
MYSQL_PORT='3306'

python manage.py migrate
python manage.py collectstatic
python manage.py runserver


### 5. Déploiement

Expliquez comment déployer le projet sur un serveur, comme o2switch avec Apache et Passenger.

```markdown
## Déploiement

Pour déployer le projet sur un serveur (comme o2switch), suivez les étapes ci-dessous :

**Préparez l'environnement de production** :
   - Désactivez le mode DEBUG dans votre fichier `.env` : `DJANGO_DEBUG=False`.
   - Ajoutez le nom de domaine et l'adresse IP à `ALLOWED_HOSTS` dans `settings.py`.

python manage.py migrate 
python manage.py collectstatic --noinput


### 6. Utilisation

Expliquez brièvement comment utiliser l'application une fois installée.


## 7. Utilisation

1. Accédez à l'interface d'administration pour gérer les utilisateurs et les contenus : `/admin`.
2. Connectez-vous avec vos identifiants administrateur pour accéder aux fonctionnalités de gestion.
3. Naviguez sur le site pour découvrir les fonctionnalités et services disponibles.

## 8. Crédits

- Développé par [Brana Benjamin](https://branabenjamin.fr)
- Framework : [Django](https://www.djangoproject.com/)
- Style : [TailwindCSS](https://tailwindcss.com/)
- Hébergement : [o2switch](https://www.o2switch.fr/)
