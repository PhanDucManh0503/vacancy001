import pytest
from base.base_test import BaseTest
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.read_config import ConfigReader

class TestLogin(BaseTest):
    def test_login_success(self, driver):
        login_page = LoginPage(self.driver)
        login_page.login(
            ConfigReader.get_username(),
            ConfigReader.get_password()
        )

        dashboard = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-text--h6"))
        )

        assert "OrangeHRM" in self.driver.title
        assert dashboard.text == "Dashboard"
