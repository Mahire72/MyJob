import httplib2
import json
import os

import certifi
from dotenv import load_dotenv


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
def _http() -> httplib2.Http:
    if _disable_ssl_validation:
        return httplib2.Http(disable_ssl_certificate_validation=True)
    return httplib2.Http(ca_certs=certifi.where())

# Fonction pour vérifier si les variables d'environnement sont présentes
def _require_secrets() -> None:
    if not client_id or not client_secret:
        raise RuntimeError(
            "Faltan FRANCE_TRAVAIL_CLIENT_ID / FRANCE_TRAVAIL_CLIENT_SECRET en el entorno (.env)."
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


def jobs_ville(code_postal, token):
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

    data_json = json.loads(data.decode())
    if "results" not in data_json or len(data_json["results"]) == 0:
        return {"error": "Aucun code INSEE trouvé pour ce code postal"}

    code_insee = data_json["results"][0]["insee"]
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
    }
    url = (
        "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search?commune="
        + str(code_insee)
    )

    reponse, data = _http().request(url, method="GET", headers=headers)
    if not (200 <= reponse.status < 300):
        return {"error": "Erreur lors de la récupération des offres", "status": reponse.status}

    return json.loads(data.decode())


if __name__ == "__main__":
    
    print(jobs_ville("75001", get_token()))