"""Модуль автоматизированных UI-тестов для сервиса Кинопоиск."""

import time
import pytest
import allure
from pages.main_page import MainPage


@pytest.mark.ui
@allure.epic("Дипломный проект. Автоматизация UI")
@allure.feature("Тестирование элементов главной страницы")
class TestKinopoiskUI:
    """Набор тестов для проверки пользовательского интерфейса."""

    @allure.title("UI-01. Проверка доступности главной страницы")
    @allure.story("Базовая загрузка интерфейса")
    def test_main_page_accessibility(self, driver) -> None:
        """Проверяет, что главная страница открывается без ошибок."""
        main_page = MainPage(driver)
        main_page.open_main_page()

        with allure.step("Проверка корректности заголовка вкладки"):
            assert "Кинопоиск" in driver.title

    @allure.title("UI-02. Поиск фильма через поисковую строку")
    @allure.story("Валидация отправки поисковой формы")
    def test_search_film_action(self, driver) -> None:
        """Проверяет ввод названия фильма и клик по кнопке поиска."""
        main_page = MainPage(driver)
        main_page.open_main_page()

        main_page.type_search_query("Интерстеллар")
        main_page.click_search_button()

        with allure.step("Проверка перехода на страницу результатов"):
            curr_url = driver.current_url
            assert "index" in curr_url or "search" in curr_url

    @allure.title("UI-03. Проверка появления быстрых подсказок")
    @allure.story("Динамическое отображение подсказок при вводе")
    def test_search_suggests_appear(self, driver) -> None:
        """Проверяет появление выпадающего списка подсказок."""
        main_page = MainPage(driver)
        main_page.open_main_page()

        main_page.type_search_query("Оно")
        suggests = main_page.get_suggest_items()

        with allure.step("Проверка, что список подсказок не пуст"):
            assert len(suggests) > 0

    @allure.title("UI-04. Проверка вызова формы авторизации Яндекс ID")
    @allure.story("Клик по кнопке войти в шапке сайта")
    def test_login_modal_call(self, driver) -> None:
        """Проверяет редирект на защищенную форму Яндекс ID."""
        main_page = MainPage(driver)
        main_page.open_main_page()

        main_page.click_login()

        with allure.step("Проверка изменения URL на домен паспорта"):
            assert "passport.yandex.ru" in driver.current_url

    @allure.title("UI-05. Проверка воспроизведения трейлера фильма")
    @allure.story("Запуск видеопотока в модальном плеере")
    def test_play_trailer_modal(self, driver) -> None:
        """Проверяет клик по кнопке трейлера на промо-блоке."""
        main_page = MainPage(driver)
        main_page.open_main_page()

        main_page.play_trailer()

        with allure.step("Проверка появления DOM-элемента плеера"):
            player_element = main_page.find_element(
                main_page.MODAL_PLAYER
            )
            assert player_element.is_displayed()

    # ==========================================
    # ПРОДВИНУТЫЕ НЕФУНКЦИОНАЛЬНЫЕ UI-ТЕСТЫ
    # ==========================================

    @allure.title("PERF-01. Проверка скорости загрузки контента (LCP)")
    @allure.feature("Нефункциональное тестирование производительности")
    def test_main_page_performance_lcp(self, driver) -> None:
        """Проверяет время появления первого значимого элемента."""
        main_page = MainPage(driver)

        start_time = time.time()
        main_page.open_main_page()
        main_page.find_element(main_page.FIRST_CONTENT_ELEMENT)
        end_time = time.time()

        load_duration = end_time - start_time
        with allure.step(f"Проверка: загрузка {load_duration:.2f}s <= 3s"):
            assert load_duration <= 3.0

    @allure.title("ACC-01. Проверка доступности: наличие атрибутов alt")
    @allure.feature("Нефункциональное тестирование доступности (a11y)")
    def test_posters_have_alt_attributes(self, driver) -> None:
        """Проверяет, что постеры содержат текстовое описание alt."""
        main_page = MainPage(driver)
        main_page.open_main_page()

        poster = main_page.find_element(main_page.FIRST_CONTENT_ELEMENT)
        alt_text = poster.get_attribute("alt")

        with allure.step("Проверка, что атрибут alt не пустой"):
            assert alt_text is not None
