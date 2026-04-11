# Projet MyJob 

Projet web simple pour rechercher des offres d’emploi (API France Travail), gérer un profil utilisateur, et afficher des recommandations.

## Auteurs

- 21213263 GOMEZ SANDOVAL Camilo  
- 21319773 MAIMAITI Maharemu

## Structure du projet

- **`backend/`** : API FastAPI + base SQLite (utilisateurs + profils)
- **`frontend/`** : pages HTML/CSS/JS (site statique)

## Prérequis

- Python 3.10+ (recommandé)
- `pip`
- Docker (optionnel)

## Installation (backend)

Depuis le dossier `backend/` :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Variables d’environnement

Le backend lit un fichier `backend/.env` (via `python-dotenv`). Un modèle est fourni dans `backend/.env.example` : copiez-le vers `backend/.env` et adaptez les valeurs.

Variables importantes :

- **`JWT_SECRET`** : secret pour signer les tokens JWT (obligatoire)
- **`FRANCE_TRAVAIL_CLIENT_ID`**, **`FRANCE_TRAVAIL_CLIENT_SECRET`** : accès à l’API France Travail (le scope OAuth est fixe dans `backend/src/requete_api.py`)
- **`DISABLE_SSL_CERT_VALIDATION`** : uniquement pour debug 


## Lancer l’API (backend)

Toujours depuis `backend/` (avec l’environnement virtuel activé) :

```bash
uvicorn main:app --reload
```

L’API démarre par défaut sur `http://127.0.0.1:8000`.

La base SQLite est créée automatiquement au lancement (fichier `backend/profiles.sqlite3`).

## Docker

Racine du dépôt, `backend/.env` présent pour le build.

**Compose (API + frontend)**

```bash
sudo apt install docker-compose
docker-compose up --build
```

```bash
docker compose down
```

- http://127.0.0.1:8080 — frontend  
- http://127.0.0.1:8000 — API  

**Backend seul**

```bash
docker build -t myjob-api ./backend
docker run --rm -p 8000:8000 myjob-api
```

```bash
docker run --rm -p 8000:8000 --env-file backend/.env myjob-api
```

```bash
docker run --rm -p 8000:8000 -e JWT_SECRET="..." myjob-api
```

SQLite sur l’hôte :

```bash
touch backend/profiles.sqlite3
docker run --rm -p 8000:8000 --env-file backend/.env \
  -v "$(pwd)/backend/profiles.sqlite3:/app/profiles.sqlite3" \
  myjob-api
```

## Lancer le frontend

Le frontend est statique. Le plus simple est d’ouvrir les fichiers HTML dans un navigateur :

- `frontend/se_connecter.html` (connexion)
- `frontend/creer_compte.html` (création de compte)
- `frontend/dashboard.html` (dashboard)
- `frontend/profile.html` (profil)

**Frontend seul**

```bash
docker build -t myjob-web ./frontend
docker run --rm -p 8080:80 myjob-web
```

http://127.0.0.1:8080/

## Authentification (résumé)

- `POST /register` et `POST /login` renvoient un **`access_token`**
- Les routes protégées attendent le header :

```text
Authorization: Bearer <access_token>
```

Routes protégées :
- `GET /profile`
- `POST /profile`
- `GET /jobs/recommended`
