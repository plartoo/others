"""This Class will be used directly or will be inherited
by transform modules for individual countries.

This Class or its children module will be imported by
transform.py module to execute data processing steps.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import datetime
import logging
import re

import pandas as pd
import numpy as np

import transform_errors
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER


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

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def __init_subclass__(cls, **kwargs):
        """
        Run time check to see if functions in this class
        and its subclasses return pandas dataframe, which
        is a pre-requisite.
        REF: https://stackoverflow.com/a/60571077/1330974
        """
        super().__init_subclass__(**kwargs)
        for f_name, f_object in cls.__dict__.items():
            if (f_name != '__init__') and callable(f_object):
                setattr(cls, f_name, return_value_type_check(f_object))

    def _cap_sentence(self, s):
        """
        Capitalize the first letter then join it back together.
        Remember, we do NOT want to use '.title()' method of
        Python's string library because it'll have undesired effect
        such as transforming 'GDN Video' to 'Gdn Video' and
        'YouTube' to 'Youtube'.
        REF: https://stackoverflow.com/a/42500863/1330974
        """
        return re.sub("(^|\s)(\S)", lambda m: m.group(1) + m.group(2).upper(), s)


class CommonTransformFunctions(TransformFunctions):
    """
    ALL **COMMON** transform functions must be written as part of this class.
    getattr(obj, function_name)(*args, **kwargs)
    REF: https://stackoverflow.com/a/2203479
         https://stackoverflow.com/a/6322114
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_data_from_other_sheets_in_excel_file_and_append_to_the_main_dataframe(
            self,
            df,
            list_of_sheet_names
        ):
        """
        Given the list of sheet names, we will append data from these
        sheets to the main dataframe.

        Args:
            df: Original dataframe to append data to.
            list_of_sheet_names: List of Excel sheet names to read data
            from and append to the original dataframe.

        Returns:
            Data frame which now has data from additional sheets
            appended/concatenated.
        """
        for sheet in list_of_sheet_names:
            temp_df = pd.read_excel(
                self.config[KEY_CURRENT_INPUT_FILE],
                sheet_name=sheet,
                header=self.config[KEY_HEADER])

            # To append all sheet with same columns names,
            # those columns names that not match will be at the end of the dataframe
            df = df.append(temp_df)

        return df

    def drop_columns_by_index(
            self,
            df,
            list_of_col_idx
    ):
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


    def drop_columns_by_name(
            self,
            df,
            list_of_col_names
    ):

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

    def drop_columns_by_name_if_they_exist_in_dataframe(
            self,
            df,
            list_of_col_names
    ):

        """
        Drop columns from a dataframe using a list of column names
        (strings).

        **If column name(s) in list_of_col_names is(are) not in the
        dataframe, this method will NOT attempt to drop them. Only
        use this in scenarios where we don't know for sure if a
        column will be included in the raw input file, but we must
        drop it if it appears.**

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of column names (string).
                                E.g., ['Channel', 'Network']

        Returns:
            Dataframe with columns dropped.
        """
        existing_cols = set(df.columns)
        common_cols = set(list_of_col_names).intersection(existing_cols)

        return df.drop(common_cols, axis=1)

    def drop_unnamed_columns(
            self,
            df
    ):
        """
        Drop columns that have 'Unnamed' as column header, which is a usual
        occurrence for some Excel/CSV raw data files with empty but hidden columns.
        Args:
            df: Raw dataframe to transform.

        Returns:
            Dataframe whose 'Unnamed' columns are dropped.
        """
        return df.loc[:, ~df.columns.str.contains(r'Unnamed')]

    def drop_empty_rows(
            self,
            df,
            list_of_col_names,
            reset_index=True
    ):
        """
        Drop rows that have columns (col_names) have empty/blank cells.
        REF: https://stackoverflow.com/a/56708633/1330974

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of column names in which the code
            should check if the cells are empty/blank.
            reset_index: Reset index column. Default is True.

        Returns:
            Dataframe whose empty/blank rows are dropped.
        """
        if not isinstance(list_of_col_names, list):
            raise transform_errors.InputDataTypeError("List of column names must "
                                                      "be of list type with individual "
                                                      "names being string values.")
        for col_name in list_of_col_names:
            df = df[df[col_name].astype(bool)]

        if reset_index:
            return df.reset_index(drop=True)

        return df

    def drop_rows_with_matching_string_values(
            self,
            df,
            list_of_col_names,
            list_of_list_of_string_values
    ):
        """
        Drops rows if any of the columns in the list_of_col_names
        contain a matching string value in the corresponding set
        in the list_of_set_of_string_values.

        For example, if we want to drop rows whenever 'QATAR',
        or 'SAUDI ARABIA' appears in the 'COUNTRY' column, we will
        call this method like below:
        drop_rows_with_certain_string_values(df, ['COUNTRY','REGION'],
        [['SAUDI ARABIA', 'QATAR'], ['APAC']]).

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of column names in which the code
            should check if the cell values matches and thus, the row
            should be dropped.
            list_of_list_of_string_values: List of lists (data type) of
            string values that will be checked against the existing
            values in the dataframe to see if the rows should be
            dropped. We unfortunately have to use list of lists because
            JSON config does not allow us to represent 'set' data types
            in Python.s

        Returns:
            Dataframe with rows dropped (if matches were found).
        """
        if not (isinstance(list_of_col_names, list)
                and isinstance(list_of_list_of_string_values, list)):
            raise transform_errors.InputDataTypeError(
                f"List of column names and list of set "
                f"of string values must both be of list type.")

        if len(list_of_col_names) != len(list_of_list_of_string_values):
            raise transform_errors.InputDataLengthError(
                f"The length of the list of column names: {len(list_of_col_names)} "
                f"is NOT the same as the length of the set of string values: "
                f"{len(list_of_list_of_string_values)}.")

        for i, col_name in enumerate(list_of_col_names):
            df = df[~df[col_name].isin(list_of_list_of_string_values[i])]
        return df

    def rename_columns(self, df, old_to_new_cols_dict):
        """
        Rename column headers to new ones given a dictionary of
        old to new column names.
        REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html

        Args:
            df: Raw dataframe to transform.
            old_to_new_cols_dict: Dictionary of old to new column names.
            E.g., {'old_col_name':'new_col_name', 'ChannelNames':'Channel_Names'}

        Returns:
            Dataframe with column headers renamed.
        """
        return df.rename(columns=old_to_new_cols_dict)

    def capitalize_first_letter_of_each_word_in_columns(self,
                                                        df,
                                                        list_of_col_names):
        """
        This method will capitalize the first letter of every word
        in a given list of columns (list_of_col_names).
        For example, suppose we have these values for 'col1':
        ['Other social', 'Other Social', 'Female body cleansers',
        'Female Body cleansers'], this method will transform these
        values into this - ['Other Social', 'Other Social',
        'Female Body Cleansers', 'Female Body Cleansers'].

        Args:
            df: Raw dataframe to capitalize the beginning of each word.
            list_of_col_names:  List of column names in the dataframe
                                in which this code will look to capitalize
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
            df[col_name] = df[col_name].apply(lambda s: self._cap_sentence(s))

        return df

    def capitalize_all_letters_of_each_word_in_columns(self,
                                                       df,
                                                       list_of_col_names):
        """
        This method will capitalize all letters of each word in a given
        list of columns (list_of_col_names). This method is basically a modified
        version of "capitalize_first_letter_of_each_word_in_columns"
        to capitalize every letter in each word.

        For example, suppose we have these values for 'col1':
        ['Other social', 'Other Social', 'Female body cleansers',
        'Female Body cleansers'], this method will transform these
        values into one of these values -
        ['OTHER SOCIAL', 'FEMALE BODY CLEANSERS'].

        Args:
            df: Raw dataframe to capitalize the words.
            list_of_col_names:  List of column names in the dataframe
                                in which this code will look to capitalize
                                each word.
        Returns:
            Dataframe with the column values (for each of the columns in
            list_of_col_names) where each word is capitalized.
        """
        if not isinstance(list_of_col_names, list):
            raise transform_errors.InputDataTypeError("List of column names must "
                                                      "be of list type with individual "
                                                      "names being string values.")
        for col_name in list_of_col_names:
            df[col_name] = df[col_name].apply(lambda s: s.upper())

        return df

    def sum_column_data_by_group_by(
            self,
            df,
            group_by_cols,
            target_col_names,
            label_to_assign_for_non_aggregated_cols
    ):
        """
        Function to sum target column values by group_by_cols and
        assign a given label to columns that are not part of the
        group_by_cols.

        For example, if we are to sum budget values by year and
        region, we can use this function as:
        sum_column_data_by_group_by(df, ['Year', 'Region'],
        'Budget', 'Total_Budget_By_Year_And_Region').

        Args:
            df: Dataframe to sum.
            group_by_cols: Columns to be included as Group By in the summation.
            target_col_names: The target columns that will summed using Group By.
            label_to_assign_for_non_aggregated_cols: The label (string) that
            will be assigned to columns that are not part of the Group By columns.

        Returns:
            Dataframe with values that now includes aggregated (summed) values
            using Group By.
        """
        df_grouped_and_summed = df.groupby(group_by_cols)[target_col_names] \
            .sum().reset_index()
        df = pd.concat([df, df_grouped_and_summed], sort=False) \
            .fillna(label_to_assign_for_non_aggregated_cols) \
            .sort_values(by=group_by_cols).reset_index(drop=True)

        return df

    def append_characters_in_front_of_column_value(
            self,
            df,
            list_of_col_names,
            chars_to_add_in_front):
        """
        If we need to add some character(s) in front of the
        values of some columns, use this function.

        For example, if we want to add 'WVM_' in front of
        Category and Subcategory columns, we use this function
        as below:
        append_characters_in_front_of_column_value(df,
        ['Category', 'Subcategory'], 'WVM_')
        """
        if not isinstance(list_of_col_names, list):
            raise transform_errors.InputDataTypeError("List of column names must "
                                                      "be of list type with individual "
                                                      "names being string values.")
        for col_name in list_of_col_names:
            df[col_name] = chars_to_add_in_front + df[col_name]

        return df

    def update_str_values_in_columns(self,
                                     df,
                                     list_of_col_names,
                                     list_of_dictionary_of_value_mappings):
        """
        Given a dataframe, list of columns and corresponding list of dictionaries
        representing old-to-new-value mappings for each column, apply the provided
        mappings to each column.

        For example, if we want 'Ecommerce' and 'Amazon' values in 'col1' of the
        dataframe to be updated to 'E-Commerce', we would call this method like this:
        update_str_values_in_columns(df, ["col1"],
        [{"Ecommerce": "E-Commerce", "Amazon": "E-Commerce"}]).
        REF: https://stackoverflow.com/a/20250996

        **Note that if any of the columns holds non-string type data,
        this method will NOT work as intended because in JSON config file
        we can only use string as keys. To update non-string values in
        columns, please use another method for specific data type such as
        'update_int_values_in_columns_to_str_values'.

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
            Dataframe with updated values based on the provided arguments.
        """
        if not (isinstance(list_of_col_names, list) and
                isinstance(list_of_dictionary_of_value_mappings, list)):
            raise transform_errors.InputDataTypeError("List of column names and list of "
                                                      "dictionary of value mappings must "
                                                      "be of type 'list'.")

        if len(list_of_col_names) != len(list_of_dictionary_of_value_mappings):
            raise transform_errors.InputDataLengthError(
                f"The length of column list: {len(list_of_col_names)} "
                f"is NOT the same as the length of the list of dictionaries "
                f"of update values: {len(list_of_dictionary_of_value_mappings)}")

        for i, col in enumerate(list_of_col_names):
            df[col] = df[col].map(list_of_dictionary_of_value_mappings[i]).fillna(df[col])

        return df

    def update_int_values_in_columns_to_str_values(self,
                                                   df,
                                                   list_of_col_names,
                                                   list_of_dictionary_of_value_mappings):
        """
        Sometimes, we need to convert integer values in certain columns
        to string values. For example, if we don't have full year data
        for 2020 in 'Year' column, and thus, we must replace 2020 (integer
        value) with '2020 YTD'. This is the method to accomplish that.
        REF: https://stackoverflow.com/a/17950531/1330974

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of columns to update values at.
            list_of_dictionary_of_value_mappings: List of dictionaries, each of them
            representing original values and desired (updated) values.
            E.g., if we want '2019' and '2020' to be mapped to '2019 LE'
            and '2020 YTD' respectively, we should provide
            [{"2019": "2019 LE", "2020": "2020 YTD"}]

        Returns:
            Dataframe with updated values based on the provided arguments.
            Note that this modified dataframe will have string columns
            instead of original integer columns.
        """
        if len(list_of_col_names) != len(list_of_dictionary_of_value_mappings):
            raise transform_errors.InputDataLengthError(
                f"The length of column list: {len(list_of_col_names)} "
                f"is NOT the same as the length of the list of dictionaries "
                f"of update values: {len(list_of_dictionary_of_value_mappings)}")

        for i, col in enumerate(list_of_col_names):
            # first, convert the data type of the column to string
            df[col] = df[col].apply(str)
            df[col] = df[col].map(list_of_dictionary_of_value_mappings[i]).fillna(df[col])

        return df

    def update_str_values_in_col2_based_on_col1_values(self,
                                                       df,
                                                       base_column_name,
                                                       target_column_name,
                                                       dictionary_of_value_pairs):
        """
        Given a dataframe, two column names (col1 and col2) and a dictionary
        representing col1-values-to-new-col2-values mappings, apply the mappings.

        E.g., whenever we see 'Ecommerce' or 'Amazon' in column named, 'Channel',
        we want to update values in 'Macro Channel' column to 'E-Commerce'.
        In this case, we provide following args to this method:
        update_str_values_in_col2_based_on_col1_values(df, "Channel", "Macro Channel",
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

    def update_str_values_in_col2_if_col1_has_one_of_given_values(self,
                                                                  df,
                                                                  col1_name,
                                                                  col2_name,
                                                                  list_of_values_in_col1,
                                                                  final_val_in_col2):
        """
        Update the string value column 2 to 'final_val_in_col1'
        if column 1's value is one of the items in the given
        list_of_values_in_col1.

        E.g., Whenever value in Market column is ' AFRICA-EURASIA', ' EUROPE',
        or ' HILLS', we want to update Brand column to " All Brands". Then,
        update_str_values_in_col2_if_col1_has_one_of_given_values(df, "Market", "Brand",
        [" AFRICA-EURASIA", " EUROPE", " HILLS" ], " All Brands")

        REF: How to use isin() in pandas
        https://archive.st/7804
        http://archive.ph/pZWv6

        Args:
            df: Raw dataframe to transform.
            col1_name: Name of the column in which we will try to match the
            values against.
            col2_name: Name of the column whose value we will update.
            list_of_values_in_col1: If one of the values in this list of values
            matches what's in col1, then we'll update the value in col2.
            final_val_in_col1: We will update the value of col2 to this value.

        Returns:
            Dataframe with updated values based on provided arguments.
        """
        if not (isinstance(col1_name, str) and isinstance(col2_name, str)):
            raise transform_errors.InputDataTypeError("Column names must be of string "
                                                      "type.")

        if not isinstance(final_val_in_col2, str):
            raise transform_errors.InputDataTypeError("The final value for col2_name"
                                                      " must be a string.")

        if not isinstance(list_of_values_in_col1, list):
            raise transform_errors.InputDataTypeError("list_of_values_in_col1 must "
                                                      "be of list type with individual "
                                                      "names being string values.")

        df.loc[df[col1_name].isin(list_of_values_in_col1), col2_name] = final_val_in_col2

        return df

    def update_order_of_columns_in_dataframe(self,
                                             df,
                                             list_reordered_col_headers):
        """
        Updates the ordering of existing columns in the dataframe.
        In addition to reordering columns, this method can be used
        to exclude columns in the final dataframe.

        For example, if the existing order of column headeres in the dataframe is:
        ["Col3", "Col1", "Col2"], we can  rearrange ordering of columns
        in the dataframe as below:
        update_order_of_columns_in_dataframe(df, ["Col1", "Col2", "Col3"])

        Args:
            df: Raw dataframe to transform.
            list_reordered_col_headers: List of column header names
            in the order they are supposed to be reordered.

        Returns:
            The dataframe with newly added column with fixed string values.
        """
        if not isinstance(list_reordered_col_headers, list):
            raise transform_errors.InputDataTypeError("list_reordered_col_headers must "
                                                      "be of list type with individual "
                                                      "names being string values.")

        df = df[list_reordered_col_headers]

        return df

    def update_decimal_places_in_columns(self,
                                         df,
                                         list_of_col_names,
                                         number_of_decimal_places_to_round):
        """
        Updates the decimal places of given columns to certain number.

        For example, if we want to round up to 2 decimal places for
        currency related columns such as 'Gross_Spend' and 'Net_Spend',
        we can call this function as below:
        update_decimal_places_in_columns(df, ['Gross_spend','Net_Spend'], 2)

        Args:
            df: Raw dataframe to transform.
            list_of_col_names: List of column names to apply this the
            decimal place rounding.
            number_of_decimal_places_to_round: Number of decimal places to
            round to.

        Returns:
            The dataframe with given columns rounded to specified decimal places.
        """
        if not isinstance(list_of_col_names, list):
            raise transform_errors.InputDataTypeError("list_of_col_names must "
                                                      "be of list type with individual "
                                                      "column names being string values.")

        if not isinstance(number_of_decimal_places_to_round, int):
            raise transform_errors.InputDataTypeError("Value for number of decimal places "
                                                      "must be of integer type.")

        # REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.round.html
        return df.round({col: number_of_decimal_places_to_round for col in list_of_col_names})

    def update_na_values_with_empty_str_values(self,
                                               df,
                                               list_of_col_names):
        """
        Replace NaN values with empty string.
        An example use of this method would be when we load a file that has
        "NA" as values in some of its cells, but when Pandas read the file
        with keep_default_na = True (which is default), then it will load
        these values as pd.np.nan (i.e. NaN values). In instances like that,
        we must use this method to replace these NaN values with empty string.
        REF: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html

        Args:
            df: Raw dataframe.
            list_of_col_names: List of column names (each is of string type)
            in which we should look for NaN/NULL values to replace with
            empty strings.

        Returns:
            The dataframe whose NaN values are replaced with empty string.
        """
        df[list_of_col_names] = df[list_of_col_names].fillna('')

        return df

    def copy_value_from_row_above_to_empty_rows_below(self,
                                                      df,
                                                      list_of_col_names):
        """
        Copy value from row directly above to the row below if the row below
        is empty (meaning it has empty string value).
        REF 1: https://stackoverflow.com/a/41213232/1330974
        REF 2: https://stackoverflow.com/a/56132709/1330974

        Args:
            df: Raw dataframe.
            list_of_col_names: List of column names that we must
            copy the value from above row whenever we see a cell
            with empty string value.

        Returns:
            The dataframe with columns whose empty string values
            are now populated with what's in the row directly above.
        """
        if not isinstance(list_of_col_names, list):
            raise transform_errors.InputDataTypeError("list_of_col_names must "
                                                      "be of list type with individual "
                                                      "column names being string values.")

        for col_name in list_of_col_names:
            df[col_name] = df[col_name].replace('', np.NaN).ffill()

        return df

    def copy_col1_value_to_col2_if_col2_has_specific_value(self,
                                                           df,
                                                           col1_name,
                                                           col2_name,
                                                           col2_value):
        """
        Copy value from column 1 to column 2 if **column 2** (not column 1)
        has provided value.
        For example, if we want to copy values from region (division) column
        to market (country) whenever region column has value equal to 'Total',
        we can call this function with parameters like this:
        copy_col1_value_to_col2_if_col2_has_specific_value(df, 'region', 'market', 'Total')
        REF: https://stackoverflow.com/a/51039824

        Args:
            df: Raw dataframe to transform.
            col1_name: Column name **from** which the value will be copied.
            col2_name: Column name **to** which to value will be copied.
            col2_value: Column 2's value which will be used as a condition
            to decide if we should copy column 1's value to column 2.

        Returns:
            Dataframe with updated values based on the provided arguments.
        """
        if not (isinstance(col1_name, str) and isinstance(col2_name, str)
                and isinstance(col2_value, str)):
            raise transform_errors.InputDataTypeError("Column names and values "
                                                      "must be of string type")

        df.loc[df[col2_name] == col2_value, col2_name] = df[col1_name]

        return df

    def strip_extra_spaces_and_newline_characters_in_column_names(
            self,
            df
    ):
        """
        Strips the extra spaces (before and after) and/or the newline
        characters (\n) that surrounds the beginning and the end of
        the column names.

        For example, Russia data usually comes with column names like:
        ' Advertisers', ' COUNTRY ', "Subcategories\n". We can use
        this method to transform these column names to the followings:
        'Advertisers', 'COUNTRY', 'Subcategories'.
        """
        return df.rename(columns=lambda x: x.strip())

    def add_new_column_with_fixed_str_value(self,
                                            df,
                                            new_col_name,
                                            fixed_str_value):
        """
        Creates a new column with constant string values.

        For example, if we want to add 'Region' column in the dataframe
        with values 'AED', we will call this function like below:
        add_new_column_with_fixed_str_value(df, 'Region', 'AED')

        Args:
            df: Raw dataframe to transform.
            new_col_name: Name of the new column to be added.
            fixed_str_value: Value (string type) of each cell in the newly added column.

        Returns:
            The dataframe with newly added column with fixed string values.
        """
        if not (isinstance(new_col_name, str) and isinstance(fixed_str_value, str)):
            raise transform_errors.InputDataTypeError("Column names and fixed_str_value "
                                                      "must be of string type")

        df[new_col_name] = fixed_str_value

        return df

    def add_new_column_by_copying_values_from_another_column(
            self,
            df,
            list_of_existing_col_names,
            list_of_new_col_names):
        """
        Creates new columns by copying the existing columns values.
        In other words, copy values from one column to create another
        column with a different name.

        For example, if we want to add 'Harmonized_Region' column
        in the dataframe by copying all the values from raw column
        named 'Region', we can call this method like:
        add_new_column_by_copying_values_from_another_column(
        df, ['Region'], ['Harmonized_Region'])

        Args:
            df: Raw dataframe to transform.
            list_of_existing_col_names: List of original column names
            that we want to copy the data from.
            list_of_new_col_names: List of corresponding new column
            names to which we should copy the data to.

        Returns:
            The dataframe with newly added column(s) which has exactly
            the same data copied from original column(s).
        """
        if not (isinstance(list_of_existing_col_names, list)
                and isinstance(list_of_new_col_names, list)):
            raise transform_errors.InputDataTypeError(
                f"List of existing and new column names must be "
                f"of list type.")

        if len(list_of_existing_col_names) != len(list_of_new_col_names):
            raise transform_errors.InputDataLengthError(
                f"The length of existing column list: "
                f"{len(list_of_existing_col_names)} "
                f"is NOT the same as the length of new column "
                f"name list: {len(list_of_new_col_names)}")

        for i, new_col_name in enumerate(list_of_new_col_names):
            df[new_col_name] = df[list_of_existing_col_names[i]]

        return df

    def add_new_column_with_values_based_on_another_column_values_using_regex_match(
            self,
            df,
            existing_col_name,
            new_col_name,
            dictionary_of_mappings):
        """
        Creates a new column with values based on the dictionary of
        mappings in which keys represent **REGULAR EXPRESSION** values
        in existing column and values represent values in the new column.
        Whenever the regular expression key matches the value in the
        existing column, the new column will be assigned corresponding
        value from the dictionary.

        **If regular expression does NOT match the value in the existing
        column, original value from the existing column will be copied
        to the new column.**

        Suppose we want to create a new column named "Harmonized_Advertiser"
        based on "Advertiser" column. When we see "L'OREAL PARIS",
        "L'oreal Paris" and "l'oreal" in 'Advertiser' column, we want to
        assign in the value "LOREAL" in 'Harmonized_Advertiser' column.
        Then we can call this method with parameters like this:
        add_new_column_with_values_based_on_another_column_values_using_regex_match(
        df, "Advertiser", "Harmonized_Advertiser", {"(i?)l\'oreal.*": "LOREAL"}).

        For Python Regular Expression Syntax,
        REF 1: https://docs.python.org/3/library/re.html

        How to use regular expression in Pandas's replace method:
        REF 2: https://stackoverflow.com/a/54464222/1330974
        REF 3: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html

        Args:
            df: Raw dataframe to transform.
            existing_col_name: Name of the column which already exist in
            the dataframe and the one we should use as reference in creating
            the new column.
            new_col_name: Name of the new column to be created.
            dictionary_of_mappings: Dictionary representing key-value pairs
            in which keys represent **regular expression** values to look for
            in existing column and values representing the ones to be assigned
            in the new column.

        Returns:
            The dataframe with the new column attached with values either from
            the value of the dictionary or the corresponding value from the existing
            column.
        """
        if not (isinstance(new_col_name, str) and isinstance(existing_col_name, str)):
            raise transform_errors.InputDataTypeError("Column names must be of string type")

        if not isinstance(dictionary_of_mappings, dict):
            raise transform_errors.InputDataTypeError(
                "Mapping key-value pairs must be of dictionary type with keys representing "
                "the regular expressions and values the desired final string values for the "
                "new column.")

        df[new_col_name] = df[existing_col_name].replace(regex=dictionary_of_mappings)

        return df

    def add_new_column_with_values_based_on_another_column_values_using_exact_str_match(
            self,
            df,
            existing_col_name,
            new_col_name,
            dictionary_of_mappings,
            use_existing_col_values=False):
        """
        Creates a new column with values based on the dictionary of
        mappings in which keys represent values in existing column
        and values represent values in the new column. Whenever the key
        **EXACTLY** matches the value in the existing column, the new
        column will be assigned corresponding value from the dictionary.

        NOTE: If we want to use/borrow existing column's value when
        there is no direct mapping available (i.e. mapping is not
        defined/provided), then set 'use_existing_col_values'
        parameter to True. Otherwise, default is to leave the
        cells (without defined mapping) blank/empty.

        For example, we have a column named 'Channel' in our original
        dataframe with values "GDN Display", "GDN Video" and "YouTube".
        We want to create a new column named "NewChannelNames" and in that
        column, whenever we see "GDN Display" in 'Channel' column, we want to
        enter "Display"; when we see "GDN Video" in 'Channel' column, we want
        to enter "Online Video"; when we see "YouTube" in 'Channel' column,
        we want to enter "Online Video" in the new column, we call this method
        with parameters like this:
        add_new_column_with_values_based_on_another_column_values_using_exact_str_match(
        df, "Channel", "NewChannelNames", {"GDN Display": "Display",
        "GDN Video": "Online Video", "YouTube": "Online Video"}).

        As another example, if we want to created a harmonized category
        name column by using existing/raw category column values such as
        'HOME CARE' and 'ORAL CARE', but we want to copy the values from
        existing column if unexpected value occurs in the raw data, then
        we call this function like below:
        add_new_column_with_values_based_on_another_column_values_using_exact_str_match(
        df, "Category", "Harmonized_Category", {"HOME CARE": "Home Care",
        "ORAL CARE": "Oral Care"}).
        In the above method call, if there is a value, say, "Personal Care",
        then the new column will have corresponding value "Personal Care".

        REF: https://stackoverflow.com/a/24216489

        Args:
            df: Raw dataframe to transform.
            existing_col_name: Name of the column which already exist in
            the dataframe and the one we should use as reference in creating
            the new column.
            new_col_name: Name of the new column to be created.
            dictionary_of_mappings: Dictionary representing key-value pairs
            in which keys representing the values from the existing column
            and values representing the ones to be assigned to the new column.
            use_existing_col_values: Set this to True if the existing
            column's value must be copied when there's no mapping defined.
            Default is False.

        Returns:
            The dataframe with new column attached which has values in the
            mapping provided.
        """
        if not (isinstance(new_col_name, str) and isinstance(existing_col_name, str)):
            raise transform_errors.InputDataTypeError("Column names must be of string type")

        if not isinstance(dictionary_of_mappings, dict):
            raise transform_errors.InputDataTypeError(
                "Mapping key-value pairs must be of dictionary type")

        if use_existing_col_values:
            df[new_col_name] = df[existing_col_name].replace(dictionary_of_mappings)
        else:
            df[new_col_name] = df[existing_col_name].map(dictionary_of_mappings)

        return df

    def add_year_column_with_fixed_int_value(self,
                                             df,
                                             year_int_value=None,
                                             new_year_col_name='YEAR'
                                             ):
        """
        Creates a new column for YEAR column with integer value provided as parameter.

        For example, if we want to add YEAR column with current year
        as value, we call this method like below:
        create_new_column_with_fixed_str_value(df)

        If we want to use specific year value and custom column name for year,
        we can call the method like below:
        add_year_column_with_fixed_int_value(df, 'YYYY', 2019)

        Args:
            df: Raw dataframe to transform.
            year_int_value: (Optional) If we want to assign custom year value instead
            of the current year (which is default), we can pass in an integer for this
            parameter.
            new_year_col_name: Column name for new year column. Default is 'YEAR'.

        Returns:
            The dataframe with newly added YEAR column with integer year value.
        """
        if not isinstance(new_year_col_name, str):
            raise transform_errors.InputDataTypeError("Column name for new year column "
                                                      "must be string type.")
        if year_int_value is not None:
            if not isinstance(year_int_value, int):
                raise transform_errors.InputDataTypeError("Year value must be integer type.")
            df[new_year_col_name] = year_int_value
        else:
            now = datetime.datetime.now()
            df[new_year_col_name] = now.year

        return df

    def add_year_column_using_existing_column_with_year_values(
            self,
            df,
            existing_date_col_name,
            new_date_col_name='YEAR'):
        """
        Creates a new column for YEAR column by extract year
        information from an existing column in the dataframe.
        The existing column's year data can be in varying format
        like this: 'Apr - 2020' (India); '1/1/2020' (Kenya)'
        and this function will correctly extract the year value.

        For example, if we want to add 'YEAR' column by using
        the date string column in the dataframe called 'YEAR_MONTH',
        we call this method like below:
        add_year_column_using_existing_string_column_with_string_values(
        df, 'YEAR_MONTH')

        Args:
            df: Raw dataframe to transform.
            existing_date_col_name: Column name in the dataframe
            that has date data from which this code will infer
            the YEAR information from.
            new_year_col_name: Column name for the new year column.
            Default is 'YEAR'.

        Returns:
            The dataframe with newly added YEAR column with integer year value.
        """
        df[new_date_col_name] = pd.to_datetime(df[existing_date_col_name]).dt.year

        return df

    def add_month_column_using_existing_column_with_month_values(
            self,
            df,
            existing_date_col_name,
            new_date_col_name='MONTH'):
        """
        Creates a new column for MONTH column by inferring from
        the existing date string column in the dataframe.

        For example, if we want to add 'MONTH' column by using
        the date string column in the dataframe called 'YEAR_MONTH',
        we call this method like below:
        add_month_column_using_existing_date_column_with_3_first_month_letters_values(
        df, 'YEAR_MONTH')

        Args:
            df: Raw dataframe to transform.
            existing_date_col_name: Column name in the dataframe
            that has date data from which this code will infer
            the MONTH information from.
            new_year_col_name: Column name for the new year column.
            Default is 'MONTH'.

        Returns:
            The dataframe with newly added YEAR column with integer year value.
        """
        df[new_date_col_name] = pd.to_datetime(df[existing_date_col_name]).dt.month

        return df

    def add_integer_month_column_using_existing_month_col_with_full_month_names(
            self,
            df,
            existing_month_col_name_with_full_month_names,
            new_month_col_name='MONTH'):
        """
        Creates a new column for integer MONTH values using **data from an existing
        month column which has full month name (such as 'January', 'February',
        etc.)**.

        For example, if we want to add a new integer month column named 'MM' using
        an existing month column named 'Existing_Month' which has full month's names,
        we will call this method like below:
        add_integer_month_column_using_existing_month_col_with_full_month_names(df,
        'MM', 'Existing_Month')

        Args:
            df: Raw dataframe to transform.
            existing_col_name_with_full_month_names: Column name in the raw dataframe
            that will be used as reference to assign integer month values in the new
            month column.
            new_month_col_name: (Optional) If we want to assign custom name for the
            new month column, provide the new month column name (string type) using
            this parameter. Otherwise, the default new month column name is 'MONTH'.

        Returns:
            The dataframe with newly added MONTH column with integer month value.
        """
        if not (isinstance(existing_month_col_name_with_full_month_names, str)
                and isinstance(new_month_col_name, str)):
            raise transform_errors.InputDataTypeError("Parameters for existing month column "
                                                      "name and new month column name must be "
                                                      "of string type.")
        df[new_month_col_name] = df[existing_month_col_name_with_full_month_names].map(
            lambda x: datetime.datetime.strptime(x, '%B').month)

        return df

    def add_date_column_using_existing_year_and_month_columns_with_integer_values(
            self,
            df,
            existing_year_col_name_with_integer_year_values,
            existing_month_col_name_with_integer_month_values,
            new_date_col_name='DATE'):
        """
        Creates a new column for date with date data type values using
        the **data from existing month and year columns both of which
        have integer values representing Years and Months in them**.

        For example, if we want to add a new date column named 'DatePurchased'
        using an existing year column named 'Existing_Year', which has integer
        year values (2018, 2019, etc.) for Year and an existing month column
        named 'Existing_Month', which also has integer month values (such as
        1 for 'January'; 2 for 'February'), we will call this method like
        below:
        add_date_column_using_existing_year_and_month_columns_with_integer_values(
        df, 'Existing_Year', 'Existing_Month', 'DatePurchased')

        Args:
            df: Raw dataframe to transform.
            existing_year_col_name_with_integer_year_values: Column name
            with integer Year values in the raw dataframe that will be
            used as reference to create date values in the new date column.
            existing_month_col_name_with_integer_year_values: Column name
            with integer Month values in the raw dataframe that will be
            used as reference to create date values in the new date column.
            new_date_col_name: (Optional) If we want to assign custom name for the
            new month column, provide the new month column name (string type) using
            this parameter. Otherwise, the default new month column name is 'DATE'.

        Returns:
            The dataframe with newly added DATE column with values of date data type.
        """
        if not (isinstance(existing_year_col_name_with_integer_year_values, str)
                and isinstance(existing_month_col_name_with_integer_month_values, str)
                and isinstance(new_date_col_name, str)):
            raise transform_errors.InputDataTypeError("Parameters for existing year column "
                                                      "name, new month column name and new "
                                                      "date column name must be of "
                                                      "string type.")

        # REF: https://stackoverflow.com/a/37103131
        df[new_date_col_name] = pd.to_datetime(
            dict(year=df[existing_year_col_name_with_integer_year_values],
                 month=df[existing_month_col_name_with_integer_month_values],
                 day=1)
        )

        return df

    def add_date_column_with_current_date(self,
                                          df,
                                          new_date_col_name='PROCESSED_DATE'):
        """
        Creates a new column with date data type values.

        For example, if we want to add a new date column named 'CURRENT_DATE',
        we will call this method like below:
        add_date_column_with_current_date(df, 'CURRENT_DATE')

        Args:
            df: Raw dataframe to transform.
            new_date_col_name: (Optional) If we want to assign custom name for the
            new date column, provide new column name (string type) using
            this parameter. Otherwise, the default column name is
            'DATA_PROCESSED_DATE'.

        Returns:
            The dataframe with PROCESSED_DATE (or any other custom
            column name provided as parameter) column that has
            with current date values (of date type).
        """
        if not isinstance(new_date_col_name, str):
            raise transform_errors.InputDataTypeError("New date column name must "
                                                      "be of string type.")
        # REF: https://stackoverflow.com/a/37103131
        df[new_date_col_name] = pd.to_datetime(datetime.datetime.now().date())

        return df

    def remove_string_values_in_column(
            self,
            df,
            col_name,
            regex_pattern_of_string_to_remove):
        """
        This function will remove string_value (based on the REGEX pattern
        provided as input parameter) found in a given column.
        For example, if we want to delete comma values (',') in spend column
        we can call this function like below:
        remove_string_values_in_column(df, 'Gross Spend', ',')
        If we want to use REGEX, we will provide the pattern as the
        input parameter like below:
        remove_string_values_in_column(df, 'Category', '^Cleaning')
        Args:
            df: Raw dataframe to transform.
            col_name: Name of the column in which the function
            will look for the string value to remove.
            regex_pattern_of_string_to_remove: REGEX pattern which
            will be used to find the string to remove.

        Returns:
            Dataframe with rows without the string value (if matches are found).
        """
        df[col_name] = df[col_name].str.replace(regex_pattern_of_string_to_remove, "", regex = True)

        return df

    def remove_dollar_sign(self):
        """
        Remove the dollar sign given a data frame.
        :return:
        """
        pass
