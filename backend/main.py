from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    id: int
    userId: int
    title: str
    body: str

@app.get("/posts")
def get_posts():
    try:
        res = requests.get(API_URL)
        return [Post(**post) for post in res.json()]
    except Exception:
        return []
