import os
from telegram_client import client
from config import CHANNEL_ID

async def add_post(text_content, image_path=None, info_file=None):
    # Публикует пост в канале. Объединяет основной текст (название) с информацией из info_file.

    # :param text_content: Основной текст (название фильма).
    # :param image_path: (опционально) Путь к изображению (постеру).
    # :param info_file: (опционально) Путь к файлу с детальной информацией (info.txt).
    # :return: Объект сообщения (`channel_post`) в случае успеха, иначе `None`.

    print("--- Публикация поста ---")

    # Формируем итоговый текст для поста, делая название жирным
    final_post_text = f"<b>{text_content}</b>"

    # Добавляем содержимое info.txt, если файл найден
    if info_file and os.path.exists(info_file):
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                info_content = f.read()
            final_post_text += f"\n\n{info_content}"
            print(f"Информация для поста загружена из файла: {info_file}")
        except Exception as e:
            print(f"Ошибка чтения файла info.txt {info_file}: {e}. Будет использовано только название.")

    if image_path and not os.path.exists(image_path):
        print(f"Ошибка: Изображение не найдено по пути {image_path}. Пост будет без картинки.")
        image_path = None

    try:
        channel_entity = await client.get_entity(CHANNEL_ID)

        print("Отправка поста в канал...")
        channel_post = await client.send_message(
            entity=channel_entity,
            message=final_post_text,
            file=image_path,
            parse_mode='html'
        )
        print(f"Пост успешно отправлен. ID сообщения: {channel_post.id}")
        return channel_post

    except Exception as e:
        print(f"Произошла ошибка при отправке поста: {e}")
        return None