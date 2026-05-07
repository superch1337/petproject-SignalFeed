import os
import sqlite3

DB_NAME = os.path.join(os.path.dirname(__file__), "..", "database.db")


def get_connection():
    return sqlite3.connect(DB_NAME)


# 🚀 ИНИЦИАЛИЗАЦИЯ БД
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # POSTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        score INTEGER,
        url TEXT,
        comments INTEGER
    )
    """)

    # TRENDS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # CACHE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cache (
        key TEXT PRIMARY KEY,
        value TEXT,
        expires REAL
    )
    """)

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT UNIQUE,
        email TEXT,
        name TEXT,
        picture TEXT
    )
    """)

    # FAVORITES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        title TEXT,
        url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, url)
    )
    """)

    conn.commit()
    conn.close()


# 📥 СОХРАНЕНИЕ ПОСТОВ
def save_posts(posts):
    conn = get_connection()
    cursor = conn.cursor()

    for p in posts:
        cursor.execute("SELECT COUNT(*) FROM posts WHERE title = ?", (p["title"],))
        exists = cursor.fetchone()[0]

        if not exists:
            cursor.execute("""
            INSERT INTO posts (title, author, score, url, comments)
            VALUES (?, ?, ?, ?, ?)
            """, (p["title"], p["author"], p["score"], p["url"], p["comments"]))

    conn.commit()
    conn.close()


# 📥 СОХРАНЕНИЕ ТРЕНДА
def save_trend(trend_text):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO trends (content)
    VALUES (?)
    """, (trend_text,))

    conn.commit()
    conn.close()


# 📥 СОХРАНЕНИЕ ПОЛЬЗОВАТЕЛЯ
def save_user(user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (google_id, email, name, picture)
    VALUES (?, ?, ?, ?)
    """, (
        user["sub"],
        user["email"],
        user["name"],
        user["picture"]
    ))

    conn.commit()
    conn.close()


# ❤️ ДОБАВИТЬ В ИЗБРАННОЕ
def save_favorite(user_id, title, url):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO favorites (user_id, title, url)
    VALUES (?, ?, ?)
    """, (user_id, title, url))

    conn.commit()
    conn.close()


# 📦 ПОЛУЧИТЬ ИЗБРАННОЕ
def get_favorites(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, url, created_at
    FROM favorites
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"title": r[0], "url": r[1], "created_at": r[2]}
        for r in rows
    ]


# ❌ УДАЛИТЬ ИЗ ИЗБРАННОГО
def delete_favorite(user_id, url):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM favorites
    WHERE user_id = ? AND url = ?
    """, (user_id, url))

    conn.commit()
    conn.close()


# 📤 ПОЛУЧИТЬ ПОСТЫ
def get_posts_from_db(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT title, author, score, url, comments
    FROM posts
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"title": r[0], "author": r[1], "score": r[2], "url": r[3], "comments": r[4]}
        for r in rows
    ]


# 📤 ПОЛУЧИТЬ ТРЕНДЫ
def get_trends_from_db(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT content, created_at
    FROM trends
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {"content": r[0], "created_at": r[1]}
        for r in rows
    ]