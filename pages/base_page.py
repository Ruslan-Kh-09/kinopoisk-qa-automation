"""Модуль базового класса для реализации паттерна Page Object."""

from typing import List
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Базовый класс страницы со встроенными явными ожиданиями."""

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """Инициализация базовой страницы."""
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, timeout)

    @allure.step("Открытие веб-страницы по URL: {url}")
    def open(self, url: str) -> None:
        """Открывает указанный URL в браузере."""
        self.driver.get(url)

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        """Ожидает появление элемента в DOM и возвращает его."""
        condition = EC.presence_of_element_located(locator)
        element: WebElement = self.wait.until(condition)
        return element

    def find_elements(
        self, locator: tuple[str, str]
    ) -> List[WebElement]:
        """Ожидает появление списка элементов в DOM."""
        condition = EC.presence_of_all_elements_located(locator)
        elements: List[WebElement] = self.wait.until(condition)
        return elements

    @allure.step("Клик по элементу с локатором: {locator}")
    def click(self, locator: tuple[str, str]) -> None:
        """Выполняет клик по элементу после его ожидания."""
        condition = EC.element_to_be_clickable(locator)
        self.wait.until(condition).click()

    @allure.step("Ввод текста '{text}' в поле: {locator}")
    def enter_text(self, locator: tuple[str, str], text: str) -> None:
        """Очищает поле и вводит в него указанный текст."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
