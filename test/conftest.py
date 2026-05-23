"""Модуль общих фикстур для организации UI и API тестов."""

from typing import Generator
import allure
import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    """Инициализирует и закрывает WebDriver для каждого UI-теста."""
    with allure.step("Запуск и настройка браузера Google Chrome"):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--silent")

        # Комплексная маскировка под реального пользователя против капчи
        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        options.add_experimental_option(
            "useAutomationExtension", False
        )

        chrome_driver = webdriver.Chrome(options=options)

        # Стираем след присутствия Selenium в DOM через инъекцию JS
        js_bypass = (
            "Object.defineProperty(navigator, 'webdriver', "
            "{get: () => undefined})"
        )
        chrome_driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": js_bypass}
        )

        chrome_driver.maximize_window()

    yield chrome_driver

    with allure.step("Закрытие сессии браузера"):
        chrome_driver.quit()
