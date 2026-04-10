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

## Installation (backend)

Depuis le dossier `backend/` :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Variables d’environnement

Le backend lit un fichier `backend/.env` (via `python-dotenv`).

Variables importantes :

- **`JWT_SECRET`** : secret pour signer les tokens JWT (obligatoire)
- **`FRANCE_TRAVAIL_CLIENT_ID`**, **`FRANCE_TRAVAIL_CLIENT_SECRET`**, **`FRANCE_TRAVAIL_SCOPE`** : accès à l’API France Travail
- **`DISABLE_SSL_CERT_VALIDATION`** : uniquement pour debug 


## Lancer l’API (backend)

Toujours depuis `backend/` (avec l’environnement virtuel activé) :

```bash
uvicorn main:app --reload
```

L’API démarre par défaut sur `http://127.0.0.1:8000`.

La base SQLite est créée automatiquement au lancement (fichier `backend/profiles.sqlite3`).

## Lancer le frontend

Le frontend est statique. Le plus simple est d’ouvrir les fichiers HTML dans un navigateur :

- `frontend/se_connecter.html` (connexion)
- `frontend/creer_compte.html` (création de compte)
- `frontend/dashboard.html` (dashboard)
- `frontend/profile.html` (profil)

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
