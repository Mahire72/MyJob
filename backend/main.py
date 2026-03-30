from fastapi import FastAPI, Query
# Importer la librairie dotenv pour charger les variables d'environnement
from dotenv import load_dotenv

from backend.src import requete_api

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


