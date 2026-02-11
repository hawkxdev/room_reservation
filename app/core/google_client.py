"""Настройка клиента Google API через aiogoogle (OAuth2)."""

import json
from collections.abc import AsyncGenerator
from pathlib import Path

from aiogoogle import Aiogoogle  # pyright: ignore[reportPrivateImportUsage]
from aiogoogle.auth.creds import ClientCreds, UserCreds

# Monkey-patch: Google OAuth2 возвращает refresh_token_expires_in,
# которое aiogoogle 5.13.0 не поддерживает.
_original_init = UserCreds.__init__


def _patched_init(
    self: UserCreds, *args: object, **kwargs: object,
) -> None:
    kwargs.pop('refresh_token_expires_in', None)
    _original_init(self, *args, **kwargs)


UserCreds.__init__ = _patched_init  # type: ignore[method-assign]

from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

TOKEN_FILE = BASE_DIR / 'token.json'
OAUTH_CLIENT_FILE = BASE_DIR / 'oauth_client.json'


def _load_user_creds() -> UserCreds:
    """Загрузка OAuth2 токенов из token.json."""
    token_data = json.loads(TOKEN_FILE.read_text())
    return UserCreds(
        access_token=token_data['token'],
        refresh_token=token_data['refresh_token'],
        token_uri=token_data['token_uri'],
        scopes=token_data['scopes'],
        expires_at=token_data.get('expiry', '').replace('Z', ''),
    )


def _load_client_creds() -> ClientCreds:
    """Загрузка client_id/secret из oauth_client.json."""
    oauth_data = json.loads(OAUTH_CLIENT_FILE.read_text())
    installed = oauth_data['installed']
    return ClientCreds(
        client_id=installed['client_id'],
        client_secret=installed['client_secret'],
        scopes=SCOPES,
    )


user_creds = _load_user_creds()
client_creds = _load_client_creds()


async def get_service() -> AsyncGenerator[Aiogoogle, None]:
    """Асинхронный генератор для получения экземпляра Aiogoogle."""
    async with Aiogoogle(
        user_creds=user_creds,
        client_creds=client_creds,
    ) as aiogoogle:
        yield aiogoogle
