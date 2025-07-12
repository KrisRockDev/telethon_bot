import asyncio
import os
from telegram_client import client
from file_parser import get_info
from send_post import add_post
from send_comment import add_comment_text, add_comment_photos, add_comments_file

async def main():
    # Основная функция, координирующая процесс публикации.

    # 1. Получаем информацию о файлах для публикации
    film_data = get_info(base_dir="downloads")

    if not film_data:
        print("\nНе удалось получить данные для публикации. Работа скрипта остановлена.")
        return

    # 2. Публикуем основной пост (название + info.txt) с постером
    post_object = await add_post(
        text_content=film_data["post_text"],
        image_path=film_data["poster"],
        info_file=film_data["info_file"]
    )

    if not post_object:
        print("\nПубликация поста не удалась. Комментарии не будут добавлены.")
        return

    # 3. Добавляем комментарии к созданному посту

    # Добавляем текстовый комментарий из файла описания (des.txt)
    if film_data["description_file"] and os.path.exists(film_data["description_file"]):
        try:
            with open(film_data["description_file"], 'r', encoding='utf-8') as file:
                description_text = file.read()
            await add_comment_text(post_object, description_text)
        except Exception as e:
            print(f"\nОшибка чтения файла описания (des.txt) для комментария: {e}")
    else:
        print("\nФайл описания (des.txt) для комментария не найден.")

    # Добавляем комментарий со скриншотами
    if film_data["screenshots"]:
        await add_comment_photos(post_object, film_data["screenshots"])
    else:
        print("\nСкриншоты для комментария не найдены.")

    # Добавляем комментарии с торрент-файлами
    if film_data["torrents"]:
        await add_comments_file(post_object, film_data["torrents"])
    else:
        print("\nТоррент-файлы для комментариев не найдены.")


if __name__ == "__main__":
    print("Запуск клиента...")
    try:
        with client:
            client.loop.run_until_complete(main())
    except Exception as e:
        print(f"Произошла критическая ошибка при работе клиента: {e}")

    print("\nРабота клиента завершена.")