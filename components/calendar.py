from datetime import date

from dateutil import parser
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from base.components.base import Base


class PickupDate(Base):
    """
    Picks a date in a calendar
    """

    CALENDAR_OPEN = '//input[@name="PickupDate"]'
    CALENDAR_MODAL = '//div[@id="ui-datepicker-div"]'
    PREV_MONTH = '//a[contains(@class, "ui-datepicker-prev")]'
    NEXT_MONTH = '//a[contains(@class, "ui-datepicker-next")]'
    TITLE = '//div[@class="ui-datepicker-title"]'
    DATE = '//a[@class="ui-state-default"][@data-date="{day}"]'
    CALENDAR_PAGE = ('//div[contains(@class, "ui-datepicker-group")]'
                     '[.//span[@class="ui-datepicker-month"][text() = "{month}"]]'
                     '[.//span[@class="ui-datepicker-year"][text() = "{year}"]]')

    def __init__(self, driver: WebDriver, pick_date: str):
        """
        :param WebDriver driver: Selenium Web Driver object
        :param str pick_date: Date to pick
        """

        super().__init__(driver)
        self.date = parser.parse(pick_date).date()

    def open_calendar(self):
        """
        Opens a calendar
        """

        self.click(self.CALENDAR_OPEN)
        self.wait_calendar_to_open()

    def wait_calendar_to_open(self):
        """
        Waits for Calendar window to open
        """

        self.find_element(self.CALENDAR_MODAL)

    def find_calendar_page(self):
        """
        Finds the correct calendar page
        """

        self.open_calendar()

        for i in range(12):
            try:
                return self.find_element(
                    self.CALENDAR_PAGE.format(month=self.date.strftime("%B"), year=self.date.strftime("%Y")),
                    timeout=3)
            except TimeoutException:
                self.click(self.NEXT_MONTH)

        raise ValueError("Select the pickup date within 12 months")

    def pick_date(self):
        """
        Picks a date
        """

        assert self.date >= date.today(), "Pickup date could not be in the past"
        date_page = self.find_calendar_page()
        date_page.find_element(By.XPATH, f".{self.DATE.format(day=self.date.day)}").click()
