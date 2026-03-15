from fastapi import FastAPI
from src.token_manager import get_token
from src.requete_api import search_jobs

app = FastAPI()

@app.get("/jobs")
def jobs(keyword: str, city: str = ""):

    token = get_token()

    return search_jobs(token, keyword, city)