uv self update
cd E:\py\main
mkdir telethon_bot
cd telethon_bot
uv init
uv venv
# 🔧 Базовые утилиты
# Набор полезных инструментов для Python
uv add pytools
# Упаковка Python проектов в wheel-формат
uv add wheel
# Стандартный инструмент для сборки и установки пакетов
uv add setuptools
# Прогресс-бары в консоли
uv add tqdm
# Работа с HTTP (используется многими библиотеками)
uv add urllib3

# 🌐 Работа с HTTP-запросами и HTML
# Простая работа с HTTP-запросами
uv add requests
# Парсинг HTML и XML
uv add beautifulsoup4
# Генерация HTML из Python-структур
uv add pydoll-python
# Автоматическая перезагрузка кода при изменениях
uv add jurigged
# Утилиты для работы с данными и структурами
uv add boltons

# 🖼️ Работа с изображениями, PDF и нотификациями
# Удобный вывод переменных для отладки
uv add icecream
# Работа с переменными окружения
uv add python-dotenv
# Логирование с красивым выводом
uv add loguru
# Встроенный модуль логирования (необязательно устанавливать)
uv add logging
# Работа с изображениями
uv add pillow
# Генерация PDF-файлов с помощью wkhtmltopdf
uv add pdfkit
# Отправка уведомлений на рабочий стол
uv add desktop-notifier
# Управление браузером для автотестов/парсинга
uv add playwright
# Создание PDF-документов из HTML
uv add hotpdf

# 📦 JSON
# Быстрый JSON-сериализатор на Rust
uv add orjson
# Упрощённый и ускоренный JSON
uv add ujson
# Расширение стандартного json с улучшенной точностью
uv add simplejson

# 🤖 Телеграм-боты
# Асинхронный фреймворк для Telegram-ботов
uv add aiogram
# Работа с Telegram API напрямую (боты и пользователи)
uv add telethon

# ⚙️ Асинхронность
# Асинхронные HTTP-запросы
uv add aiohttp
# Асинхронная работа с файлами
uv add aiofiles
# Асинхронная SQLite база данных
uv add aiosqlite
# Асинхронный драйвер PostgreSQL
uv add asyncpg

# 🗄️ ORM и базы данных
# Универсальный ORM (поддержка разных БД)
uv add sqlalchemy

uv sync --upgrade
uv run main.py