import sqlite3
from datetime import datetime, timezone
from pathlib import Path

"""
Base de données SQLite pour stocker les profils utilisateurs
"""
#Chemin de la base de données
_DB_PATH = Path(__file__).resolve().parents[1] / "profiles.sqlite3"

#Fonction pour se connecter à la base de données
def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

#Fonction pour initialiser la base de données
#On crée la table profiles si elle n'existe pas
def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id TEXT PRIMARY KEY,
                mots_cles TEXT NOT NULL,
                code_postal TEXT NOT NULL,
                type_contrat TEXT,
                distance_max INTEGER,
                salaire_min INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

#Fonction pour insérer ou mettre à jour un profil
def upsert_profile(profile_id: str, data: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    row = {
        "id": profile_id,
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
            "SELECT id, created_at FROM profiles WHERE id = ?",
            (profile_id,),
        ).fetchone()
        if existing is not None:
            row["created_at"] = existing["created_at"]

        conn.execute(
            """
            INSERT INTO profiles (id, mots_cles, code_postal, type_contrat, distance_max, salaire_min, created_at, updated_at)
            VALUES (:id, :mots_cles, :code_postal, :type_contrat, :distance_max, :salaire_min, :created_at, :updated_at)
            ON CONFLICT(id) DO UPDATE SET
                mots_cles=excluded.mots_cles,
                code_postal=excluded.code_postal,
                type_contrat=excluded.type_contrat,
                distance_max=excluded.distance_max,
                salaire_min=excluded.salaire_min,
                updated_at=excluded.updated_at
            """,
            row,
        )

    return get_profile(profile_id)

#Fonction pour récupérer un profil
def get_profile(profile_id: str) -> dict | None:
    with _connect() as conn:
        #On récupère le profil dans la base de données
        r = conn.execute(
            "SELECT id, mots_cles, code_postal, type_contrat, distance_max, salaire_min, created_at, updated_at FROM profiles WHERE id = ?",
            (profile_id,),
        ).fetchone()
        if r is None:
            return None
        return dict(r)

