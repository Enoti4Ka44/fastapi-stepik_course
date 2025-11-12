from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, HTMLResponse
from defend.models.models import UserData, Movietop
import jwt
import time

app = FastAPI()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2

movies = [
    Movietop(id=i, name=f"Фильм{i}", cost=100000, director="Тим Бертон") for i in range(1, 11)
]

users = {
    "test": "qwe",
}

security = HTTPBearer()

#token
def create_jwt(username: str):
    payload = {"username": username, "exp": time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

#login endponits
@app.get("/login", response_class=HTMLResponse)
def login_page():
    return FileResponse("defend/templates/login.html")

@app.get("/login.js")
def login_js():
    return FileResponse("defend/templates/login.js")

@app.post("/login")
async def login(data: UserData):
    username = data.username
    password = data.password

    if username in users and users[username] == password:
        token = create_jwt(username)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")

#user endpoints
@app.get("/user.js")
def user_js():
    return FileResponse("defend/templates/user.js")

@app.get("/user", response_class=HTMLResponse)
def user_page():
    return FileResponse("defend/templates/user.html")

@app.get("/user_data")
async def user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt(token)
    return {
        "username": payload["username"],
        "movies": [m.model_dump() for m in movies]
    }

#other endpoints
@app.get('/')
def root():
    return FileResponse("defend/index.html")

@app.get("/movietop/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Фильм не найден")

@app.post("/add_film")
async def add_film(movie: Movietop, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt(token)

    if movie.id is None:
        movie.id = max([m.id for m in movies], default=0) + 1

    movies.append(movie)
    return {"message": f"Фильм '{movie.name}' добавлен пользователем {payload['username']}"}


