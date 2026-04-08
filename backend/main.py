from fastapi import FastAPI, Query
from fastapi import HTTPException
from dotenv import load_dotenv


#importation des middleware pour la gestion des CORS
from fastapi.middleware.cors import CORSMiddleware

from src import db, requete_api
from src.models import UserLogin, UserProfile, UserRegister



"""
Ce fichier est le fichier principal de l'application.
Il contient la fonction principale qui permet de lancer l'application.
Il contient également les routes pour les différentes fonctionnalités de l'application.

Les routes sont :
- / : la route principale qui renvoie un message de bienvenue
- /jobs : la route pour rechercher les offres d'emploi pour une ville donnée
- /profile : la route pour créer ou mettre à jour un profil utilisateur
- /profile : la route pour récupérer un profil utilisateur
- /jobs/recommended : la route pour récupérer les offres recommandées pour un profil utilisateur
- /registers : la route pour créer un utilisateur
- /login : la route pour se connecter à l'application

Les fonctionnalités sont :
- Rechercher les offres d'emploi pour une ville donnée
- Afficher les offres d'emploi pour une ville donnée
- Créer ou mettre à jour un profil utilisateur
- Récupérer un profil utilisateur
- Récupérer les offres recommandées pour un profil utilisateur
- Créer un utilisateur
- Se connecter à l'application
"""

# Charger les variables d'environnement
load_dotenv()
app = FastAPI()
#On initialise la base de données
db.init_db()

# CORS permet des appels depuis le frontend statique
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def create_or_update_profile(
    profile: UserProfile,
    user_id: str = Query(...),
):
    stored = db.upsert_profile(user_id, profile.model_dump())
    return {
        "message": "Profil créé ou mis à jour avec succès",
        "profile": stored,
    }

@app.get("/profile")
async def get_profile(user_id: str = Query(...)):
    profile = db.get_profile(user_id)
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
#Route pour récupérer les offres recommandées pour un profil donné
#/jobs/recommended?profile_id=default
async def recommended_jobs(user_id: str = Query(...)):
    profile = db.get_profile(user_id)
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


@app.post("/register")
async def register(payload: UserRegister):
    try:
        user = db.create_user(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Utilisateur créé avec succès", "user": user}


@app.post("/login")
async def login(payload: UserLogin):
    user = db.verify_user(payload.email, payload.password)
    if user is None:
        return {"message": "Identifiants invalides", "user": None}
    return {"message": "Connexion réussie", "user": user}