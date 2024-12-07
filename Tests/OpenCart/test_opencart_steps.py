
import pytest
from TeamWebQaUPT.utils import navigate_menu, validate_elements_in_list

@pytest.mark.parametrize("browser_name", ["chrome", "firefox", "edge"])
def test_navigation_opencart(browser_name, driver):
    driver.get("https://demo.opencart.com/")
    navigate_menu(
        driver,
        menu_items={
            "Desktops": "https://demo.opencart.com/index.php?route=product/category&path=20",
            "Laptops & Notebooks": "https://demo.opencart.com/index.php?route=product/category&path=18",
        },
        base_url="https://demo.opencart.com/"
    )

@pytest.mark.parametrize("browser_name", ["chrome", "firefox", "edge"])
def test_validate_categories(browser_name, driver):
    driver.get("https://demo.opencart.com/")
    validate_elements_in_list(
        driver,
        xpath_template="//a[text()='{}']",
        items=["Desktops", "Laptops & Notebooks", "Tablets"]
    )
