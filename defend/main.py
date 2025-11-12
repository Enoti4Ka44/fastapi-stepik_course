from fastapi import FastAPI, Request, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from defend.models.models import UserData, Movietop
from datetime import datetime, timedelta
import jwt
import time
import uuid

app = FastAPI()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2  

movies = [
    Movietop(id=i, name=f"Фильм{i}", cost=100000, director="Тим Бертон")
    for i in range(1, 11)
]

users = {
    "test": "qwe",
}

security = HTTPBearer()
sessions = {}  # хранение активных cookie-сессий

# ==========================================================
# TOKEN-BASED АУТЕНТИФИКАЦИЯ
# ==========================================================

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


# ==========================================================
# COOKIE-BASED АУТЕНТИФИКАЦИЯ
# ==========================================================

@app.get("/login_cookie", response_class=HTMLResponse)
def login_cookie_page():
    return FileResponse("defend/templates/login_cookie.html")

@app.get("/login_cookie.js")
def login_cookie_js():
    return FileResponse("defend/templates/login_cookie.js")


@app.post("/login_cookie")
async def login_cookie(data: UserData, response: Response):
    username = data.username
    password = data.password

    if username in users and users[username] == password:
        session_token = str(uuid.uuid4())
        expire_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        sessions[session_token] = {
            "username": username,
            "expires": expire_time,
            "login_time": datetime.now()
        }

        # Устанавливаем куки
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=False,  # можно True, если https
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        return {"message": "Вход выполнен успешно"}
    raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")


# ==========================================================
# USER PAGE (общая, и для токенов, и для куки)
# ==========================================================

@app.get("/user", response_class=HTMLResponse)
def user_page():
    return FileResponse("defend/templates/user.html")

@app.get("/user.js")
def user_js():
    return FileResponse("defend/templates/user.js")

@app.get("/user_cookie", response_class=HTMLResponse)
def user_cookie_page():
    return FileResponse("defend/templates/user_cookie.html")

@app.get("/user_cookie.js")
def user_cookie_js():
    return FileResponse("defend/templates/user_cookie.js")


# ==========================================================
# USER DATA через JWT
# ==========================================================

@app.get("/user_data")
async def user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt(token)
    return {
        "username": payload["username"],
        "movies": [m.model_dump() for m in movies]
    }


# ==========================================================
# USER DATA через COOKIE
# ==========================================================

@app.get("/user_data_cookie")
async def user_info_cookie(request: Request):
    session_token = request.cookies.get("session_token")

    if not session_token or session_token not in sessions:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    session_data = sessions[session_token]

    # Проверяем срок действия
    if datetime.now() > session_data["expires"]:
        del sessions[session_token]
        return JSONResponse(status_code=401, content={"message": "Session expired"})

    # Обновляем срок действия (продлеваем на 2 минуты)
    session_data["expires"] = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "username": session_data["username"],
        "login_time": session_data["login_time"].strftime("%Y-%m-%d %H:%M:%S"),
        "session_expires": session_data["expires"].strftime("%Y-%m-%d %H:%M:%S"),
        "movies": [m.model_dump() for m in movies]
    }


# ==========================================================
# ДРУГИЕ ЭНДПОЙНТЫ
# ==========================================================

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

@app.post("/add_film_cookie")
async def add_film_cookie(movie: Movietop, request: Request):
    session_token = request.cookies.get("session_token")

    if not session_token or session_token not in sessions:
        return JSONResponse(status_code=401, content={"detail": "Пожалуйста, войдите в аккаунт"})

    session_data = sessions[session_token]

    if datetime.now() > session_data["expires"]:
        del sessions[session_token]
        return JSONResponse(status_code=401, content={"detail": "Сессия истекла, войдите снова"})

    # создаём id фильма
    if movie.id is None:
        movie.id = max([m.id for m in movies], default=0) + 1

    movies.append(movie)

    return {"message": f"Фильм '{movie.name}' добавлен пользователем {session_data['username']}"}
