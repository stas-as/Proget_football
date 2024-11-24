import requests as req
from bs4 import BeautifulSoup

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from datetime import datetime
import pandas as pd
import uvicorn
from fastapi import *

proxy_apikey = "a464304279-a8efee8e2f-5356392617"
proxy_url = "https://proxy6.net/api/{api_key}/{method}/?{params}"

app = FastAPI()
response = req.get("https://proxy6.net/api/{api_key}/{getproxy}/?{params}")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

# uvicorn main:app --reload