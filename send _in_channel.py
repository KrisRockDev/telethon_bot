import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import rpcerrorlist

load_dotenv()

# --- 1. Загружаем все необходимые переменные ---
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_name = os.getenv('SESSION_NAME')

# Загружаем ID и для канала, и для группы
raw_channel_id = os.getenv('CHANNEL_ID')
raw_grup_id = os.getenv('GRUP_ID')  # Группа для обсуждений

if not all([api_id, api_hash, session_name, raw_channel_id, raw_grup_id]):
    raise ValueError(
        "Пожалуйста, убедитесь, что в файле .env заданы API_ID, API_HASH, SESSION_NAME, CHANNEL_ID и GRUP_ID")

# --- 2. Преобразуем ID в числа (важный шаг) ---
try:
    CHANNEL_ID = int(raw_channel_id)
    GRUP_ID = int(raw_grup_id)
    print(f'Используем CHANNEL_ID: {CHANNEL_ID}')
    print(f'Используем GRUP_ID (для комментариев): {GRUP_ID}')
except (ValueError, TypeError):
    raise TypeError("CHANNEL_ID и GRUP_ID в .env файле должны быть числами (например, -100123456789)")

# Создаем клиент
client = TelegramClient(session_name, int(api_id), api_hash)


async def main():
    try:
        # --- 3. Получаем "сущность" (entity) для канала ---
        # Для группы это делать не обязательно, т.к. мы будем отвечать на пост из канала,
        # но для надежности можно получить и ее.
        print(f"\nПопытка найти сущность для канала ID: {CHANNEL_ID}...")
        channel_entity = await client.get_entity(CHANNEL_ID)
        print("Сущность канала успешно найдена!")

        # --- 4. Отправляем основной пост в канал ---
        print("\nОтправка основного поста в канал...")
        channel_post = await client.send_message(
            entity=channel_entity,
            message='Это мой основной пост в канале! Сейчас я оставлю к нему комментарий.'
        )
        print(f"Пост успешно отправлен в канал. ID сообщения: {channel_post.id}")

        # Небольшая пауза для наглядности
        await asyncio.sleep(0.1)

        # --- 5. КЛЮЧЕВОЙ МОМЕНТ: Отправляем комментарий ---
        # Мы отправляем сообщение в группу обсуждений, указывая,
        # на какое сообщение из канала нужно ответить.
        print("\nОтправка комментария к посту...")
        comment = await client.send_message(
            entity=GRUP_ID,  # Отправляем именно в группу
            message='А это мой первый комментарий под постом!',
            reply_to=channel_post.id  # Указываем ID поста в канале
        )
        print(f"Комментарий успешно отправлен! ID комментария: {comment.id}")


    except rpcerrorlist.PeerIdInvalidError:
        print(f"Ошибка: неверный ID канала ({CHANNEL_ID}) или группы ({GRUP_ID}), либо у вас нет к ним доступа.")
    except ValueError as e:
        print(f"Ошибка: не удалось найти чат. Проверьте правильность ID. {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


# Запускаем клиент
try:
    with client:
        client.loop.run_until_complete(main())
except Exception as e:
    print(f"Произошла критическая ошибка при запуске или работе клиента: {e}")

print("\nРабота клиента завершена.")