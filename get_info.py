import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import rpcerrorlist  # Импортируем для более точной обработки ошибок

# Загружаем переменные окружения из файла .env
load_dotenv()

# Считываем значения из .env.
# Не забудьте использовать ваши собственные значения с my.telegram.org!
# https://docs.telethon.dev/en/stable/basic/quick-start.html

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
CHAT_ID = os.getenv('CHAT_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
GRUP_ID = os.getenv('GRUP_ID')
USER_NAME = os.getenv('USER_NAME')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
session_name = os.getenv('SESSION_NAME')

# Проверяем, что все переменные окружения были загружены
if not all([api_id, api_hash, session_name]):
    raise ValueError("Пожалуйста, убедитесь, что в файле .env заданы API_ID, API_HASH и SESSION_NAME")

# Создаем клиент Telegram
# Файл сессии (session_name.session) будет создан для хранения авторизации
client = TelegramClient(session_name, int(api_id), api_hash)


async def main():
    # --- Блок получения информации о себе ---
    try:
        # Получение информации о себе
        me = await client.get_me()

        # "me" - это объект пользователя. Вы можете красиво распечатать
        # любой объект Telegram с помощью метода "stringify":
        # print("--- Информация о пользователе ---")
        # print(me.stringify())

        # Когда вы что-то печатаете, вы видите его представление.
        # Вы можете получить доступ ко всем атрибутам объектов Telegram
        # с помощью точечной нотации. Например, чтобы получить имя пользователя:
        username = me.username
        print(f"Имя пользователя: {username}")
        print(f"Номер телефона: {me.phone}")
        print("-" * 20)

    except Exception as e:
        print(f"Произошла ошибка при получении информации о себе: {e}")

    # --- Блок перебора диалогов ---
    try:
        # Вы можете вывести все диалоги/чаты, в которых вы состоите:
        print("\n--- Список диалогов ---")
        async for dialog in client.iter_dialogs():
            print(f'"{dialog.name}" имеет ID: {dialog.id}')
        print("-" * 20)
    except Exception as e:
        print(f"Произошла ошибка при получении списка диалогов: {e}")

# Контекстный менеджер 'with client:' автоматически выполняет client.start()
# при входе и client.disconnect() при выходе из блока.
try:
    with client:
        # Запускаем асинхронную функцию main в цикле событий клиента
        client.loop.run_until_complete(main())
except Exception as e:
    print(f"Произошла критическая ошибка при запуске или работе клиента: {e}")

print("\nРабота клиента завершена.")