import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from TeamWebQaUPT.utils import (
    select_dropdown_option,
    validate_elements_in_list,
    navigate_menu,
    navigate_linklabel,
    process_table_data,
    search_and_validate_results,
)

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.driver = MagicMock()

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_select_dropdown_option(self, mock_wait):
        # Mock the dropdown and option elements
        dropdown_mock = MagicMock(spec=WebElement)
        option_mock = MagicMock(spec=WebElement)
        mock_wait.side_effect = [dropdown_mock, option_mock]

        select_dropdown_option(
            self.driver, dropdown_selector=".dropdown", option_text="Option 1"
        )
        dropdown_mock.click.assert_called_once()
        option_mock.click.assert_called_once()

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_validate_elements_in_list_success(self, mock_wait):
        # Mock the element found
        element_mock = MagicMock(spec=WebElement)
        element_mock.is_displayed.return_value = True
        mock_wait.return_value = element_mock

        validate_elements_in_list(self.driver, "//span[text()='{}']", ["Item 1"])
        element_mock.is_displayed.assert_called_once()

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_validate_elements_in_list_not_found(self, mock_wait):
        # Simulate timeout for element not found
        mock_wait.side_effect = TimeoutException

        with self.assertRaises(AssertionError):
            validate_elements_in_list(self.driver, "//span[text()='{}']", ["Item 1"])

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_navigate_menu(self, mock_wait):
        # Mock menu navigation
        menu_mock = MagicMock(spec=WebElement)
        mock_wait.side_effect = [menu_mock]

        navigate_menu(
            self.driver,
            {"Menu 1": "http://example.com/menu1"},
            base_url="http://example.com",
        )
        menu_mock.click.assert_called_once()

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_navigate_linklabel(self, mock_wait):
        # Mock link navigation
        link_mock = MagicMock(spec=WebElement)
        mock_wait.return_value = link_mock

        navigate_linklabel(
            self.driver, link_selector=".link", expected_url="http://example.com/link"
        )
        link_mock.click.assert_called_once()

    def test_process_table_data(self):
        table_data = [
            ["Name", "Age", "City"],
            ["Alice", "30", "New York"],
            ["Bob", "25", "Los Angeles"],
        ]
        expected_result = [
            {"Name": "Alice", "Age": "30", "City": "New York"},
            {"Name": "Bob", "Age": "25", "City": "Los Angeles"},
        ]
        result = process_table_data(table_data)
        self.assertEqual(result, expected_result)

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_search_and_validate_results(self, mock_wait):
        # Mock search input, button, and result elements
        search_input_mock = MagicMock(spec=WebElement)
        search_button_mock = MagicMock(spec=WebElement)
        result_mock = MagicMock(spec=WebElement)
        result_mock.text = "Result 1"
        mock_wait.side_effect = [search_input_mock, search_button_mock, [result_mock]]

        search_and_validate_results(
            self.driver,
            search_input_selector=".search-input",
            search_button_selector=".search-button",
            search_term="Test",
            results_selector=".results",
            expected_results=["Result 1"],
        )
        search_input_mock.send_keys.assert_called_once_with("Test")
        search_button_mock.click.assert_called_once()
        self.assertIn("Result 1", result_mock.text)

if __name__ == "__main__":
    unittest.main()
