from fastapi import FastAPI, Query
# Importer la librairie dotenv pour charger les variables d'environnement
from dotenv import load_dotenv

from backend.src import requete_api

"""
Ce fichier est le fichier principal de l'application.
Il contient la fonction principale qui permet de lancer l'application.
Il contient également les routes pour les différentes fonctionnalités de l'application.

Les routes sont :
- / : la route principale qui renvoie un message de bienvenue
- /jobs : la route pour rechercher les offres d'emploi pour une ville donnée

Les fonctionnalités sont :
- Rechercher les offres d'emploi pour une ville donnée
- Afficher les offres d'emploi pour une ville donnée
"""

# Charger les variables d'environnement
load_dotenv()
app = FastAPI()

_token: str | None = None


def _get_valid_token() -> str:
    global _token
    if _token is None:
        _token = requete_api.get_token()
        return _token

    if not requete_api.toujours_valide(_token):
        _token = requete_api.get_token()

    return _token


@app.get("/")
async def root():
    return {"message": "API emploi active"}

@app.get("/jobs")
async def jobs(code_postal: str = Query(...)):
    token = _get_valid_token()
    data = requete_api.jobs_ville(code_postal, token)

    return data


