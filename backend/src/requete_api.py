# France travail API calls

import requests

def search_jobs(token, keyword):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search" #endpoint serach job 
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "motsCles": keyword,
        "lieux": city
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()