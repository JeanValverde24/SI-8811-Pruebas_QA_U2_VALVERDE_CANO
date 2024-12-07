import pytest
from TeamWebQaUPT.utils import validate_elements_in_list

@pytest.mark.parametrize("browser_name", ["chrome", "firefox", "edge"])
def test_validate_departments(browser_name, driver):
    driver.get("https://www.amazon.com/")
    validate_elements_in_list(
        driver,
        xpath_template="//a[normalize-space()='{}']",
        items=["Best Sellers", "New Releases", "Movers & Shakers"]
    )