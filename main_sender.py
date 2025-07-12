import asyncio
import os

from telegram_client import client
from send_post import add_post
from send_comment import (
    add_comments_text,
    add_comment_photos,
    add_comments_file
)

def get_info():
    dir = "downloads"
    lst = os.listdir(dir)
    if lst != []:
        print("Список файлов в текущей директории:")
        for item in lst:
            print('\t', item)
            film_dir = os.path.join(dir, item)
            ls = os.listdir(film_dir)
            for i in ls:
                print('\t\t', i)
    return film_dir

async def main():
    """
    Основная функция, координирующая процесс публикации.
    """
    # --- 1. Публикация поста с картинкой и текстом ---
    # Укажите свои пути и текст
    dir_film = get_info()
    image_path = os.path.join(dir_film, "poster.jpg")  # Замените на реальный путь к картинке
    text_content = dir_film

    # Публикуем пост и получаем его объект
    # post_object = await add_post(text_content, image_path)
    # Если нужен пост только с текстом:
    post_object = await add_post(text_content, image_path)

    # Если пост не был опубликован, выходим
    if not post_object:
        print("\nПубликация не удалась. Работа скрипта остановлена.")
        return

    # --- 2. Добавление комментариев к созданному посту ---

    # Добавление комментария с текстом
    print(f'{post_object=}')
    text_comment = "Отличный пост! Спасибо, что поделились!"
    await add_comments_text(post_object, text_comment)

    # Добавление комментария с несколькими картинками (как альбом)
    # Укажите свои пути
    # photo_paths = ["image.jpg", "image2.png"] # Замените на реальные пути
    # await add_comment_photos(post_object, photo_paths)

    # Добавление нескольких комментариев с файлами
    # Укажите свои пути
    # file_paths = ["file1.zip", "document.pdf"] # Замените на реальные пути
    # await add_comments_file(post_object, file_paths)


if __name__ == "__main__":
    print("Запуск клиента...")
    try:
        # Используем `with client`, чтобы сессия корректно запускалась и завершалась
        with client:
            client.loop.run_until_complete(main())
    except Exception as e:
        print(f"Произошла критическая ошибка при работе клиента: {e}")

    print("\nРабота клиента завершена.")