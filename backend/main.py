from fastapi import FastAPI
from pydantic import BaseModel
import httplib2
import json
from src import requete_api

 
app = FastAPI()

token = requete_api.get_token()


@app.get("/")
async def root():
    if requete_api.toujours_valide(token) == False{
        token = get_token()
    }
        
    return {"message": "Hello World"}

@app.get("/jobs")
async def jobs():
    return {
        "count": 0,
        "jobs": []
    }


