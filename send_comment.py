import asyncio
import os
from telethon.tl.types import PeerChannel
from telegram_client import client
from config import GRUP_ID, CHANNEL_ID


async def _find_discussion_post_id(channel_post):
    # Находит ID пересланного из канала сообщения в группе для обсуждений.
    # :param channel_post: Объект сообщения, опубликованного в канале.
    # :return: ID сообщения в группе для комментариев или `None`, если не найдено.

    print("...Идет поиск поста в группе для комментирования...")

    for attempt in range(3):
        try:
            channel_entity = await client.get_entity(CHANNEL_ID)

            async for message in client.iter_messages(GRUP_ID, limit=20):
                if message.fwd_from and \
                        isinstance(message.fwd_from.from_id, PeerChannel) and \
                        message.fwd_from.from_id.channel_id == channel_entity.id and \
                        message.fwd_from.channel_post == channel_post.id:
                    print(f"Найден пост для комментирования. ID в группе: {message.id}")
                    return message.id

            if attempt < 2:
                print(f"Пост не найден. Попытка {attempt + 2}/3 через 5 секунд...")
                await asyncio.sleep(5)

        except Exception as e:
            print(f"Ошибка при поиске поста в группе: {e}")
            return None

    print("Ошибка: Не удалось найти пересланный пост в группе обсуждений.")
    return None


async def add_comment_text(channel_post, text_comment):
    # Добавляет один текстовый комментарий к посту.
    # :param channel_post: Объект сообщения из канала.
    # :param text_comment: Текст комментария.

    print(f"\n--- Добавление текстового комментария (описания) ---")
    discussion_post_id = await _find_discussion_post_id(channel_post)
    if not discussion_post_id:
        return

    try:
        await client.send_message(
            entity=GRUP_ID,
            message=text_comment,
            reply_to=discussion_post_id,
            parse_mode='html'
        )
        print("Текстовый комментарий успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении текстового комментария: {e}")


async def add_comment_photos(channel_post, path_to_images):
    # Добавляет комментарий с одним или несколькими изображениями (в виде альбома).
    # :param channel_post: Объект сообщения из канала.
    # :param path_to_images: Список путей к файлам изображений.

    print(f"\n--- Добавление комментария со скриншотами ---")
    discussion_post_id = await _find_discussion_post_id(channel_post)
    if not discussion_post_id:
        return

    valid_paths = [p for p in path_to_images if os.path.exists(p)]
    if not valid_paths:
        print("Ошибка: Файлы изображений для комментария не найдены.")
        return

    try:
        print(f"Отправка {len(valid_paths)} фото...")
        await client.send_file(
            entity=GRUP_ID,
            file=valid_paths,
            reply_to=discussion_post_id,
            # caption="Скриншоты"
        )
        print("Комментарий со скриншотами успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении комментария с фото: {e}")


async def add_comments_file(channel_post, file_paths):
    """
    Добавляет несколько комментариев, каждый с одним файлом.

    :param channel_post: Объект сообщения из канала.
    :param file_paths: Список путей к файлам.
    """
    print(f"\n--- Добавление комментариев с торрент-файлами ---")
    discussion_post_id = await _find_discussion_post_id(channel_post)
    if not discussion_post_id:
        return

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"Ошибка: Файл не найден по пути {file_path}, пропуск.")
            continue

        try:
            file_name = os.path.basename(file_path)
            print(f"Отправка файла: {file_name}...")
            await client.send_file(
                entity=GRUP_ID,
                file=file_path,
                caption="Размер: " + file_name.split("size.")[1].split("Gb")[0] + "Gb",
                reply_to=discussion_post_id
            )
            print(f"Файл {file_name} успешно отправлен.")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Ошибка при отправке файла {file_path}: {e}")