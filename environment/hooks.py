from base.environment import chrome
from base.components.behave_support import BehaveSupport as BS


def scenario_background(context, scenario):
    if 'no_background' in scenario.tags:
        scenario.background = None


def browser(context, scenario):
    start_browser = True

    if 'same_browser' in scenario.feature.tags:

        if hasattr(context, 'background_once') and not 'run_background' in scenario.tags:
            scenario.background = None
            start_browser = False
        else:
            BS(context).set_context_var('background_once', True)

    if start_browser:
        if chrome.is_alive(context) and scenario.background:
            chrome.close(context)
        chrome.init(context)

def before_scenario(context, scenario):
    scenario_background(context, scenario)
    browser(context, scenario)
