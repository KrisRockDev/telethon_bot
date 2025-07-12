# Не забудьте использовать ваши собственные значения с my.telegram.org!
# https://docs.telethon.dev/en/stable/basic/quick-start.html

import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

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
    try:
        # path_file = r'e:\Downloads\Создание_интерактивных_презентаций_с_ИИ_.mp4'
        # path_file = r'e:\Снимок экрана 2025-06-12 200647.png'
        path_file = r'e:\Downloads\Research_book_small_FREE.pdf'
        await client.send_file(USER_NAME, path_file)
    except FileNotFoundError:
        print("Ошибка: Файл для отправки не найден. Проверьте путь.")
    except Exception as e:
        print(f"Произошла ошибка при отправке файла: {e}")

# Контекстный менеджер 'with client:' автоматически выполняет client.start()
# при входе и client.disconnect() при выходе из блока.
try:
    with client:
        # Запускаем асинхронную функцию main в цикле событий клиента
        client.loop.run_until_complete(main())
except Exception as e:
    print(f"Произошла критическая ошибка при запуске или работе клиента: {e}")

print("\nРабота клиента завершена.")