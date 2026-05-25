"""Модуль автоматизированных API-тестов для сервиса Кинопоиск."""

from typing import Any
import allure
import pytest
from api_client.kinopoisk_api import KinopoiskAPI
import config


@pytest.fixture(scope="session")
def api() -> KinopoiskAPI:
    """Фикстура для инициализации API-клиента перед тестами."""
    return KinopoiskAPI(
        base_url=config.BASE_URL_API, api_key=config.API_KEY
    )


@pytest.mark.api
@allure.epic("Дипломный проект. Автоматизация API")
@allure.feature("Тестирование контентных эндпоинтов")
class TestKinopoiskAPI:
    """Набор тестов для проверки работоспособности бэкенда."""

    # ==========================================
    # ПОЗИТИВНЫЕ ТЕСТЫ
    # ==========================================

    @allure.title("Р-01. Получение данных о фактах и ошибках фильма")
    @allure.story("Успешный запрос фактов о фильме")
    def test_get_film_facts_success(self, api: KinopoiskAPI) -> None:
        """Проверяет эндпоинт фактов о фильме с валидным ID."""
        endpoint = f"/api/v2.2/films/{config.DEFAULT_FILM_ID}/facts"
        response = api.get(endpoint)

        with allure.step("Проверка статус-кода ответа (Ожидается 200 OK)"):
            assert response.status_code == 200

        with allure.step("Проверка структура (Наличие массива items)"):
            json_data = response.json()
            assert "items" in json_data
            assert isinstance(json_data["items"], list)

    @allure.title("Р-02. Получение списка похожих фильмов")
    @allure.story("Успешный запрос похожих медиаматериалов")
    def test_get_similar_films_success(self, api: KinopoiskAPI) -> None:
        """Проверяет получение рекомендаций для конкретного фильма."""
        endpoint = f"/api/v2.2/films/{config.DEFAULT_FILM_ID}/similars"
        response = api.get(endpoint)

        with allure.step("Проверка статус-кода ответа (Ожидается 200 OK)"):
            assert response.status_code == 200

        with allure.step("Проверка наличия ключевых полей в элементах"):
            json_data = response.json()
            assert "items" in json_data
            if json_data["items"]:
                first_item = json_data["items"][0]
                assert "filmId" in first_item
                assert "nameRu" in first_item

    @allure.title("Р-03. Получение списка кинопремьер")
    @allure.story("Фильтрация премьер по году и месяцу")
    def test_get_premieres_success(self, api: KinopoiskAPI) -> None:
        """Проверяет работу фильтрации афиши премьер."""
        params = {"year": 2024, "month": "MAY"}
        response = api.get("/api/v2.2/films/premieres", params=params)

        with allure.step("Проверка статус-кода ответа (Ожидается 200 OK)"):
            assert response.status_code == 200

    @allure.title("Р-05. Получение детальной информации о фильме")
    @allure.story("Запрос карточки фильма по ID")
    def test_get_film_details_success(self, api: KinopoiskAPI) -> None:
        """Проверяет отдачу полей сущности фильма."""
        endpoint = f"/api/v2.2/films/{config.DEFAULT_FILM_ID}"
        response = api.get(endpoint)

        with allure.step("Проверка статус-кода ответа (Ожидается 200 OK)"):
            assert response.status_code == 200

        with allure.step("Проверка соответствия возвращенного ID"):
            res_id = response.json().get("kinopoiskId")
            assert res_id == config.DEFAULT_FILM_ID

    # ==========================================
    # НЕГАТИВНЫЕ ТЕСТЫ (ПОДПИСАННЫЕ XFAIL НА БАГИ)
    # ==========================================

    @pytest.mark.xfail(
        reason="BUG-001: Дефект обработки исключений на сервере. "
               "При отправке метода POST вместо GET эндпоинт падает "
               "в ошибку 500 Internal Server Error вместо "
               "возврата легитимного статуса 405 Method Not Allowed."
    )
    @allure.title("N-01. Некорректный HTTP-метод (POST вместо GET)")
    @allure.story("Валидация ограничений методов на сервере")
    def test_post_instead_of_get_fails(self, api: KinopoiskAPI) -> None:
        """Тест воспроизведения бага с падением в 500 ошибку."""
        endpoint = f"/api/v2.2/films/{config.DEFAULT_FILM_ID}"
        response = api.post(endpoint)

        with allure.step("Проверка статус-кода (Ожидается 405)"):
            assert response.status_code == 405

    @allure.title("N-02. Запрос данных с некорректным токеном")
    @allure.story("Проверка системы безопасности API")
    def test_invalid_token_fails(self) -> None:
        """Проверяет реакцию на невалидный заголовок X-API-KEY."""
        bad_api = KinopoiskAPI(
            base_url=config.BASE_URL_API, api_key="INVALID_TOKEN_123"
        )
        endpoint = f"/api/v2.2/films/{config.DEFAULT_FILM_ID}"
        response = bad_api.get(endpoint)

        with allure.step("Проверка статус-кода ответа (Ожидается 401)"):
            assert response.status_code == 401

    @allure.title("N-03. Запрос премьер без параметра 'year'")
    @allure.story("Проверка валидации обязательных параметров")
    def test_get_premieres_without_year_fails(
        self, api: KinopoiskAPI
    ) -> None:
        """Проверяет защиту от пропущенных query-параметров."""
        params = {"month": "MAY"}
        response = api.get("/api/v2.2/films/premieres", params=params)

        with allure.step("Проверка статус-кода ответа (Ожидается 400)"):
            assert response.status_code == 400

    @pytest.mark.xfail(
        reason="BUG-002: Дефект валидации бизнес-логики. Бэкенд "
               "полностью пропускает некорректные диапазоны лет "
               "(год в будущем, отрицательный год, ноль) и "
               "возвращает статус 200 OK вместо отсечения по коду "
               "400 Bad Request."
    )
    @pytest.mark.parametrize("invalid_year, description", [
        (2050, "Год в будущем"),
        (-2025, "Отрицательный год"),
        (0, "Нулевой год")
    ])
    @allure.story("Валидация граничных значений года премьер")
    def test_get_premieres_invalid_years_fails(
        self, api: KinopoiskAPI, invalid_year: int, description: str
    ) -> None:
        """Кейсы N-05, N-06, N-07: некорректные диапазоны лет."""
        title = f"N-05/06/07. Ошибка на: {description} ({invalid_year})"
        allure.dynamic.title(title)

        params = {"year": invalid_year, "month": "MAY"}
        response = api.get("/api/v2.2/films/premieres", params=params)

        with allure.step(f"Проверка реакции бэкенда на {description}"):
            assert response.status_code == 400

    @pytest.mark.parametrize("invalid_month", ["03", 3, "NOT_A_MONTH"])
    @allure.title("N-04. Запрос премьер с некорректным типом месяца")
    @allure.story("Проверка валидации типов данных на бэкенде")
    def test_get_premieres_invalid_month_fails(
        self, api: KinopoiskAPI, invalid_month: Any
    ) -> None:
        """Проверяет строгую типизацию полей на уровне бэкенда."""
        params = {"year": 2024, "month": invalid_month}
        response = api.get("/api/v2.2/films/premieres", params=params)

        with allure.step("Проверка статус-кода ответа (Ожидается 400)"):
            assert response.status_code == 400

    @pytest.mark.xfail(
        reason="BUG-003: Нарушение архитектуры REST API. При "
               "запросе подресурсов для несуществующего ID фильма "
               "сервер отдает пустой массив со статусом 200 OK "
               "вместо легитимного ответа 404 Not Found."
    )
    @allure.title("N-08. Запрос списка для несуществующего ID")
    @allure.story("Проверка обработки отсутствующих сущностей")
    def test_get_similars_for_non_existent_film_fails(
        self, api: KinopoiskAPI
    ) -> None:
        """Проверяет возврат 404 ошибки для отсутствующего контента."""
        response = api.get("/api/v2.2/films/9999999/similars")

        with allure.step("Проверка статус-кода ответа (Ожидается 404)"):
            assert response.status_code == 404
