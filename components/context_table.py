from typing import List, Optional, Dict, Any

from behave.runner import Context

from base.components.behave_support import BehaveSupport


class ContextTable(BehaveSupport):
    """"
    Apply desired structure to context table data
    """

    def __init__(self, context: Context):
        """
        :param Context context: Behave Context object
        """
        super().__init__(context)
        self.table = context.table if context.table else None

    def to_list_of_dicts(self, **kwargs: str) -> List[dict]:
        """Converts Context Table into list of dicts

        :param str kwargs: Optional convert values from str to list()
        :return: list of dictionaries
        """

        result = []
        if not self.table:
            return result

        for row in self.table.rows:
            result.append(dict(row.items))

        for row in result:
            for key, val in row.items():
                if kwargs and key == kwargs['key'] and kwargs['type'] == list:
                    row.update({key: val.split(", ")})

                v = val.split('.')[-1]
                row[key] = self.get_context_var(v)

        return result

    def to_list(self, idx: Optional[int] = 0) -> List:
        """Converts Context Table into list of dicts

        :param int idx: Optional index of column, default is 0
        :return: list
        """

        result = []

        if not self.table:
            return result

        result = [self.table.headings[idx]]
        for row in self.table.rows:
            result.extend(row.cells)

        return self.get_context_var(result)

    def to_flat_dict(self) -> Dict:
        """Converts Context Table into flat dict where items in columns[0] = Keys, columns[1] = Values

        :return: Dict
        """
        result = {}

        if not self.table:
            return result

        result = {self.table.headings[0]: self.table.headings[1]}
        for row in self.table.rows:
            result[row.cells[0]] = self.__update_val(row.cells[1])

        return result

    def __update_val(self, v: Any) -> Any:
        """Converts value into desired type or gets from context

        :param Any v: Value to convert
        :return: Any type converted value
        """

        return eval(v) if any(v.startswith(x) for x in {'int(', 'dict(', '['}
                              ) else self.get_context_var(v)
