from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from base.components.base import Base


class CustomSelect(Base):
    SELECT = '//label[contains(., "Pick Up Time")]/select'
    def __init__(self, driver: WebDriver):
        super().__init__(driver)


    def by_value(self, locator: str, value: str):
        Select(self.find_element(locator))

