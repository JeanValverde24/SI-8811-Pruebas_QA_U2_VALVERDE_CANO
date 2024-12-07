
import pytest
from TeamWebQaUPT.utils import navigate_menu, validate_elements_in_list

@pytest.mark.parametrize("browser_name", ["chrome", "firefox", "edge"])
def test_navigation_menu_swaglabs(browser_name, driver):
    driver.get("https://www.saucedemo.com/")
    navigate_menu(
        driver,
        menu_items={
            "Products": "https://www.saucedemo.com/inventory.html",
            "About": "https://saucelabs.com/",
        },
        base_url="https://www.saucedemo.com/"
    )

@pytest.mark.parametrize("browser_name", ["chrome", "firefox", "edge"])
def test_validate_products(browser_name, driver):
    driver.get("https://www.saucedemo.com/inventory.html")
    validate_elements_in_list(
        driver,
        xpath_template="//div[@class='inventory_item_name' and text()='{}']",
        items=["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    )
