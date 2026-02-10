from fastapi import FastAPI
from pydantic import BaseModel
import httplib2
import json
from src.fichier import *

 
app = FastAPI()

token = get_token()


@app.get("/")
async def root():
    if not token:
        token = get_token()
        
    return {"message": "Hello World"}

@app.get("/jobs")
async def jobs():
    return {
        "count": 0,
        "jobs": []
    }


