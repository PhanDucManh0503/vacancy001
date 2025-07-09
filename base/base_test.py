import pytest
from selenium import webdriver
from utils.read_config import ConfigReader

class BaseTest:
    @pytest.fixture(scope="class", autouse=True)
    def driver(self, request):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(ConfigReader.get_base_url())
        driver.implicitly_wait(5)
        request.cls.driver = driver
        yield driver
        driver.quit()
