from .db import SessionLocal
from .models import User, Favorite, Post, Trend


# =========================
# USERS
# =========================

def save_user(user):
    db = SessionLocal()

    exists = (
        db.query(User)
        .filter(User.google_id == user["sub"])
        .first()
    )

    if not exists:
        new_user = User(
            google_id=user["sub"],
            email=user["email"],
            name=user["name"],
            picture=user["picture"]
        )

        db.add(new_user)
        db.commit()

    db.close()


# =========================
# POSTS
# =========================

def save_posts(posts):
    db = SessionLocal()

    for p in posts:

        exists = (
            db.query(Post)
            .filter(Post.title == p["title"])
            .first()
        )

        if not exists:
            post = Post(
                title=p["title"],
                author=p["author"],
                score=p["score"],
                url=p["url"],
                comments=p["comments"]
            )

            db.add(post)

    db.commit()
    db.close()


def get_posts_from_db(limit=10):
    db = SessionLocal()

    posts = (
        db.query(Post)
        .order_by(Post.id.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return [
        {
            "title": p.title,
            "author": p.author,
            "score": p.score,
            "url": p.url,
            "comments": p.comments
        }
        for p in posts
    ]


# =========================
# TRENDS
# =========================

def save_trend(trend_text):
    db = SessionLocal()

    trend = Trend(
        content=trend_text
    )

    db.add(trend)
    db.commit()

    db.close()


def get_trends_from_db(limit=5):
    db = SessionLocal()

    trends = (
        db.query(Trend)
        .order_by(Trend.id.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return [
        {
            "content": t.content,
            "created_at": str(t.created_at)
        }
        for t in trends
    ]


# =========================
# FAVORITES
# =========================

def save_favorite(user_id, title, url):
    db = SessionLocal()

    exists = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == user_id,
            Favorite.url == url
        )
        .first()
    )

    if not exists:
        favorite = Favorite(
            user_id=user_id,
            title=title,
            url=url
        )

        db.add(favorite)
        db.commit()

    db.close()


def get_favorites(user_id):
    db = SessionLocal()

    favorites = (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id)
        .order_by(Favorite.id.desc())
        .all()
    )

    db.close()

    return [
        {
            "title": f.title,
            "url": f.url,
            "created_at": str(f.created_at)
        }
        for f in favorites
    ]


def delete_favorite(user_id, url):
    db = SessionLocal()

    (
        db.query(Favorite)
        .filter(
            Favorite.user_id == user_id,
            Favorite.url == url
        )
        .delete()
    )

    db.commit()
    db.close()