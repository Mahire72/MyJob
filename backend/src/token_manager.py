import requests
import time

CLIENT_ID = " "
CLIENT_SECRET = " "

token = None
token_expire = 0

def get_token()
    global tokenglobal token_expire

    #toke hala gecerliyse tekrar alma
    if token and time.time() < token_expire:
        return token

    url = "POST https://entreprise.francetravail.fr/connexion/oauth2/access_token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }

    reponse = requests.post(url, data=data).json()

    token = reponse["access_token"]

    #token suresi
    token_expire = time.time()+ response["expires_in"]
    return token
