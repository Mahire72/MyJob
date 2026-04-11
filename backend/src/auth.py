import os
import time
from datetime import timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

"""
Ce fichier contient les fonctions pour la creation et la verification des tokens
- _bearer : pour la verification des tokens
- create_access_token() : pour la creation du token d'accès
- verify_access_token() : pour la verification du token d'accès
- get_current_user_id() : pour la récupération de l'id de l'utilisateur connecté
"""

load_dotenv()

JWT_SECRET = (os.getenv("API_KEY3") or os.getenv("JWT_SECRET") or "").strip()
if not JWT_SECRET:
    raise RuntimeError("Secret manquant : API_KEY3 (déploiement) ou JWT_SECRET (local)")

_bearer = HTTPBearer()


def create_access_token(*, user_id: str, expires_in_seconds: int = 60 * 60 * 24 * 7) -> str: #on crée le token d'accès
    now = int(time.time())
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + int(timedelta(seconds=expires_in_seconds).total_seconds()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256") #on encode le token avec le secret et l'algorithme HS256


def verify_access_token(token: str) -> str: #on verifie le token d'accès
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Token expiré") from e
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Token invalide") from e

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Token invalide")
    return user_id #on retourne l'id de l'utilisateur connecté


def get_current_user_id(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    if creds is None or creds.scheme.lower() != "bearer": #si le token n'est pas défini ou si le scheme n'est pas bearer
        raise HTTPException(status_code=401, detail="Authentification requise")
    return verify_access_token(creds.credentials) #on verifie le token et on retourne l'id de l'utilisateur connecté

