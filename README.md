# OfficeNomad

API для бронирования переговорных комнат.

## Tech Stack

- [Python 3.12](https://www.python.org/)
- [FastAPI 0.115.5](https://fastapi.tiangolo.com/)
- [Pydantic Settings 2.6.1](https://docs.pydantic.dev/latest/)
- [SQLAlchemy 2.0 (async)](https://docs.sqlalchemy.org/)
- [FastAPI Users 13.0.0](https://fastapi-users.github.io/fastapi-users/)
- [aiogoogle 5.13.0](https://aiogoogle.readthedocs.io/) (Google Sheets/Drive API)
- [Alembic 1.13.1](https://alembic.sqlalchemy.org/)

## Локальное развертывание

```bash
git clone <repository-url>
cd room_reservation/apps/room_reservation
```

```bash
uv venv
source .venv/bin/activate
uv sync
```

```bash
cp .env.example .env
# Отредактировать .env при необходимости
```

```bash
uv run alembic upgrade head
uvicorn app.main:app --reload
```

API документация: http://127.0.0.1:8000/docs

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DATABASE_URL` | Строка подключения к БД | `sqlite+aiosqlite:///./room_reservation.db` |
| `SECRET` | Ключ для JWT токенов | — |
| `FIRST_SUPERUSER_EMAIL` | Email суперпользователя | — |
| `FIRST_SUPERUSER_PASSWORD` | Пароль суперпользователя | — |
| `EMAIL` | Email для расшаривания Google Sheets | — |
