from fastapi import FastAPI, Query
# Importer la librairie dotenv pour charger les variables d'environnement
from dotenv import load_dotenv

from src import requete_api
from src.models import UserProfile
from src import db
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
#On initialise la base de données
db.init_db()

# Exemple de profil utilisateur (créé si absent)
if db.get_profile("default") is None:
    db.upsert_profile(
        "default",
        {
            "mots_cles": "developpeur python",
            "type_contrat": "CDI",
            "code_postal": "75013",
            "distance_max": 20,
            "salaire_min": 2000,
        },
    )

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
async def create_or_update_profile(profile: UserProfile, profile_id: str = Query("default")):
    stored = db.upsert_profile(profile_id, profile.model_dump())
    return {
        "message": "Profil créé ou mis à jour avec succès",
        "profile": stored,
    }

@app.get("/profile")
async def get_profile(profile_id: str = Query("default")):
    profile = db.get_profile(profile_id)
    if profile is None:
        return {
            "message": "Aucun profil trouvé",
            "profile": None
        }
    return {
        "message": "Profil récupéré avec succès",
        "profile": profile,
    }


@app.get("/jobs/recommended")
#Fonction pour récupérer les offres recommandées pour un profil donné
#/jobs/recommended?profile_id=default
async def recommended_jobs(profile_id: str = Query("default")):
    profile = db.get_profile(profile_id)
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