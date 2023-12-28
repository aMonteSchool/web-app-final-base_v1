from typing import List, Optional

from deepdiff import DeepDiff


class CustomAssert:
    """
    Custom assertion class to work with DeepDiff
    """

    def __init__(self,
                 act_data: dict | List[dict],
                 exp_data: dict | List[dict],
                 exclude_path: Optional[str] = None):
        """
        :param dict | List[dict] act_data: Actual data to compare
        :param dict | List[dict] exp_data: Expected data to compare
        :param Optional[str] exclude_path: Exclude paths (DeepDiff parameter)
        """

        if (not (isinstance(act_data, dict) and isinstance(exp_data, dict))
                or not (isinstance(act_data, list) and isinstance(exp_data, list))):
            raise ValueError(f"Provide dict type objects for assertion"
                             f"\nActual: {type(act_data)}"
                             f"\nExpected: {type(exp_data)}")
        self.act_data = act_data
        self.exp_data = exp_data
        self.exclude_path = exclude_path
        self.diff: List = []

    def equal(self):
        """
        Selects the comparison method based on type of data
        """

        if self.__check_objects_empty():
            return

        if isinstance(self.act_data, list):
            self.__compare_lists()
        else:
            self.__compare_dicts(self.act_data, self.exp_data)

        assert not self.diff, self.__print_diff()

    def __check_objects_empty(self):
        """
        Checks if the items for comparison are empty
        """

        return True if (not self.act_data and not self.exp_data) else False

    def __compare_dicts(self, act_data, exp_data):
        """
        Checks if two dicts are equal

        :param act_data: Actual dict to compare
        :param exp_data: Expected dict to compare
        """

        params = {'ignore_order': True}

        if self.exclude_path:
            params['exclude_paths'] = self.exclude_path

        diff = DeepDiff(act_data, exp_data, **params)

        if diff and 'values_changed' in diff:
            self.diff.append(diff['values_changed'])
        elif diff and 'dictionary_item_added' in diff:
            self.diff.append(diff)

    def __compare_lists(self):
        """
        Checks if two lists of dicts are equal
        """

        for x, y in zip(self.act_data, self.exp_data):
            self.__compare_dicts(x, y)

    def __print_diff(self):
        for diff in self.diff:
            for key, val in diff.items():
                if isinstance(val, dict):
                    for k, v in val.items():
                        print(f"{k}: {v}")
                else:
                    for it in val:
                        print(f"{it}")
