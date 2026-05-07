import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")


def analyze_post(title: str):
    if not API_KEY:
        return "❌ Нет API ключа (проверь .env)"

    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    prompt = f"""
Ты аналитик технологий.

Ответь кратко:
1. О чем это
2. Категория
3. Почему это важно

Заголовок: {title}
"""

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"❌ Ошибка API: {response.text}"

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Ошибка: {str(e)}"


# 🔥 ВОТ ЭТО ДОБАВЬ НИЖЕ
def analyze_trends(posts):
    if not API_KEY:
        return "❌ Нет API ключа"

    titles = "\n".join([f"- {p['title']}" for p in posts])

    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    prompt = f"""
Ты аналитик технологий.

Вот список заголовков:

{titles}

Сделай:
1. Главные темы (3-5)
2. Основные тренды
3. Что сейчас происходит
4. Идеи стартапов

Кратко и по делу.
"""

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"❌ Ошибка API: {response.text}"

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Ошибка: {str(e)}"
