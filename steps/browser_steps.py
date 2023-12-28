import logging
from time import sleep
from behave import step
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base.environment import chrome
from base.helpers.helper import map_url

logger = logging.getLogger('browser')


@step('Browser: navigate to "{url}"')
def navigate_to_url(context, url):
    """
    Navigate to url
    """
    url = map_url(url)
    context.browser.get(url)
    assert context.browser.current_url == url


@step('Browser: navigate to {url} in new tab')
def navigate_to_url(context, url):
    """
    Navigate to url
    """

    context.execute_steps('''* Browser: open new tab''')
    context.browser.get('/'.join([path.strip('/') for path in url.split('/')]))


@step('Browser: open new tab')
def open_new_tab(context):
    """
    Open new tab
    """

    context.browser.execute_script("window.open('');")
    sleep(2)


@step('Browser: close current tab')
def close_tab_and_go_to_previous(context):
    """
    Close current tab
    """

    context.browser.close()
    sleep(2)


@step('Browser: switch to the previous tab')
def switch_back_tp_previous_tab(context):
    all_tabs = context.browser.window_handles
    index = all_tabs.index(context.browser.current_window_handle)

    if index > 0:
        previous_tab = all_tabs[index - 1]
        context.browser.switch_to.window(previous_tab)
    sleep(2)


@step('Browser: refresh the page')
def browser_refresh(context):
    """
    Refresh browser
    """

    context.browser.refresh()

    # hard page reload
    context.browser.execute_script("location.reload(true);")

    try:
        # accept reload if alert is present
        WebDriverWait(context.browser, 3).until(EC.alert_is_present())

        logger.debug(
            "Alert is present and will be accepted",
            {'screenshot': chrome.take_screenshot()})

        context.browser.switch_to.alert.accept()
        logger.debug("Alert accepted")
    except TimeoutException:
        pass

    sleep(2)


@step('Browser: forward')
def browser_back(context):
    context.browser.forward()
    sleep(2)


@step('Browser: back')
def browser_back(context):
    context.browser.back()
    sleep(2)


@step('Browser: close browser session')
def close_browser(context):
    chrome.close(context)
