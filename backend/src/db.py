import sqlite3
import hashlib
import secrets
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

"""
Base de données SQLite pour stocker les profils utilisateurs

"""
#Chemin de la base de données
_DB_PATH = Path(__file__).resolve().parents[1] / "profiles.sqlite3"

#Fonction pour se connecter à la base de données
def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#Fonction pour récupérer la date et l'heure UTC
def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

#Fonction pour hacher le mot de passe
def _hash_password(password: str, salt: bytes) -> str:
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return dk.hex()

#Fonction pour initialiser la base de données
#On crée la table profiles si elle n'existe pas
def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_salt BLOB NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                user_id TEXT PRIMARY KEY,
                nom TEXT,
                prenom TEXT,
                email TEXT,
                mots_cles TEXT NOT NULL,
                code_postal TEXT NOT NULL,
                type_contrat TEXT,
                distance_max INTEGER,
                salaire_min INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )


def create_user(email: str, password: str) -> dict:
    now = _utc_now()
    user_id = str(uuid4())
    salt = secrets.token_bytes(16)
    pwd_hash = _hash_password(password, salt)

    with _connect() as conn:
        try:
            conn.execute(
                """
                INSERT INTO users (id, email, password_salt, password_hash, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, email, salt, pwd_hash, now),
            )
        except sqlite3.IntegrityError as e:
            # Email déjà existant (UNIQUE)
            raise ValueError("Email déjà utilisé") from e

    return {"id": user_id, "email": email, "created_at": now}


def get_user_by_email(email: str) -> dict | None:
    with _connect() as conn:
        r = conn.execute(
            "SELECT id, email, password_salt, password_hash, created_at FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        return None if r is None else dict(r)


def verify_user(email: str, password: str) -> dict | None:
    user = get_user_by_email(email)
    if user is None:
        return None
    salt = user["password_salt"]
    expected = user["password_hash"]
    if _hash_password(password, salt) != expected:
        return None
    return {"id": user["id"], "email": user["email"], "created_at": user["created_at"]}


#Fonction pour insérer ou mettre à jour un profil
def upsert_profile(user_id: str, data: dict) -> dict:
    now = _utc_now()
    row = {
        "user_id": user_id,
        "nom": data.get("nom"),
        "prenom": data.get("prenom"),
        "email": data.get("email"),
        "mots_cles": data["mots_cles"],
        "code_postal": data["code_postal"],
        "type_contrat": data.get("type_contrat"),
        "distance_max": data.get("distance_max"),
        "salaire_min": data.get("salaire_min"),
        "created_at": now,
        "updated_at": now,
    }

    #On se connecte à la base de données
    with _connect() as conn:
        #On vérifie si le profil existe déjà
        existing = conn.execute(
            "SELECT user_id, created_at FROM profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if existing is not None:
            row["created_at"] = existing["created_at"]

        conn.execute(
            """
            INSERT INTO profiles (user_id, nom, prenom, email, mots_cles, code_postal, type_contrat, distance_max, salaire_min, created_at, updated_at)
            VALUES (:user_id, :nom, :prenom, :email, :mots_cles, :code_postal, :type_contrat, :distance_max, :salaire_min, :created_at, :updated_at)
            ON CONFLICT(user_id) DO UPDATE SET
                nom=excluded.nom,
                prenom=excluded.prenom,
                email=excluded.email,
                mots_cles=excluded.mots_cles,
                code_postal=excluded.code_postal,
                type_contrat=excluded.type_contrat,
                distance_max=excluded.distance_max,
                salaire_min=excluded.salaire_min,
                updated_at=excluded.updated_at
            """,
            row,
        )

    return get_profile(user_id)

#Fonction pour récupérer un profil
def get_profile(user_id: str) -> dict | None:
    with _connect() as conn:
        #On récupère le profil dans la base de données
        r = conn.execute(
            "SELECT user_id, nom, prenom, email, mots_cles, code_postal, type_contrat, distance_max, salaire_min, created_at, updated_at FROM profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if r is None:
            return None
        return dict(r)

