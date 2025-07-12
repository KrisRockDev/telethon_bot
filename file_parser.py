import os

def get_info(base_dir="downloads"):
    # Сканирует первую поддиректорию в base_dir, классифицирует файлы и возвращает их пути и другую информацию в словаре.
    # :param base_dir: Директория для сканирования (например, "downloads").
    # :return: Словарь с путями к файлам или None, если директория пуста или не найдена.

    if not os.path.isdir(base_dir):
        print(f"Ошибка: Директория '{base_dir}' не найдена.")
        return None

    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not subdirs:
        print(f"Ошибка: В директории '{base_dir}' нет поддиректорий для обработки.")
        return None

    film_dir_name = subdirs[0]
    film_dir_path = os.path.join(base_dir, film_dir_name)
    print(f"--- Обработка директории: {film_dir_path} ---")

    file_paths = {
        "poster": None,
        "info_file": None,          # Для info.txt
        "description_file": None,   # Для des.txt
        "screenshots": [],
        "torrents": [],
        "post_text": film_dir_name
    }

    poster_filename = "poster.jpg"
    if os.path.exists(os.path.join(film_dir_path, poster_filename)):
        file_paths["poster"] = os.path.join(film_dir_path, poster_filename)

    for filename in os.listdir(film_dir_path):
        full_path = os.path.join(film_dir_path, filename)

        if filename.lower() == "info.txt":
            file_paths["info_file"] = full_path
        elif filename.lower() == "des.txt":
            file_paths["description_file"] = full_path
        elif filename.lower().endswith(('.jpg', '.jpeg', '.png')) and filename.lower() != poster_filename:
            file_paths["screenshots"].append(full_path)
        elif filename.lower().endswith('.torrent'):
            file_paths["torrents"].append(full_path)

    print("Файлы успешно классифицированы:")
    print(f"  Текст поста: {file_paths['post_text']}")
    print(f"  Постер: {file_paths['poster']}")
    print(f"  Файл с информацией (для поста): {file_paths['info_file']}")
    print(f"  Файл с описанием (для комментария): {file_paths['description_file']}")
    print(f"  Скриншоты: {len(file_paths['screenshots'])} шт.")
    print(f"  Торренты: {len(file_paths['torrents'])} шт.")

    return file_paths