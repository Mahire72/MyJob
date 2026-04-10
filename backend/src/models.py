from pydantic import BaseModel
from typing import Optional

"""
Modèle de profil utilisateur
"""
class UserProfile(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[str] = None

    #mots clés de recherche obligatoires
    #code postal obligatoire
    mots_cles: str
    type_contrat: Optional[str] = None
    code_postal: str
    distance_max: Optional[int] = None
    salaire_min: Optional[int] = None


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str



