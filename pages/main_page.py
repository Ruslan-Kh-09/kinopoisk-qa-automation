"""Модуль описания элементов и логики Главной страницы Кинопоиска."""

from typing import List
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
import config


class MainPage(BasePage):
    """Класс Главной страницы с локаторами элементов интерфейса."""

    # 🔍 Локаторы элементов (Селекторы)
    SEARCH_INPUT = (By.NAME, "kp_query")
    SEARCH_BUTTON = (By.CLASS_NAME, "search-form__submit")
    SUGGEST_WINDOW = (By.CLASS_NAME, "kinopoisk-header-item__suggest")
    SUGGEST_ITEMS = (By.CLASS_NAME, "suggest-item")
    LOGIN_BUTTON = (
        By.XPATH, "//button[contains(text(), 'Войти')]"
    )
    TRAILER_PLAY_BUTTON = (
        By.XPATH, "//button[contains(@class, 'ButtonWatchTrailer')]"
    )
    MODAL_PLAYER = (By.CLASS_NAME, "discovery-trailer-player")

    # Продвинутые локаторы для нефункциональных тестов из чек-листов
    CARD_NUMBER_MASKED = (By.CLASS_NAME, "payment-card__number")
    FIRST_CONTENT_ELEMENT = (By.CLASS_NAME, "feed-complex-poster")

    @allure.step("Открыть главную страницу Кинопоиска")
    def open_main_page(self) -> None:
        """Открывает стартовый URL из конфигурационного файла."""
        self.open(config.BASE_URL_UI)

    @allure.step("Ввести название фильма '{film_name}' в строку поиска")
    def type_search_query(self, film_name: str) -> None:
        """Вводит поисковый запрос в input."""
        self.enter_text(self.SEARCH_INPUT, film_name)

    @allure.step("Нажать на кнопку поиска")
    def click_search_button(self) -> None:
        """Выполняет клик для отправки поисковой формы."""
        self.click(self.SEARCH_BUTTON)

    @allure.step("Получить список быстрых подсказок (саджестов)")
    def get_suggest_items(self) -> List[WebElement]:
        """Ожидает появление окна подсказок и возвращает элементы."""
        self.find_element(self.SUGGEST_WINDOW)
        return self.find_elements(self.SUGGEST_ITEMS)

    @allure.step("Нажать кнопку 'Войти' для вызова Яндекс ID")
    def click_login(self) -> None:
        """Выполняет клик по кнопке авторизации в шапке сайта."""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Нажать на кнопку воспроизведения трейлера")
    def play_trailer(self) -> None:
        """Запускает трейлер фильма на главном промо-блоке."""
        self.click(self.TRAILER_PLAY_BUTTON)
