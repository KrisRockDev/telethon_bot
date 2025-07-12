
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# --- API-ключи и сессия ---
# Получены при регистрации приложения на my.telegram.org
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
# Имя файла сессии, создается автоматически при первом запуске
SESSION_NAME = os.getenv('SESSION_NAME', 'my_session')

# --- ID чатов ---
# ID целевого канала для публикации постов
RAW_CHANNEL_ID = os.getenv('CHANNEL_ID')
# ID группы, привязанной к каналу для комментариев
RAW_GRUP_ID = os.getenv('GRUP_ID')

# --- Валидация и преобразование типов ---
if not all([API_ID, API_HASH, RAW_CHANNEL_ID, RAW_GRUP_ID]):
    raise ValueError(
        "Ключевые переменные не найдены. Убедитесь, что в файле .env заданы: "
        "API_ID, API_HASH, CHANNEL_ID и GRUP_ID."
    )

try:
    # ID в Telegram должны быть целочисленными
    CHANNEL_ID = int(RAW_CHANNEL_ID)
    GRUP_ID = int(RAW_GRUP_ID)
except (ValueError, TypeError):
    raise TypeError(
        "CHANNEL_ID и GRUP_ID в .env файле должны быть числами (например, -100123456789)."
    )