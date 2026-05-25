"""Модуль описания элементов и логики Главной страницы Кинопоиска."""

from typing import List
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
import config


class MainPage(BasePage):
    """Класс Главной страницы с локаторами элементов интерфейса."""

    # 🔍 Локаторы элементов (Селекторы обновлены под верстку 2026 года)
    # Используем CSS_SELECTOR и XPATH с относительными путями
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Фильмы']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUGGEST_WINDOW = (
        By.XPATH, "//*[contains(@class, 'suggest') or @role='listbox']"
    )
    SUGGEST_ITEMS = (
        By.XPATH, "//div[contains(@class, 'suggest-item') or @role='option']"
    )
    LOGIN_BUTTON = (
        By.XPATH, "//button[contains(text(), 'Войти')]"
    )
    TRAILER_PLAY_BUTTON = (
        By.XPATH, "//button[contains(., 'Трейлер') or contains(., 'трейлер')]"
    )
    MODAL_PLAYER = (
        By.XPATH,
        "//div[contains(@class, 'player') or contains(@class, 'modal')]"
    )

    # Стабильные элементы для нефункциональных тестов
    HEADER_LOGO = (By.CSS_SELECTOR, "a[href='/'] svg, img[alt='Логотип']")
    FIRST_POSTER = (By.CSS_SELECTOR, "img[class*='poster'], img[class*='image']")

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
