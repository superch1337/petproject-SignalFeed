# SignalFeed 🚀

SignalFeed — это AI-powered агрегатор новостей на основе Hacker News.

Проект собирает популярные статьи, анализирует их с помощью ИИ, показывает тренды и позволяет сохранять интересные материалы в избранное через Google-аккаунт.

## Возможности

- 🔐 Авторизация через Google OAuth
- 📰 Получение топовых новостей из Hacker News
- 🤖 AI-анализ статей
- 📈 Определение трендов
- ⭐ Система избранного
- 🗄️ SQLAlchemy ORM
- 💾 SQLite база данных
- ⚡ FastAPI backend
- 🎨 React frontend

---

## Технологии

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Authlib (Google OAuth)
- OpenAI API

### Frontend

- React
- Axios
- Vite

---

## Установка

### Клонирование репозитория

```bash
git clone https://github.com/superch1337/petproject-SignalFeed.git
cd petproject-SignalFeed
```

### Backend

Создать виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Создать файл `.env`:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
OPENAI_API_KEY=your_openai_api_key
```

Запуск сервера:

```bash
uvicorn app:app --reload
```

---

### Frontend

Перейти в папку фронтенда:

```bash
cd frontend
```

Установить зависимости:

```bash
npm install
```

Запустить приложение:

```bash
npm run dev
```

---

## Структура проекта

```text
utils/
├── crud.py
├── db.py
├── models.py
├── cache.py

services/
├── ai.py
├── hackernews.py

frontend/
├── src/
│   ├── App.jsx
│   └── api.js

app.py
```

---

## Скриншоты

позже добавлю ! 

---

## Автор

GitHub: https://github.com/superch1337