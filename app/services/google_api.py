# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false
# pyright: reportPrivateImportUsage=false
"""Сервисные функции для работы с Google API."""

from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
) -> str:
    """Создать документ с таблицами."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт на {now_date_time}',
            'locale': 'ru_RU',
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11,
                },
            },
        }],
    }
    response = await wrapper_services.as_user(
        service.spreadsheets.create(json=spreadsheet_body),
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle,
) -> None:
    """Предоставить права доступа к документу."""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_user(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id',
        ),
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    reservations: list[dict[str, int]],
    wrapper_services: Aiogoogle,
) -> None:
    """Записать данные из БД в гугл-таблицу."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Количество бронирований переговорок'],
        ['ID переговорки', 'Кол-во бронирований'],
    ]
    for res in reservations:
        new_row = [str(res['meetingroom_id']), str(res['count'])]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }
    await wrapper_services.as_user(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body,
        ),
    )
