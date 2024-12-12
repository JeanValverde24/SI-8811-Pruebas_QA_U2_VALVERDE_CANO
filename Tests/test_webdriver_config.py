import unittest
from unittest.mock import patch, MagicMock
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from TeamWebQaUPT.webdriver_config import get_driver

class TestWebDriverConfig(unittest.TestCase):

    @patch("selenium.webdriver.Remote")
    def test_get_driver_chrome(self, mock_remote):
        mock_remote.return_value = MagicMock(spec=Remote)

        driver = get_driver("chrome")
        self.assertIsInstance(driver, Remote)
        mock_remote.assert_called_once()
        args, kwargs = mock_remote.call_args

        self.assertIn("options", kwargs)
        self.assertIsInstance(kwargs["options"], ChromeOptions)
        self.assertTrue(kwargs["options"].get_capability("se:recordVideo"))

    @patch("selenium.webdriver.Remote")
    def test_get_driver_firefox(self, mock_remote):
        mock_remote.return_value = MagicMock(spec=Remote)

        driver = get_driver("firefox")
        self.assertIsInstance(driver, Remote)
        mock_remote.assert_called_once()
        args, kwargs = mock_remote.call_args

        self.assertIn("options", kwargs)
        self.assertIsInstance(kwargs["options"], FirefoxOptions)
        self.assertTrue(kwargs["options"].get_capability("se:recordVideo"))

    @patch("selenium.webdriver.Remote")
    def test_get_driver_edge(self, mock_remote):
        mock_remote.return_value = MagicMock(spec=Remote)

        driver = get_driver("edge")
        self.assertIsInstance(driver, Remote)
        mock_remote.assert_called_once()
        args, kwargs = mock_remote.call_args

        self.assertIn("options", kwargs)
        self.assertIsInstance(kwargs["options"], EdgeOptions)
        self.assertTrue(kwargs["options"].get_capability("se:recordVideo"))

    def test_get_driver_invalid_browser(self):
        with self.assertRaises(ValueError):
            get_driver("invalid_browser")

    @patch("selenium.webdriver.Remote")
    def test_get_driver_default_capabilities(self, mock_remote):
        mock_remote.return_value = MagicMock(spec=Remote)

        driver = get_driver("chrome")
        self.assertIsInstance(driver, Remote)
        mock_remote.assert_called_once()
        args, kwargs = mock_remote.call_args

        self.assertIn("options", kwargs)
        self.assertEqual(kwargs["options"].get_capability("se:name"), "chrome")
        self.assertTrue(kwargs["options"].get_capability("se:recordVideo"))
