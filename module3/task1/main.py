from fastapi import FastAPI
from models.models import UserCreate

app = FastAPI()
db = []


@app.post("/create_user")
async def create_user(user: UserCreate):
    db.append(user)
    return user


