"""Конфигурация приложения через переменные окружения."""

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения загружаемые из .env файла."""

    app_title: str = 'Бронирование переговорок'
    description: str = 'API для бронирования переговорных комнат'
    database_url: str = 'sqlite+aiosqlite:///./room_reservation.db'
    secret: str = 'SECRET'
    first_superuser_email: EmailStr | None = None
    first_superuser_password: str | None = None

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
