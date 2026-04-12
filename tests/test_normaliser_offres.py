import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.src.requete_api import normaliser_offres


def check(test_name, condition):
    if condition:
        print(f"{test_name} : OK")
    else:
        print(f"{test_name} : FAIL")


def test_normaliser_offres():
    print("\n--- TEST NORMALISER OFFRES ---")

    #input non dict
    result = normaliser_offres("pas un dict")
    print("Résultat :", result)
    check("Input non dict", result == {"offres": [], "total": 0})

    #Test 2 : propagation erreur
    data = {"error": "API down"}
    result = normaliser_offres(data)
    print("Résultat :", result)
    check("Propagation erreur", result == data)

    #structure standard
    data = {
        "resultats": [
            {
                "id": "123",
                "intitule": "Développeur Python",
                "entreprise": {"nom": "TechCorp"},
                "lieuTravail": {"libelle": "Paris", "codePostal": "75000"},
                "origineOffre": {"urlOrigine": "http://example.com"},
            }
        ],
        "nombreResultats": 1,
    }

    result = normaliser_offres(data)
    offre = result["offres"][0]

    print("Offre :", offre)

    check("Total correct", result["total"] == 1)
    check("Titre correct", offre["titre"] == "Développeur Python")
    check("Entreprise correcte", offre["entreprise"] == "TechCorp")
    check("Lieu correct", offre["lieu"] == "Paris")
    check("Code postal correct", offre["code_postal"] == "75000")
    check("URL correcte", offre["url"] == "http://example.com")

    #structure alternative
    data = {
        "results": [
            {
                "id": "456",
                "title": "Data Engineer",
                "company": {"name": "DataCorp"},
                "location": {"label": "Lyon", "postalCode": "69000"},
                "applyUrl": "http://apply.com",
            }
        ],
        "total": 1,
    }

    result = normaliser_offres(data)
    offre = result["offres"][0]

    print("Offre alt :", offre)

    check("Titre alt", offre["titre"] == "Data Engineer")
    check("Entreprise alt", offre["entreprise"] == "DataCorp")
    check("Lieu alt", offre["lieu"] == "Lyon")
    check("Code postal alt", offre["code_postal"] == "69000")
    check("URL alt", offre["url"] == "http://apply.com")

    #champs manquants
    data = {"resultats": [{"id": "789"}]}
    result = normaliser_offres(data)
    offre = result["offres"][0]

    print("Offre champs manquants :", offre)

    check("Titre None", offre["titre"] is None)
    check("Entreprise None", offre["entreprise"] is None)
    check("Lieu None", offre["lieu"] is None)
    check("URL None", offre["url"] is None)

    #liste invalide
    data = {
        "resultats": [
            {"id": "ok"},
            "bad",
            123,
        ]
    }

    result = normaliser_offres(data)

    print("Liste filtrée :", result["offres"])

    check("Ignore invalid", len(result["offres"]) == 1)
    check("ID correct", result["offres"][0]["id"] == "ok")

    #fallback total
    data = {"resultats": [{"id": "1"}, {"id": "2"}]}
    result = normaliser_offres(data)

    print("Total fallback :", result["total"])

    check("Total fallback", result["total"] == 2)


if __name__ == "__main__":
    test_normaliser_offres()