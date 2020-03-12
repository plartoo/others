"""This Class will be used directly or will be inherited
by transform modules for individual countries.

This Class or its children module will be imported by
transform.py module to execute data processing steps.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import re

import pandas as pd

import transform_errors


def return_value_type_check(f):
    def check_callable(*args, **kwargs):
        """
        Helper function which asserts that all functions implemented
        within TransformFunctions and its subclasses return pandas
        dataframe. If not, raise exception.
        """
        r = f(*args, **kwargs)
        if not isinstance(r, pd.DataFrame):
            raise Exception(f"Functions defined within TransformFunctions "
                            f"and/or its subclasses must return pandas' dataframe, "
                            f"but this function, '{f.__name__}', is returning: {r!r}")
        return r
    return check_callable


class TransformFunctions:
    """
    Meta class to serve as a parent class so that we can enforce
    the rule that every transform function must return pandas
    dataframe.

    Also in this meta class, we can implement helper functions,
    which does NOT necessarily return dataframe and can be used
    by transform functions.
    """
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


    def _cap_sentence(self, s):
        """
        Capitalize the first letter then join it back together.
        Remember, we do NOT want to use '.title()' method of
        Python's string library because it'll have undesired effect
        such as transforming 'GDN Video' to 'Gdn Video' and
        'YouTube' to 'Youtube'.
        REF: https://stackoverflow.com/a/42500863/1330974
        """
        # TODO: remove line below
        # print(s)
        return re.sub("(^|\s)(\S)", lambda m: m.group(1) + m.group(2).upper(), s)


class CommonTransformFunctions(TransformFunctions):
    """
    ALL **COMMON** transform functions must be written as part of this class.
    getattr(obj, function_name)(*args, **kwargs)
    REF: https://stackoverflow.com/a/2203479
         https://stackoverflow.com/a/6322114
    """
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


    def check_possible_duplicates_in_one_column(self,
                                                df,
                                                col_name) -> pd.DataFrame:
        """
        This method will make sure that the given column (col_name)
        does NOT have duplicate values. It will do so by first
        turning all letters of each value in the column to small case.
        Then it will retain alpha-numerical values of the aforementioned
        values. Then by comparing the difference between the set of
        original values vs. that of modified values, this method will
        raise an Alert/Error message telling user that they should
        look at possible duplicate values and re-map them as necessary.

        For example, these values in 'Channel' column are possible
        duplicates: ['YouTube', 'Youtube', 'Other social', 'other social',
        'E-commerce',' ECommerce']. This method will create a new set of
        values like this: {'youtube', 'other social', 'ecommerce'} and
        by comparing it against the original set of values, it will detect
        possible duplicates

        NOTE: In Python, \W = [^a-zA-Z0-9_]
        REF: https://docs.python.org/3/library/re.html

        Args:
            df: Raw dataframe to search for duplicates.
            col_name:   Column name in the dataframe in which we should
                        look for duplicates.

        Returns:
            Original dataframe if no duplicates are found.

        Raises:
            PossibleDuplicateError, if there's a possible duplicate values.
        """
        orig_values = set(df[col_name].values)
        non_alpha_numerical_chars_pattern = re.compile(r'\W', re.UNICODE)
        simplified_values = {non_alpha_numerical_chars_pattern.sub('', s).lower()
                             for s in orig_values}
        if len(orig_values) != len(simplified_values):
            err_msg = ''.join(["Possible duplicates found in the values of column, '",
                               col_name, "':\n", str(sorted(orig_values)),
                               ".\nPlease update/map these values to new, standardized values."
                               ])
            raise transform_errors.PossibleDuplicateError(err_msg)

        return df


    def check_possible_duplicates_in_multiple_columns(self,
                                                      df,
                                                      list_of_col_names) -> pd.DataFrame:
        """
        This method will check if any of the given list of columns
        has duplicate values in it. It will do so by first
        turning all letters of each value in individual column to small case.
        See description of "check_possible_duplicates_in_one_column" for
        more detail.

        Args:
            df: Raw dataframe to search for duplicates.
            col_name:   Column name in the dataframe in which we should
                        look for duplicates.

        Returns:
            Original dataframe if no duplicates are found.

        Raises:
            PossibleDuplicateError, if there's a possible duplicate values.
        """
        non_alpha_numerical_chars_pattern = re.compile(r'\W', re.UNICODE)
        for col_name in list_of_col_names:
            orig_values = set(df[col_name].values)
            simplified_values = {non_alpha_numerical_chars_pattern.sub('', s).lower()
                                 for s in orig_values}
            if len(orig_values) != len(simplified_values):
                err_msg = ''.join(["Possible duplicates found in the values of column, '",
                                   col_name, "':\n", str(sorted(orig_values)),
                                   ".\nPlease update/map these values to new, standardized values."
                                   ])
                raise transform_errors.PossibleDuplicateError(err_msg)

        return df


    def capitalize_first_letter_of_each_word_in_one_column(self,
                                                           df,
                                                           col_name):
        """
        This method will make sure every word of the values in a given
        column (col_name) will be capitalized.
        For example, suppose we have these values for 'col1':
        ['Other social', 'Other Social', 'Female body cleansers',
        'Female Body cleansers'], this method will transform these
        values into this - [Other Social', 'Other Social',
        'Female Body Cleansers', 'Female Body Cleansers'].

        Args:
            df: Raw dataframe to capitalize the beginning of each word.
            col_name:   Column name in the dataframe in which we should
                        look to capitalize the beginning of each word.
        Returns:
            Dataframe with the column values where the first letter of
            each word is capitalized.
        """
        if not isinstance(col_name, str):
            raise transform_errors.InputDataTypeError("Column name must be of string type")

        df[col_name] = df[col_name].apply(lambda s: self._cap_sentence(s))

        return df


    def capitalize_first_letter_of_each_word_in_multiple_columns(self,
                                                                 df,
                                                                 list_of_col_names):
        """
        This method will capitalize every word in a given list of columns
        (list_of_col_names). This method is basically a modified version of
        "capitalize_first_letter_of_each_word_in_column_values" to transform
        more than one column.

        NOTE: I have decided to not call "capitalize_first_letter_of_each_word_in_one_column"
        from this method because I don't want to pass in the dataframe
        many times (which is inefficient in terms of memory  consumption)
        into another method although it'd have been a better coding practice.

        Args:
            df: Raw dataframe to capitalize the beginning of each word.
            list_of_col_names:  List of column names in the dataframe
                                in which we should look to capitalize
                                the beginning of each word.
        Returns:
            Dataframe with the column values (for each of the columns in
            list_of_col_names) where the first letter of each word is
            capitalized.
        """
        if not isinstance(list_of_col_names, list):
            raise transform_errors.InputDataTypeError("List of column names must "
                                                      "be of list type with individual "
                                                      "names being string values.")

        for col_name in list_of_col_names:
            # TODO: df['Region'].unique() have 'nan' value, and
            # we can see them via df[df['Region'].isnull()] (not via df[df['Region'] == pd.np.nan]
            # so **we need a method to set nan and then null values to something like empty string**
            df[col_name] = df[col_name].apply(lambda s: self._cap_sentence(s))

        return df


    def update_values_in_one_column(self,
                                    df,
                                    col_name,
                                    dictionary_of_value_mappings)  -> pd.DataFrame:
        """
        Given a dataframe, column name and dictionary representing
        old-to-new-value mappings for the column, apply the mappings.

        For example, if we want 'Ecommerce' and 'Amazon' values in 'col1' of the
        dataframe to be updated to 'E-Commerce', we would call this method like this:
        update_values_in_columns(df, "col1", {"Ecommerce": "E-Commerce", "Amazon": "E-Commerce"}).
        REF: https://stackoverflow.com/a/20250996

        Args:
            df: Raw dataframe to transform.
            col_name: Column to update values at.
            dictionary_of_value_mappings: Dictionary which represents mappings between
            original values and desired (updated) values.
            E.g., if we want 'Amazon' and 'Ecommerce' to be mapped to 'E-Commerce'
            we should provide {"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}.

        Returns:
            Dataframe with updated values based on provided arguments.
        """
        if not isinstance(col_name, str):
            raise transform_errors.InputDataTypeError("Column name must be of string type")

        if not isinstance(dictionary_of_value_mappings, dict):
            raise transform_errors.InputDataTypeError(
                "Value (old to new) mappings must be of dictionary type")

        df[col_name] = df[col_name].map(dictionary_of_value_mappings).fillna(df[col_name])

        return df


    def update_values_in_multiple_columns(self,
                                          df,
                                          list_of_col_names,
                                          list_of_dictionary_of_value_mappings)  -> pd.DataFrame:
        """
        Given a dataframe, list of columns and corresponding list of dictionaries
        representing old-to-new-value mappings for each column, apply these
        mappings to each column.

        For example, if we want 'Ecommerce' and 'Amazon' values in 'col1' of the
        dataframe to be updated to 'E-Commerce', we would call this method like this:
        update_values_in_columns(df, ["col1"], {"Ecommerce": "E-Commerce", "Amazon": "E-Commerce"}).
        REF: https://stackoverflow.com/a/20250996

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of columns to update values at.
            For example, if we want 'col1' and 'col2' values to be updated, we
            provide: ['col1', 'col2'].
            list_of_dictionary_of_value_mappings: List of dictionaries, each of them
            representing original values and desired (updated) values.
            E.g., if we want 'Amazon' and 'Ecommerce' to be mapped to 'E-Commerce'
            we should provide [{"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}]

        Returns:
            Dataframe with updated values based on provided arguments.
        """
        if len(list_of_col_names) != len(list_of_dictionary_of_value_mappings):
            raise transform_errors.InputDataLengthError("The length of column list:",
                                                    len(list_of_col_names),
                                                    "is NOT the same as the length of",
                                                    "list of dictionaries of update values:",
                                                    len(list_of_dictionary_of_value_mappings))
        for i, col in enumerate(list_of_col_names):
            df[col] = df[col].map(list_of_dictionary_of_value_mappings[i]).fillna(df[col])

        return df


    def update_values_in_col2_based_on_col1_values(self,
                                                   df,
                                                   base_column_name,
                                                   target_column_name,
                                                   dictionary_of_value_pairs)  -> pd.DataFrame:
        """
        Given a dataframe, two column names (col1 and col2) and a dictionary
        representing col1-values-to-new-col2-values mappings, apply the mappings.

        E.g., whenever we see 'Ecommerce' or 'Amazon' in column named, 'Channel',
        we want to update values in 'Macro Channel' column to 'E-Commerce'.
        In this case, we provide following args to this method:
        update_values_in_col2_based_on_col1_values(df, "Channel", "Macro Channel",
        {"Ecommerce": "E-Commerce", "Amazon": "E-Commerce"})
        REF: https://stackoverflow.com/a/19226745/1330974

        Args:
            df: Raw dataframe to transform.
            base_column_name:   Base column name whose values we need to use to
                                determine if we need to update values in another
                                (target) column.
            target_column_name: Target column name whose values we need update
                                based on the values in the base column.
            dictionary_of_value_mappings:
                                Dictionary which holds keys representing values
                                from base column and values representing values
                                from target column.
                                E.g., whenever we see 'Amazon' and 'Ecommerce'
                                in base column, we want target column values
                                to be updated to 'E-Commerce', we should provide
                                {"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}.

        Returns:
            Dataframe with updated values based on provided arguments.
        """
        if not (isinstance(base_column_name, str) and isinstance(target_column_name, str)):
            raise transform_errors.InputDataTypeError("Column names must be of string type")

        if not isinstance(dictionary_of_value_pairs, dict):
            raise transform_errors.InputDataTypeError(
                "Col1-Col2 value pairs must be of dictionary type")

        df[target_column_name] = df[base_column_name].map(dictionary_of_value_pairs).fillna(df[target_column_name])

        return df


    def create_new_column_based_on_another_column_values(self,
                                                         df,
                                                         new_col_name,
                                                         existing_col_name,
                                                         dictionary_of_mappings):
        """
        Creates a new column using dictionary of mappings in which keys represent
        values in existing column name and dict values representing values in
        the new column.

        For example, say we have a column named 'Channel' in our original
        dataframe with values "GDN Display", "GDN Video" and "YouTube".
        We want to create a new column named "NewChannelNames" and in that
        column, whenever we see "GDN Display" in 'Channel' column, we want to
        enter "Display"; when we see "GDN Video" in 'Channel' column, we want
        to enter "Online Video"; when we see "YouTube" in 'Channel' column,
        we want to enter "Online Video" in the new column, we call this method
        with parameters like this:
        create_new_column_based_on_another_column_values(df, "NewChannelNames",
        "Channel", {"GDN Display": "Display", "GDN Video": "Online Video",
        "YouTube": "Online Video"}).

        REF: https://stackoverflow.com/a/24216489

        Args:
            df: Raw dataframe to transform.
            new_col_name: Name of the new column to be created.
            existing_col_name: Name of the column which already exist in
            the dataframe and the one we should use as a base to map from.
            dictionary_of_mappings: Dictionary representing key-value pairs
            of existing column's values (as keys) and new column's values
            (as values).

        Returns:
            The dataframe with new column attached which has values in the
            mapping provided.
        """
        if not (isinstance(new_col_name, str) and isinstance(existing_col_name, str)):
            raise transform_errors.InputDataTypeError("Column names must be of string type")

        if not isinstance(dictionary_of_mappings, dict):
            raise transform_errors.InputDataTypeError(
                "Mapping key-value pairs must be of dictionary type")

        df[new_col_name] = df[existing_col_name].map(dictionary_of_mappings)

        return df


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


    def assert_no_null_values_in_columns(self,
                                         df,
                                         list_of_col_names) -> pd.DataFrame:
        """
        Assert that there is no NULL/NaN values in the list
        of columns provided.

        Args:
            df: Raw dataframe to check for Nan/NULL values.
            list_of_col_names: List of column names (each is of string type)
            in which we should look for NaN/NULL values.
            REF1: https://stackoverflow.com/a/27159258
            REF2: https://stackoverflow.com/a/42923089

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            NaNFoundError: If there is any NaN/NULL value in the given list
            of columns.
        """
        # for col_name in list_of_col_names:
        import pdb
        pdb.set_trace()
        print("test")


        # if df.shape[1] != num_of_cols_expected:
        #     raise transform_errors.ColumnCountError(
        #         ' '.join(["Expected column count of:", str(num_of_cols_expected),
        #                   "but found:", str(df.shape[1]), "in the current dataframe."])
        #     )
        # else:
        #     print("Successfully check that the current dataframe has:", num_of_cols_expected, "columns.")

        return df


    def assert_no_nan_values_in_columns(self,
                                        df,
                                        list_of_col_names) -> pd.DataFrame:
        # TODO: to implement
        pass


    def assert_no_empty_string_values_in_columns(self,
                                                 df,
                                                 list_of_col_names) -> pd.DataFrame:
        # TODO: to implement
        pass


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
#     CommonTransformFunctions().__init__()