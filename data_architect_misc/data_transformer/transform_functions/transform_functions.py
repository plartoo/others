"""This Class will be used directly or will be inherited
by transform modules for individual countries.

This Class or its children module will be imported by
transform.py module to execute data processing steps.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import pandas as pd

import transform_errors


def return_value_type_check(f):
    def check_callable(*args, **kwargs):
        r = f(*args, **kwargs)
        if not isinstance(r, pd.DataFrame):
            raise Exception(f"Functions defined within TransformFunctions "
                            f"and/or its subclasses must return pandas' dataframe, "
                            f"but this function, '{f.__name__}', is returning: {r!r}")
        return r
    return check_callable


class TransformFunctions:
    def __init_subclass__(cls, **kwargs):
        """
        Run time check to see if functions in this class
        and its subclasses return pandas dataframe, which
        is a pre-requisite.
        REF: https://stackoverflow.com/a/60571077/1330974
        """
        super().__init_subclass__(**kwargs)
        for k, v in cls.__dict__.items():
            if callable(v):
                setattr(cls, k, return_value_type_check(v))


class CommonTransformFunctions(TransformFunctions):
    """
    ALL **COMMON** transform functions must be written as part of this class.
    getattr(obj, function_name)(*args, **kwargs)
    REF: https://stackoverflow.com/a/2203479
         https://stackoverflow.com/a/6322114
    """

    # def __init__(self, **kwargs):
    #     """
    #     Run time check to see if functions in this class
    #     and its subclasses return pandas dataframe, which
    #     is a pre-requisite.
    #     REF: https://stackoverflow.com/a/60571077/1330974
    #     """
    #     super().__init__(**kwargs)
    #     import pdb
    #     pdb.set_trace()
    #     for k, v in self.__dict__.items():
    #         print(k, v)
    #         if callable(v):
    #             setattr(self, k, return_value_type_check(v))


    # def __init_subclass__(cls, **kwargs):
    #     """
    #     Run time check to see if functions in this class
    #     and its subclasses return pandas dataframe, which
    #     is a pre-requisite.
    #     REF: https://stackoverflow.com/a/60571077/1330974
    #     """
    #     super().__init_subclass__(**kwargs)
    #     for k, v in cls.__dict__.items():
    #         if callable(v):
    #             setattr(cls, k, return_value_type_check(v))


    def drop_columns_by_index(self, df, list_of_col_idx) -> pd.DataFrame:
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


    def drop_columns_by_name(self, df, list_of_col_names) -> pd.DataFrame:
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


    def drop_unnamed_columns(self, df) -> pd.DataFrame:
        """
        Drop columns that have 'Unnamed' as column header, which is a usual
        occurrence for some Excel/CSV raw data files with empty but hidden columns.
        Args:
            df: Raw dataframe to transform.
            params: We don't need any parameter for this function,
                    so it's defaulted to None.

        Returns:
            Dataframe whose 'Unnamed' columns are dropped.
        """
        return df.loc[:, ~df.columns.str.contains(r'Unnamed')]


    def rename_columns(self, df, old_to_new_cols_dict) -> pd.DataFrame:
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


    # def parent_return_int(self, df) -> int:
    #     return 1


    def update_values_in_columns(self,
                                 df,
                                 list_of_col_names,
                                 list_of_dictionary_of_update_values)  -> pd.DataFrame:
        """
        Given a dataframe, list of columns and corresponding list of dictionaries
        representing old-to-new-value mappings for each column, apply these
        mappings to each column.

        For example, if we want 'Ecommerce' and 'Amazon' values in 'col1' of the
        dataframe to be updated to 'E-Commerce', we would call this method like this:
        update_values_in_columns(df, ["col1"], {"Ecommerce": "E-Commerce", "Amazon": "E-Commerce"}).

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of columns to update values at.
            For example, if we want 'col1' and 'col2' values to be updated, we
            provide: ['col1', 'col2'].
            list_of_dictionary_of_update_values: List of dictionaries, each of them
            representing original values and desired (updated) values.
            E.g., if we want 'Amazon' and 'Ecommerce' to be mapped to 'E-Commerce'
            we should provide [{"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}]

        Returns:
            Dataframe with updated values based on provided arguments.
        """
        # https://stackoverflow.com/a/20250996
        if len(list_of_col_names) != len(list_of_dictionary_of_update_values):
            raise transform_errors.InputLengthError("The length of column list:",
                                                    len(list_of_col_names),
                                                    "is NOT the same as the length of",
                                                    "list of dictionaries of update values:",
                                                    len(list_of_dictionary_of_update_values))
        print("update_values_in_columns")
        for i, col in enumerate(list_of_col_names):
            df[col] = df[col].map(list_of_dictionary_of_update_values[i]).fillna(df[col])

        # return df


    def assert_number_of_columns_equals(self, df, num_of_cols_expected) -> pd.DataFrame:
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
            raise transform_errors.ColumnCountError(
                ' '.join(["Expected column count of:", str(num_of_cols_expected),
                          "but found:", str(df.shape[1]), "in the current dataframe."])
            )
        else:
            print("Successfully check that the current dataframe has:", num_of_cols_expected, "columns.")

        return df


    def _trim_space(self, cell_str) -> pd.DataFrame:
        return str(cell_str).strip()


    def remove_dollars(self) -> pd.DataFrame:
        """
        Remove the dollar sign given a data frame.
        :return:
        """
        pass


    def multiply_by_thousand(self) -> pd.DataFrame:
        pass


    def parent_function(self) -> pd.DataFrame:
        print("calling parent")


# if __name__ == '__main__':
#
#     CommonTransformFunctions().__init__()
#     # TransformFunctions().__init__()