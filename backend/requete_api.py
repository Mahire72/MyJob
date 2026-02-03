import httplib2
import json
from io import BytesIO

ACCES_POINT = 'https://entreprise.francetravail.fr/connexion/oauth2/access_token'
Recherche_API = 'https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search'

client_id = "PAR_futurejob_f111ac9cc68d1d5b397eb74df49e7eaf3c647c94228310f2dae8c33d63156b1d"
client_secret = "4fc6f68794bdacef02570a6176625b9de3ce931f2f67081cc7fabd7cb09b8f25"
scope = "api_offresdemploiv2 o2dsoffre"


def get_access_token():
    header = {'Content-Type' : 'application/x-www-form-urlencoded'}
    body = (
        "grant_type=client_credentials "
        "&client_id=" + client_id + 
        "&client_secret="+client_secret + 
        "&scope=" +scope
    )
    print(body)
    reponse,data = httplib2.Http().request(ACCES_POINT, method='POST' ,headers=header, body=body)
    print(reponse)
   

print(get_access_token())

