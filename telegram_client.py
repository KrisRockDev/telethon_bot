from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME

# Создаем и экспортируем единый экземпляр клиента Telegram.
# Это позволяет избежать многократного создания подключения в разных модулях.
# Клиент будет запущен и остановлен в основном файле `main_sender.py`.
client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)