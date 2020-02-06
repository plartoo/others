"""This Class will be used directly or will be inherited
by transform modules for individual countries.

This Class or its children module will be imported by
transform.py module to execute data processing steps.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""


class TransformFunctions(object):
    """
    ALL **COMMON** transform functions must be written as part of this class.
    getattr(obj, function_name)(*args, **kwargs)
    REF: https://stackoverflow.com/a/2203479
         https://stackoverflow.com/a/6322114
    """

    def __init__(self):
        pass


    def drop_columns(self, df, col_idx):
        """
        Drop columns from a dataframe and returns the resulting dataframe.
        REF: https://stackoverflow.com/a/18145399

        Args:
            df: Raw dataframe from which we need to drop columns.
            list_of_cols: List of column indexes (

        Returns:
            Dataframe from which the columns are dropped.
        """


    def rename_columns(self, df, old_to_new_cols_dict):
        # df.rename(columns=old_to_new_col_mappings, inplace=True) if not old_to_new_col_mappings
        print("hey rename_columns was called")


    def _trim_space(self, cell_str):
        return str(cell_str).strip()


    def remove_dollars(self):
        """
        Remove the dollar sign given a data frame.
        :return:
        """
        pass


    def multiply_by_thousand(self):
        pass


    def parent_function(self):
        print("calling parent")


# if __name__ == '__main__':
#     TransformFunctions().__init__()