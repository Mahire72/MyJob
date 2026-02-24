import httplib2
import json
from io import BytesIO


ACCESS_POINT = 'https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire'
Recherche_API = 'https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search'

client_id = "PAR_futurejob_f111ac9cc68d1d5b397eb74df49e7eaf3c647c94228310f2dae8c33d63156b1d"
client_secret = "4fc6f68794bdacef02570a6176625b9de3ce931f2f67081cc7fabd7cb09b8f25"
scope = "api_offresdemploiv2 o2dsoffre"

def get_token():
    header = {'Content-Type' : 'application/x-www-form-urlencoded'}
    body = (
        "grant_type=client_credentials" +
        "&client_id=" + client_id + 
        "&client_secret="+client_secret + 
        "&scope=" +scope
    )
    reponse,data = httplib2.Http().request(ACCESS_POINT, method='POST', headers=header, body=body)

    p = json.loads(data.decode())
    return p["access_token"]
   
def toujours_valide(token):
    headers = {'Authorization' : 'Bearer '+ token, 'Accept' : 'application/json'}
    
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search?motsCles=developpeur"

    reponse,data = httplib2.Http().request(url ,method='GET', headers=headers)
    
    return reponse.status != 400


def jobs_ville(code_postal, token):
    # On a besoin du code INSEE pour faire la requete France Travail
    #Pour faire cela on se sert d'une nouvelle API de opendatasoft (base de donnees des communes)

    url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/correspondance-code-cedex-code-insee/records/?limit=10&offset=0&where=code+%3D+" + str(code_postal)
    reponse, data= httplib2.Http().request(url, method='GET')

    if (reponse.status != 200):
        #Erreur code postale non valide à traiter
        print("Code postal non valide")
    else:
        data_json= json.loads(data)
        code_insee = data_json['results'][0]['insee']

    headers = {'Authorization' : 'Bearer '+ token, 'Accept' : 'application/json'}

    url ="https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search?commune="+ str(code_insee)

    reponse, data= httplib2.Http().request(url, method='GET', headers=headers)

    return data
        
    

    
    
