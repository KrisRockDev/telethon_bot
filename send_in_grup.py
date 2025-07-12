import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import rpcerrorlist
# Для преобразования ID супергрупп/каналов
from telethon.tl.types import PeerChannel, PeerChat

load_dotenv()


# Убедимся, что ID загружаются как строки, а потом преобразуем их в числа
# Это предотвратит ошибки, если в .env файле пустое значение
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
CHAT_ID = os.getenv('CHAT_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
# GRUP_ID = os.getenv('GRUP_ID')
USER_NAME = os.getenv('USER_NAME')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
session_name = os.getenv('SESSION_NAME')
raw_grup_id = os.getenv('GRUP_ID')

if not all([api_id, api_hash, session_name, raw_grup_id]):
    raise ValueError("Пожалуйста, убедитесь, что в файле .env заданы API_ID, API_HASH, SESSION_NAME и GRUP_ID")

# --- ВАЖНО: Преобразуем ID в число ---
try:
    # Telethon ожидает числовой ID
    GRUP_ID = int(raw_grup_id)
    print(f'Используем GRUP_ID: {GRUP_ID}',)
except (ValueError, TypeError):
    raise TypeError("GRUP_ID в .env файле должен быть числом (например, -123456789)")


client = TelegramClient(session_name, int(api_id), api_hash)


async def main():
    try:
        # --- РЕШЕНИЕ: Сначала получаем "сущность" (entity) чата ---
        # Это заставит Telethon найти чат на серверах Telegram и закэшировать его.
        # Этот шаг решает 99% проблем с "Cannot find any entity".
        print(f"Попытка найти сущность для ID: {GRUP_ID}...")
        entity = await client.get_entity(GRUP_ID)
        print("Сущность успешно найдена!")

        # Теперь отправка сообщения сработает без проблем
        msg = await client.send_message(entity, 'Привет, группа! Это сообщение должно дойти.')
        print(f"\nСообщение отправлено в группу с ID={GRUP_ID}.")
        print(f"ID отправленного сообщения: {msg.id}")
        print(msg)

    except rpcerrorlist.PeerIdInvalidError:
        print(f"Ошибка: неверный ID чата ({GRUP_ID}) или у вас нет доступа.")
    except ValueError:
        # Эта ошибка возникает, если get_entity не может найти чат
        print(f"Ошибка: не удалось найти чат с ID {GRUP_ID}. Проверьте, правильный ли ID и являетесь ли вы участником чата.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при отправке сообщений: {e}")

try:
    with client:
        client.loop.run_until_complete(main())
except Exception as e:
    print(f"Произошла критическая ошибка при запуске или работе клиента: {e}")

print("\nРабота клиента завершена.")