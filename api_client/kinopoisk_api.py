"""Модуль HTTP-клиента для взаимодействия с API Кинопоиска."""

from typing import Any, Dict, Optional
import allure
import requests


class KinopoiskAPI:
    """Класс-клиент для отправки структурированных запросов к REST API."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """Инициализирует клиент базовым URL и токеном авторизации."""
        self.base_url: str = base_url

        # Безопасно очищаем токен от возможных пробелов по краям
        clean_key = str(api_key).strip()

        self.headers: Dict[str, str] = {
            "X-API-KEY": clean_key,
            "Content-Type": "application/json"
        }

    @allure.step("Отправка GET-запроса на эндпоинт: {endpoint}")
    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Выполняет HTTP GET-запрос с аннотацией типов данных."""
        url: str = f"{self.base_url}{endpoint}"
        response: requests.Response = requests.get(
            url, headers=self.headers, params=params
        )
        return response

    @allure.step("Отправка POST-запроса на эндпоинт: {endpoint}")
    def post(
        self, endpoint: str, json_data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Выполняет HTTP POST-запрос с аннотацией типов данных."""
        url: str = f"{self.base_url}{endpoint}"
        response: requests.Response = requests.post(
            url, headers=self.headers, json=json_data
        )
        return response
