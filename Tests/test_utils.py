import unittest
from unittest.mock import MagicMock
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from TeamWebQaUPT.utils import (
    select_dropdown_option,
    validate_elements_in_list,
    navigate_menu,
    navigate_linklabel,
    process_table_data,
    search_and_validate_results
)

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.driver = MagicMock(spec=WebDriver)

    def test_select_dropdown_option(self):
        dropdown_mock = MagicMock(spec=WebElement)
        option_mock = MagicMock(spec=WebElement)

        self.driver.find_element.return_value = dropdown_mock
        dropdown_mock.click.return_value = None

        select_dropdown_option(
            self.driver,
            dropdown_selector=".dropdown",
            option_text="Option 1"
        )

        dropdown_mock.click.assert_called_once()

    def test_validate_elements_in_list(self):
        xpath_template = "//span[text()='{}']"
        items = ["Item 1", "Item 2"]

        element_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = element_mock
        element_mock.is_displayed.return_value = True

        validate_elements_in_list(self.driver, xpath_template, items)

        # Verificar llamadas
        self.driver.find_element.assert_any_call("xpath", "//span[text()='Item 1']")
        self.driver.find_element.assert_any_call("xpath", "//span[text()='Item 2']")

    def test_navigate_menu(self):
        menu_items = {"Menu 1": "http://example.com/menu1"}
        self.driver.current_url = "http://example.com"

        menu_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = menu_mock

        navigate_menu(self.driver, menu_items, base_url="http://example.com")

        menu_mock.click.assert_called_once()
        self.driver.get.assert_called_with("http://example.com")

    def test_navigate_linklabel(self):
        link_mock = MagicMock(spec=WebElement)
        self.driver.find_element.return_value = link_mock

        navigate_linklabel(
            self.driver,
            link_selector=".link",
            expected_url="http://example.com/link"
        )

        link_mock.click.assert_called_once()

    def test_process_table_data(self):
        table_data = [
            ["Name", "Age", "Country"],
            ["Alice", "30", "USA"],
            ["Bob", "25", "Canada"]
        ]
        expected_output = [
            {"Name": "Alice", "Age": "30", "Country": "USA"},
            {"Name": "Bob", "Age": "25", "Country": "Canada"}
        ]

        result = process_table_data(table_data)

        self.assertEqual(result, expected_output)

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
        self.assertTrue(any("Result 1" in result_mock.text for result_mock in self.driver.find_elements.return_value))


if __name__ == "__main__":
    unittest.main()
