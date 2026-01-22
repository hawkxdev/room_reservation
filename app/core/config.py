"""Конфигурация приложения через переменные окружения."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения, загружаемые из .env файла."""

    app_title: str = 'Бронирование переговорок'
    description: str = 'API для бронирования переговорных комнат'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
