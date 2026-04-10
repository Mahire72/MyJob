import httplib2
import json
import os
from urllib.parse import urlencode

import certifi
from .utils import extraire_salaire
from dotenv import load_dotenv

'''
Ce fichier contient les fonctions pour faire les requêtes à l'API de France Travail
_
- get_token() : pour obtenir un token d'accès
- toujours_valide() : pour vérifier si le token est toujours valide
- jobs_ville() : pour rechercher les offres d'emploi pour une ville donnée

Les variables d'environnement sont :
- FRANCE_TRAVAIL_CLIENT_ID : l'ID du client
- FRANCE_TRAVAIL_CLIENT_SECRET : le secret du client
- FRANCE_TRAVAIL_SCOPE : le scope de l'accès
- DISABLE_SSL_CERT_VALIDATION : pour désactiver la validation du certificat SSL

- _http() : pour créer une instance de la classe Http de la librairie httplib2
- _require_secrets() : pour vérifier si les variables d'environnement sont présentes

'''


ACCESS_POINT = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
Recherche_API = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

# Charger les variables d'environnement
load_dotenv()

client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")
scope = os.getenv("FRANCE_TRAVAIL_SCOPE", "api_offresdemploiv2 o2dsoffre")

# Vérifier si la validation du certificat SSL est désactivée
# Si oui, on désactive la validation du certificat SSL
#cela du à un problème de certificat SSL avec la librairie httplib2
_disable_ssl_validation = os.getenv("DISABLE_SSL_CERT_VALIDATION", "false").strip().lower() in {
    "1",
    "true",
    "yes",
    "y",
    "on",
}

# Fonction pour créer une instance de la classe Http de la librairie httplib2
#Je l'ai rajoutéé car problème ssl avec la librairie httplib2
def _http() -> httplib2.Http:
    if _disable_ssl_validation:
        return httplib2.Http(disable_ssl_certificate_validation=True)
    return httplib2.Http(ca_certs=certifi.where())

# Fonction pour vérifier si les variables d'environnement sont présentes
def _require_secrets() -> None:
    if not client_id or not client_secret:
        raise RuntimeError(
            "Il manque les variables d'environnement"
        )


def get_token():
    _require_secrets()
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    body = (
        "grant_type=client_credentials"
        + "&client_id="
        + client_id
        + "&client_secret="
        + client_secret
        + "&scope="
        + scope
    )
    reponse, data = _http().request(
        ACCESS_POINT, method="POST", headers=header, body=body
    )

    p = json.loads(data.decode())
    return p["access_token"]


def toujours_valide(token):
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search?motsCles=developpeur"

    reponse, data = _http().request(url, method="GET", headers=headers)

    return reponse.status != 400


def jobs_ville(
    code_postal,
    token,
    mots_cles=None,
    type_contrat=None,
    distance_max=None,
    salaire_min=None,
):
    # On a besoin du code INSEE pour faire la requete France Travail
    #Pour faire cela on se sert d'une nouvelle API de opendatasoft (base de donnees des communes)

    url = (
        "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
        "correspondance-code-cedex-code-insee/records/?limit=10&offset=0&where=code+%3D+"
        + str(code_postal)
    )
    reponse, data = _http().request(url, method="GET")

    if not (200 <= reponse.status < 300):
        #Erreur code postale non valide à traiter
        return {"error": "Code postal invalide ou API indisponible", "status": reponse.status}

    data_json = json.loads(data.decode()
    )
    # Vérifier si le code INSEE est présent dans les résultats
    if "results" not in data_json or len(data_json["results"]) == 0:
        return {"error": "Aucun code INSEE trouvé pour ce code postal"}

    code_insee = data_json["results"][0]["insee"]
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
    }
    params = {"commune": str(code_insee)}
    if mots_cles:
        params["motsCles"] = str(mots_cles)
    if type_contrat:
        params["typeContrat"] = str(type_contrat)
    if distance_max is not None:
        params["distanceMax"] = str(distance_max)

    #Attention, salaire_min ne fonctionne pas, l'api retourne un STRING avec un format different de celui attendu
    #Il faut donc depurer le string pour obtenir le salaire min en int
    #Exemple de string retourne par l'api : "Mensuel de 1823.03 Euros à 2500.0 Euros sur 12.0 mois"
    #On doit utiliser une expression reguliere pour extraire le salaire min
    #A faire plus tard - resolu utiliser la fonction extraire_salaire de utils.py
    #le filtrage sera fait côté backend après normalisation
    if salaire_min is not None:
        params["salaireMin"] = str(salaire_min)

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search?" + urlencode(
        params, doseq=True
    )

    reponse, data = _http().request(url, method="GET", headers=headers)
    if not (200 <= reponse.status < 300):
        return {"error": "Erreur lors de la récupération des offres", "status": reponse.status}


    #on charge les données en json
    results = json.loads(data.decode())
    offres = results.get("resultats", [])


    #Filtrer les offres si le salaire min est fourni -> on utilise la fonction extraire_salaire de utils.py

    if salaire_min is None:
        return results

    offres_filtrees = []
    seuil = float(salaire_min)
    for offre in offres:
        salaire_obj = offre.get("salaire") or {}
        if not isinstance(salaire_obj, dict):
            salaire_obj = {}
        #on extrait le libelle du salaire
        salaire_libelle = salaire_obj.get("libelle", "") or ""
        salaire_offre = extraire_salaire(salaire_libelle)
        if salaire_offre is not None and salaire_offre >= seuil:
            offres_filtrees.append(offre)

    results["resultats"] = offres_filtrees
    return results









def normaliser_offres(data_json):
    """
    Normalise la réponse France Travail en un format plus simple et stable.
    Ne lève pas d'exception si la structure varie : renvoie des champs à None.
    """
    if not isinstance(data_json, dict):
        return {"offres": [], "total": 0}

    # Propager les erreurs de jobs_ville telles quelles
    if "error" in data_json:
        return data_json

    offres_raw = None
    for key in ("resultats", "results", "offres", "items"):
        if isinstance(data_json.get(key), list):
            offres_raw = data_json[key]
            break

    if offres_raw is None:
        offres_raw = []

    def _get(d, *path):
        cur = d
        for p in path:
            if not isinstance(cur, dict) or p not in cur:
                return None
            cur = cur[p]
        return cur

    offres = []
    for o in offres_raw:
        if not isinstance(o, dict):
            continue
        offres.append(
            {
                "id": o.get("id"),
                "titre": o.get("intitule") or o.get("title"),
                "description": o.get("description"),
                "entreprise": _get(o, "entreprise", "nom") or _get(o, "company", "name"),
                "lieu": _get(o, "lieuTravail", "libelle")
                or _get(o, "lieuTravail", "commune")
                or _get(o, "location", "label"),
                "code_postal": _get(o, "lieuTravail", "codePostal") or _get(o, "location", "postalCode"),
                "type_contrat": o.get("typeContrat") or o.get("contractType"),
                "nature_contrat": o.get("natureContrat"),
                "salaire": _get(o, "salaire", "libelle") or _get(o, "salary", "label"),
                "date_creation": o.get("dateCreation") or o.get("createdAt"),
                "date_actualisation": o.get("dateActualisation") or o.get("updatedAt"),
                "url": _get(o, "origineOffre", "urlOrigine") or _get(o, "applyUrl") or _get(o, "url"),
            }
        )

    total = (
        data_json.get("nombreResultats")
        or data_json.get("total")
        or data_json.get("count")
        or len(offres_raw)
    )

    return {"offres": offres, "total": total}