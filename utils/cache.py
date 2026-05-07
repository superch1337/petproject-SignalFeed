import time
import json
from utils.db import get_connection


def set_cache(key, value, ttl=300):
    expires = time.time() + ttl
    value_json = json.dumps(value, ensure_ascii=False)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO cache (key, value, expires)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value, expires = excluded.expires
    """,
        (key, value_json, expires),
    )
    conn.commit()
    conn.close()


def get_cache(key):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value, expires FROM cache WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    value, expires = row

    if time.time() > expires:
        delete_cache(key)
        return None

    return json.loads(value)


def delete_cache(key):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
    conn.commit()
    conn.close()
