import logging

from selenium import webdriver

from base.components.behave_support import BehaveSupport as BS

logger = logging.getLogger('driver')


def init(context):
    logger.warning('Initializing Browser\n')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    prefs = {"profile.default_content_setting_values.geolocation": 2}
    options.add_experimental_option("prefs", prefs)

    BS(context).set_context_var('browser', webdriver.Chrome(options=options))
    info(context)


def close(context):
    try:
        context.browser.close()
        context.browser.quit()
    except Exception as e:
        logger.exception(f'Failed to close Chrome browser:\n\t{e.__repr__()}')


def is_alive(context):
    return hasattr(context, "browser")


def take_screenshot(context):
    try:
        return context.browser.get_screenshot_as_png()
    except Exception as e:
        logger.debug(f"Failed to take Chrome screenshot:\n\t{e.__repr__}")


def info(context):
    capabilities = context.browser.capabilities
    logger.debug(f"Browser Info:\n"
                 f"{capabilities['browserName']} "
                 f"{capabilities['browserVersion']}\n"
                 f"driver "
                 f"{capabilities['chrome']['chromedriverVersion'].split(' ')[0]}\n")
