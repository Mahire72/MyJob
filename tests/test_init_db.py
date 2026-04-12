import sys
from pathlib import Path

# IMPORTANT : avant les imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.src.db import init_db

import sqlite3

# Lance la création des tables
init_db()

# Vérifie que les tables existent
db_path = Path(__file__).resolve().parents[1] / "backend/profiles.sqlite3"
conn = sqlite3.connect(db_path)

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall()

print("Tables dans la DB :", tables)

conn.close()

def test_init_db():
    print("\n--- TEST INIT DB ---")

    # Lance la création des tables
    init_db()

    # Chemin DB
    db_path = Path(__file__).resolve().parents[1] / "backend/profiles.sqlite3"

    # Vérifier que le fichier existe
    assert db_path.exists(), "Fichier DB non créé"

    # Connexion
    conn = sqlite3.connect(db_path)

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    conn.close()

    print("Tables trouvées :", tables)

    # Transformer en liste simple
    table_names = [t[0] for t in tables]

    # Vérifier qu'il y a au moins une table
    assert len(table_names) > 0, " Aucune table trouvée"

    # Vérifier tables attendues (à adapter)
    assert "users" in table_names, "Table 'users' manquante"
    assert "profiles" in table_names, "Table 'profiles' manquante"

    print("TEST INIT DB OK")


if __name__ == "__main__":
    test_init_db()