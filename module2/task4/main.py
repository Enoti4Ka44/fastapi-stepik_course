from fastapi import FastAPI
from models.models import User

user = User(name='John Doe', id=1)
app = FastAPI()

@app.get("/users", response_model=User)
def user_root():
    return user
