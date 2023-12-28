from typing import Optional, List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as Wait


class Base:
    """
    Base class to update selenium's methods
    """

    SEARCH = '//input[@id = "search"]'

    def __init__(self, driver: WebDriver) -> None:
        """
        :param WebDriver driver: Selenium Web Driver object
        """
        self.driver = driver

    def click(self, locator: str) -> None:
        """
        Applies explicit wait before clicking

        :param str locator: Locator to find an element to click
        """

        Wait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, locator))).click()

    def find_element(self, locator: str, timeout: Optional[int] = 10, visibility: Optional[bool] = True) -> WebElement:
        """
        Applies explicit wait to element finding

        :param str locator: Locator to find element
        """

        func = ec.visibility_of_element_located if visibility else ec.invisibility_of_element_located

        return Wait(self.driver, timeout).until(func((By.XPATH, locator)),
                                                message=f"Cannot locate element by XPath: {locator}")

    def find_elements(self, locator: str, status: Optional[str] = 'Visibility') -> List[WebElement]:
        """
        Applies explicit wait to elements finding

        :param str locator: Locator to find elements
        :param str status: Status of the elements (Visible or Present), Default is Visible
        """

        func = ec.visibility_of_all_elements_located \
            if status.lower() == 'visibility' else ec.presence_of_all_elements_located

        return Wait(self.driver, 10).until(func((By.XPATH, locator)),
                                           message=f"Cannot locate element by XPath: {locator}")

    def action_click(self, locator: str) -> None:
        """
        Clicks on element using Action Chains

        :param str locator: Locator to find the element to move / click on
        """

        ActionChains(self.driver).move_to_element(self.find_element(locator)).pause(.3).click().perform()

    def click_by_offset(self, element: WebElement, x_offset: int, y_offset: int) -> None:
        """
        Clicks on element by offset using Action Chains

        :param WebElement element: Element to move on
        :param int x_offset: X offset to apply
        :param int y_offset: Y offset to apply
        """

        ActionChains(self.driver).move_to_element_with_offset(element, x_offset, y_offset).click().perform()

    @staticmethod
    def send_keys(element: WebElement, value: str) -> None:
        """
        Sends keys to a Web Element

        :param WebElement element: Element to send keys
        :param str value: Value to send
        """
        try:
            element.clear()
            element.send_keys(value)
        except TimeoutException:
            raise ValueError(f"Cannot send keys {value} to the input field")
