from fastapi import FastAPI, Query
# Importer la librairie dotenv pour charger les variables d'environnement
from dotenv import load_dotenv

from src import requete_api
from src.models import UserProfile

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

# Store en mémoire (profil unique "default")
PROFILE_STORE: dict[str, dict] = {}

# Exemple de profil utilisateur
PROFILE_STORE["default"] = {
    "mots_cles": "developpeur python",
    "type_contrat": "CDI",
    "code_postal": "75013",
    "distance_max": 20,
    "salaire_min": 2000
}

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
async def jobs(
    code_postal: str = Query(...),
    mots_cles: str | None = Query(None),
    type_contrat: str | None = Query(None),
    distance_max: int | None = Query(None),
    salaire_min: int | None = Query(None),
):
    token = _get_valid_token()
    data = requete_api.jobs_ville(
        code_postal,
        token,
        mots_cles=mots_cles,
        type_contrat=type_contrat,
        distance_max=distance_max,
        salaire_min=salaire_min,
    )

    normalised = requete_api.normaliser_offres(data)
    if isinstance(normalised, dict) and isinstance(normalised.get("offres"), list):
        normalised["offres"] = normalised["offres"][:10]
    return normalised


@app.post("/profile")
async def create_or_update_profile(profile: UserProfile):
    PROFILE_STORE["default"] = profile.model_dump()
    return {
        "message": "Profil créé ou mis à jour avec succès",
        "profile": PROFILE_STORE["default"]
    }

@app.get("/profile")
async def get_profile():
    profile = PROFILE_STORE.get("default")
    if profile is None:
        return {
            "message": "Aucun profil trouvé",
            "profile": None
        }
    return {
        "message": "Profil récupéré avec succès",
        "profile": PROFILE_STORE["default"]
    }


@app.get("/jobs/recommended")
async def recommended_jobs():
    profile = PROFILE_STORE.get("default")
    if profile is None:
        return {
            "message": "Aucun profil trouvé",
            "jobs": []
        }
    token = _get_valid_token()

    data = requete_api.jobs_ville(
        code_postal=profile["code_postal"],
        token=token,
        mots_cles=profile["mots_cles"],
        type_contrat=profile["type_contrat"],
        distance_max=profile["distance_max"],
        salaire_min=profile["salaire_min"],
    )

    #ON oublie pas de normaliser les offres et limiter le nombre d'offres à 10 (a modifier plus tard)
    normalised = requete_api.normaliser_offres(data)
    if isinstance(normalised, dict) and isinstance(normalised.get("offres"), list):
        normalised["offres"] = normalised["offres"][:10]
    return normalised