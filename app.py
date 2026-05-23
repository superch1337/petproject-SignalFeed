import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from services.hackernews import get_top_posts
from services.ai import analyze_post, analyze_trends
from utils.cache import get_cache, set_cache
from authlib.integrations.starlette_client import OAuth
from fastapi import Request
from utils.crud import (
    save_user,
    get_posts_from_db,
    save_trend,
    save_posts,
    get_trends_from_db,
    save_favorite,
    get_favorites,
    delete_favorite,
)
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from authlib.integrations.base_client.errors import OAuthError
from utils.db import engine
from utils.models import Base

Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key",
    same_site="lax",
)


oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

POSTS_TTL = 60 * 60 * 24  # 24 часа


@app.get("/")
def root():
    return {"message": "SignalFeed API работает 🚀"}


@app.get("/posts")
def get_posts():
    # 1. Проверяем кэш — если свежий (< 24ч), отдаём из БД
    cached = get_cache("posts_updated")

    if cached:
        db_posts = get_posts_from_db(10)
        return {"posts": db_posts, "source": "database"}

    # 2. Кэш протух или отсутствует — идём в HN
    try:
        posts = get_top_posts(10)
    except Exception as e:
        # HN недоступен — отдаём старые данные из БД
        db_posts = get_posts_from_db(10)
        if db_posts:
            return {"posts": db_posts, "source": "database_fallback"}
        raise HTTPException(status_code=503, detail=f"Hacker News недоступен: {str(e)}")

    # 3. Сохраняем в БД и обновляем кэш
    save_posts(posts)
    set_cache("posts_updated", True, ttl=POSTS_TTL)

    return {"posts": posts, "source": "api"}


@app.get("/trends")
def get_trends():
    cached = get_cache("trends")

    if cached:
        return {"trends": cached, "cached": True}

    try:
        posts = get_top_posts(10)
        trends = analyze_trends(posts)
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Ошибка получения трендов: {str(e)}"
        )

    save_trend(trends)
    set_cache("trends", trends, ttl=300)

    return {"trends": trends, "cached": False}


@app.get("/analyze")
def analyze(title: str):
    try:
        result = analyze_post(title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")

    return {"title": title, "analysis": result}


@app.get("/history")
def get_history():
    trends = get_trends_from_db(5)
    return {"history": trends}


@app.get("/auth/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8000/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def auth_callback(request: Request):

    try:

        token = await oauth.google.authorize_access_token(request)

        user = token.get("userinfo")

        save_user(user)

        request.session["user"] = {
            "id": user["sub"],
            "email": user["email"],
            "name": user["name"],
            "picture": user["picture"],
        }

    except OAuthError:

        # 🔥 если callback дернули повторно — просто игнорим

        return RedirectResponse(url="http://localhost:5173")

    return RedirectResponse(url="http://localhost:5173")


@app.get("/me")
def get_me(request: Request):
    user = request.session.get("user")

    if not user:
        return {"error": "Не авторизован"}

    return {"user": user}


@app.get("/protected")
def protected(request: Request):
    user = request.session.get("user")

    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован")

    return {"message": f"Привет {user['name']}"}


@app.post("/favorites")
def add_favorite(request: Request, title: str, url: str):
    user = request.session.get("user")

    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован")

    save_favorite(user["id"], title, url)

    return {"message": "Добавлено"}


@app.get("/favorites")
def get_user_favorites(request: Request):
    user = request.session.get("user")

    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован")

    data = get_favorites(user["id"])

    return {"favorites": data}


@app.delete("/favorites")
def remove_favorite(request: Request, url: str):
    user = request.session.get("user")

    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован")

    delete_favorite(user["id"], url)

    return {"message": "Удалено"}


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "ok"}
