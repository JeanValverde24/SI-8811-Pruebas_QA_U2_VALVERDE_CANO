import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from TeamWebQaUPT.utils import (
    select_dropdown_option,
    navigate_menu,
    navigate_linklabel,
    search_and_validate_results
)


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.driver = MagicMock(spec=WebDriver)

    def test_select_dropdown_option(self):
        dropdown_mock = MagicMock(spec=WebElement)
        option_mock = MagicMock(spec=WebElement)

        with patch('selenium.webdriver.support.ui.WebDriverWait.until') as mock_wait:
            mock_wait.side_effect = [dropdown_mock, option_mock]
            dropdown_mock.click.return_value = None
            option_mock.click.return_value = None

            select_dropdown_option(
                self.driver,
                dropdown_selector=".dropdown",
                option_text="Option 1"
            )

        dropdown_mock.click.assert_called_once()
        option_mock.click.assert_called_once()

    def test_navigate_menu(self):
        menu_items = {"Menu 1": "http://example.com/menu1"}
        self.driver.current_url = "http://example.com"

        menu_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = menu_mock

        with patch('selenium.webdriver.support.ui.WebDriverWait.until') as mock_wait:
            mock_wait.return_value = menu_mock
            menu_mock.click.return_value = None

            navigate_menu(self.driver, menu_items, base_url="http://example.com")

        menu_mock.click.assert_called_once()
        self.driver.get.assert_called_with("http://example.com")

    def test_navigate_linklabel(self):
        link_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = link_mock

        with patch('selenium.webdriver.support.ui.WebDriverWait.until') as mock_wait:
            mock_wait.return_value = link_mock
            link_mock.click.return_value = None
            self.driver.current_url = "http://example.com/link"

            navigate_linklabel(
                self.driver,
                link_selector=".link",
                expected_url="http://example.com/link"
            )

        link_mock.click.assert_called_once()

    def test_search_and_validate_results(self):
        search_input_mock = MagicMock(spec=WebElement)
        search_button_mock = MagicMock(spec=WebElement)
        result_mock = MagicMock(spec=WebElement)
        result_mock.text = "Result 1"

        self.driver.find_element.side_effect = [search_input_mock, search_button_mock]
        self.driver.find_elements.return_value = [result_mock]

        with patch('selenium.webdriver.support.ui.WebDriverWait.until') as mock_wait:
            mock_wait.side_effect = [search_input_mock, search_button_mock, [result_mock]]

            search_input_mock.send_keys.return_value = None
            search_button_mock.click.return_value = None

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


if __name__ == "__main__":
    unittest.main()
