import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import rpcerrorlist
from telethon.tl.types import PeerChannel

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

        # --- 5. ИСПРАВЛЕНИЕ: Находим пост в группе обсуждений ---
        # Чтобы оставить комментарий именно к новому посту, нужно сначала дождаться,
        # когда Телеграм автоматически перешлет его из канала в связанную группу.
        # Затем мы находим это пересланное сообщение в группе и отвечаем уже на него.
        print("\nОжидание пересылки поста в группу для комментариев (5 секунд)...")
        await asyncio.sleep(5)

        discussion_post_id = None
        # Ищем в последних сообщениях группы нужное нам
        async for message in client.iter_messages(GRUP_ID, limit=10):
            # Проверяем, является ли сообщение пересланным из нашего канала
            # и совпадает ли ID оригинального поста
            if message.fwd_from and \
                    isinstance(message.fwd_from.from_id, PeerChannel) and \
                    message.fwd_from.from_id.channel_id == channel_entity.id and \
                    message.fwd_from.channel_post == channel_post.id:
                discussion_post_id = message.id  # Нам нужен ID этого сообщения в ГРУППЕ
                print(f"Найден соответствующий пост в группе. ID в группе: {discussion_post_id}")
                break

        # --- 6. Отправляем комментарий, если пост найден ---
        if discussion_post_id:
            print("\nОтправка комментария к посту...")
            comment = await client.send_message(
                entity=GRUP_ID,  # Отправляем именно в группу
                message='А это мой первый комментарий под постом!',
                reply_to=discussion_post_id  # Указываем ID поста в ГРУППЕ
            )
            print(f"Комментарий успешно отправлен! ID комментария: {comment.id}")
        else:
            print("\nОШИБКА: Не удалось найти пересланный пост в группе обсуждений.")
            print(
                "Комментарий не был отправлен. Увеличьте время ожидания в 'asyncio.sleep()' или проверьте связь канала и группы.")


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