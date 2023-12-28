from typing import Optional

from selenium.webdriver.chrome.webdriver import WebDriver


class JSSupport:
    """
    JS scripts to support
    """

    def __init__(self, driver: WebDriver):
        """
        :param WebDriver driver: Selenium Web Driver object
        """

        self.driver = driver

    def scroll_down_page(self, speed: Optional[int] = 8):
        """
        Scrolls down the page

        :param int speed: Optional speed value, default is 8
        """

        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            self.driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self.driver.execute_script("return document.body.scrollHeight")

    @staticmethod
    def element_click(driver, element):
        """
        JS click on the element ignoring visibility or overlapping
        """

        driver.execute_script('arguments[0].click();', element)

    @staticmethod
    def open_new_tab(driver, link=None):
        if link:
            driver.execute_script('window.open(arguments[0]);', link)
        else:
            driver.execute_script('window.open();')

    @staticmethod
    def close_tab(driver, tab):
        driver.execute_script('window.close(arguments[0]);', tab)

    @staticmethod
    def scroll_to_the_top(driver):
        driver.execute_script('window.scrollTo(0, 0)')

    @staticmethod
    def scroll_to_the_bottom(driver):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    @staticmethod
    def get_input_value(driver, element):
        """
        Extract value from the input
        """

        return driver.execute_script("arguments[0].value;", element)
