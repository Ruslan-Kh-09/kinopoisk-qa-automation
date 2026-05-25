"""Модуль хранения настроек окружения и тестовых данных."""

import os
from dotenv import load_dotenv

# Автоматически загружаем переменные из локального файла .env в систему
load_dotenv()

# Настройки окружения (Environment settings)
BASE_URL_UI = "https://kinopoisk.ru"
BASE_URL_API = "https://kinopoiskapiunofficial.tech"

# Тестовые данные (Test Data)
# Безопасное извлечение токена из переменных окружения
API_KEY = os.getenv("API_KEY", "PLACEHOLDER_TOKEN")
DEFAULT_FILM_ID = 301
