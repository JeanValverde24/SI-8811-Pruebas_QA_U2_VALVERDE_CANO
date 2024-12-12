import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from TeamWebQaUPT.utils import (
    select_dropdown_option,
    validate_elements_in_list,
    navigate_menu,
    navigate_linklabel,
    search_and_validate_results,
)
from TeamWebQaUPT.webdriver_config import get_driver
from TeamWebQaUPT.runner import main

class TestUtils:

    def setup_method(self):
        self.driver = MagicMock()

    def teardown_method(self):
        self.driver.reset_mock()

    def test_select_dropdown_option(self):
        dropdown_mock = MagicMock(spec=WebElement)
        option_mock = MagicMock(spec=WebElement)

        self.driver.find_element.side_effect = [dropdown_mock, option_mock]
        dropdown_mock.click.return_value = None
        option_mock.click.return_value = None

        select_dropdown_option(self.driver, dropdown_selector=".dropdown", option_text="Option 1")

        dropdown_mock.click.assert_called_once()
        option_mock.click.assert_called_once()

    def test_select_dropdown_option_timeout(self):
        self.driver.find_element.side_effect = TimeoutException

        with pytest.raises(AssertionError, match="No se pudo seleccionar la opción"):
            select_dropdown_option(self.driver, dropdown_selector=".dropdown", option_text="Option 1")

    def test_validate_elements_in_list(self):
        xpath_template = "//span[text()='{}']"
        items = ["Item 1", "Item 2"]

        element_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = element_mock
        element_mock.is_displayed.return_value = True

        validate_elements_in_list(self.driver, xpath_template, items)

        for item in items:
            self.driver.find_element.assert_any_call("xpath", xpath_template.format(item))

    def test_validate_elements_in_list_not_found(self):
        xpath_template = "//span[text()='{}']"
        items = ["Nonexistent Item"]

        self.driver.find_element.side_effect = TimeoutException

        with pytest.raises(AssertionError, match="No se pudo encontrar el elemento"):
            validate_elements_in_list(self.driver, xpath_template, items)

    def test_navigate_menu(self):
        menu_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = menu_mock
        menu_mock.click.return_value = None

        navigate_menu(self.driver, {"Menu 1": "http://example.com/menu1"}, base_url="http://example.com")

        menu_mock.click.assert_called_once()

    def test_navigate_linklabel(self):
        link_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = link_mock
        link_mock.click.return_value = None
        self.driver.current_url = "http://example.com/link"

        navigate_linklabel(self.driver, link_selector=".link", expected_url="http://example.com/link")

        link_mock.click.assert_called_once()

    def test_search_and_validate_results(self):
        search_input_mock = MagicMock(spec=WebElement)
        search_button_mock = MagicMock(spec=WebElement)
        result_mock = MagicMock(spec=WebElement)
        result_mock.text = "Result 1"

        self.driver.find_element.side_effect = [search_input_mock, search_button_mock]
        self.driver.find_elements.return_value = [result_mock]

        search_and_validate_results(
            self.driver,
            search_input_selector=".search-input",
            search_button_selector=".search-button",
            search_term="Test",
            results_selector=".results",
            expected_results=["Result 1"]
        )

        search_input_mock.send_keys.assert_called_once_with("Test")
        search_button_mock.click.assert_called_once()

class TestWebDriverConfig:

    def test_get_driver_chrome(self):
        with patch("selenium.webdriver.Chrome") as mock_driver:
            driver = get_driver("chrome")
            assert driver is not None

    def test_get_driver_firefox(self):
        with patch("selenium.webdriver.Firefox") as mock_driver:
            driver = get_driver("firefox")
            assert driver is not None

    def test_get_driver_edge(self):
        with patch("selenium.webdriver.Edge") as mock_driver:
            driver = get_driver("edge")
            assert driver is not None

    def test_get_driver_invalid(self):
        with pytest.raises(ValueError):
            get_driver("invalid_browser")

class TestRunner:

    def test_main(self):
        with patch("pytest.main") as mock_pytest:
            mock_pytest.return_value = 0
            main()
            mock_pytest.assert_called_once()

if __name__ == "__main__":
    pytest.main()