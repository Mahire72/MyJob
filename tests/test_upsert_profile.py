import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.src.db import create_user, upsert_profile, get_profile
import uuid

print("\n--- TEST PROFILE ---")

# créer user unique
email = f"test_{uuid.uuid4()}@mail.com"
user = create_user(email, "1234")

# créer profil
profile = upsert_profile(user["id"], {
    "nom": "Dupont",
    "prenom": "Jean",
    "email": email,
    "mots_cles": "python,backend",
    "code_postal": "75000",
    "type_contrat": "CDI",
    "distance_max": 20,
    "salaire_min": 30000
})

print("Profil créé :", profile)

# récupérer profil
fetched = get_profile(user["id"])
print("Profil récupéré :", fetched)



print("**************mise a jour*********")

# update profil
updated = upsert_profile(user["id"], {
    "nom": "Dupont",
    "prenom": "Jean",
    "email": email,
    "mots_cles": "python,fastapi",
    "code_postal": "75000"
})

print("Profil mis à jour :", updated)

##############################################################

def check(condition, success_msg, fail_msg):
    if condition:
        print(f"{success_msg}")
    else:
        print(f"{fail_msg}")


def test_upsert_profile():
    print("\n--- TEST PROFILE ---")

    # créer user unique
    email = f"test_{uuid.uuid4()}@mail.com"
    user = create_user(email, "1234")
    print("User créé :", user)

    # créer profil
    profile = upsert_profile(user["id"], {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": email,
        "mots_cles": "python,backend",
        "code_postal": "75000",
        "type_contrat": "CDI",
        "distance_max": 20,
        "salaire_min": 30000
    })

    print("Profil créé :", profile)

    check(profile is not None, "Création profil OK", "Création profil FAIL")

    # récupérer profil
    fetched = get_profile(user["id"])
    print("Profil récupéré :", fetched)

    check(fetched is not None, "Récupération profil OK", "Récupération profil FAIL")
    check(fetched["mots_cles"] == "python,backend", "Données correctes", "Données incorrectes")

    print("\n************** MISE A JOUR *********")

    # update profil
    updated = upsert_profile(user["id"], {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": email,
        "mots_cles": "python,fastapi",
        "code_postal": "75000"
    })

    print("Profil mis à jour :", updated)

    # vérifier update
    fetched_updated = get_profile(user["id"])
    print("Profil après update :", fetched_updated)

    check(
        fetched_updated["mots_cles"] == "python,fastapi",
        "Mise à jour OK",
        "Mise à jour FAIL"
    )


if __name__ == "__main__":
    test_upsert_profile()