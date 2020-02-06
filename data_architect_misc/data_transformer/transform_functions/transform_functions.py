"""This Class will be used directly or will be inherited
by transform modules for individual countries.

This Class or its children module will be imported by
transform.py module to execute data processing steps.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import transform_errors


class TransformFunctions(object):
    """
    ALL **COMMON** transform functions must be written as part of this class.
    getattr(obj, function_name)(*args, **kwargs)
    REF: https://stackoverflow.com/a/2203479
         https://stackoverflow.com/a/6322114
    """

    # def __init__(self):
    #     pass

    # TODO: Maybe add type hints?
    def drop_columns_by_index(self, df, list_of_col_idx):
        """
        Drop columns from a dataframe using a list of indexes.
        REF: https://stackoverflow.com/a/18145399

        Args:
            df: Raw dataframe to transform.
            list_of_col_idx: List of column indexes (starting from 0).
                            E.g., [0, 10] to delete the 1st and 11th columns.

        Returns:
            Dataframe with columns dropped.
        """
        return df.drop(df.columns[list_of_col_idx], axis=1)


    def drop_columns_by_name(self, df, list_of_col_names):
        """
        Drop columns from a dataframe using a list of column names (strings).
        REF: https://stackoverflow.com/a/18145399

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of column names (string).
                                E.g., ['Channel', 'Network']

        Returns:
            Dataframe with columns dropped.
        """
        return df.drop(list_of_col_names, axis=1)


    def rename_columns(self, df, old_to_new_cols_dict):
        """
        Rename column headers to new ones given a dictionary of
        old to new column names.
        REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of column names (string type).
                                E.g., ['Channel', 'Network']

        Returns:
            Dataframe with column headers renamed.
        """
        return df.rename(columns=old_to_new_cols_dict)


    def assert_number_of_columns_equals(self, df, num_of_cols_expected):
        """
        Assert that the total number of columns in the dataframe
        is equal to num_of_cols (int).

        Args:
            df: Raw dataframe to transform.
            num_of_cols_expected: Number of columns expected (int).

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            ColumnCountMismatchError: If the number of columns found
            does not equal to what is expected.
        """
        if df.shape[1] != num_of_cols_expected:
            import pdb
            pdb.set_trace()
            raise transform_errors.ColumnCountError(
                ' '.join(["Expected column count of:", str(num_of_cols_expected),
                          "but found:", str(df.shape[1]), "in the current dataframe."])
            )

        return df


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