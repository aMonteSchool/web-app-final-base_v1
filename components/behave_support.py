from typing import Any

from behave.runner import Context


class BehaveSupport:

    def __init__(self, context: Context):
        """
        :param Context context: Behave context object
        """
        self.context = context

    def set_context_var(self, name, value, level='feature'):
        """
        Sets variable to the desired layer (scenario, feature)

        :param Context context: Behave context object
        :param str name: Name of the variable to create
        :param Any value: Value to assign to the variable
        :param str level: Level of the layer to store the var, default is "feature"
        """
        item = next((item for item in self.context._stack if item['@layer'] == level), None)
        item[name] = value

    def get_context_var(self, var: list | str) -> Any:
        """
        Gets value from context variable

        :param list | str var: Value(s) to get
        :return: Any type context variable's value single or in a list
        """

        def get_var(v: str) -> Any:
            val = v.split('.')[-1] if "context." else v
            return getattr(self.context, val, v)

        return [get_var(v) for v in var] if isinstance(var, list) else get_var(var)
