from telegram_client import client
from config import CHANNEL_ID
import os


async def add_post(text_content, image_path=None):
    """
    Публикует пост в канале. Может содержать текст и одно изображение.

    :param text_content: Текстовое содержимое поста.
    :param image_path: (опционально) Путь к изображению.
    :return: Объект сообщения (`channel_post`) в случае успеха, иначе `None`.
    """
    print("--- Публикация поста ---")
    if image_path and not os.path.exists(image_path):
        print(f"Ошибка: Изображение не найдено по пути {image_path}")
        return None

    try:
        channel_entity = await client.get_entity(CHANNEL_ID)

        print("Отправка поста в канал...")
        channel_post = await client.send_message(
            entity=channel_entity,
            message=text_content,
            file=image_path if image_path else None
        )
        print(f"Пост успешно отправлен. ID сообщения: {channel_post.id}")
        return channel_post

    except Exception as e:
        print(f"Произошла ошибка при отправке поста: {e}")
        return None