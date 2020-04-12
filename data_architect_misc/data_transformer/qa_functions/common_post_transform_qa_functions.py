"""
Include this python file in the common_post_transform_qa_config.json
file with the key like this:
"custom_transform_functions_file": "./transform_functions/common_post_transform_qa_functions.py",

and run the transform.py like this:
>> python transform.py

Author: Phyo Thiha
Last Modified: April 10, 2020
"""
import logging
import re

import pandas as pd

import qa_errors


class CustomFunctions:
    """
    This class is the collection of QA functions that must be run
    against the transformed data. The QA functions here will either
    give warnings or throw errors (if the impact is serious).
    """
    EXPECTED_COLUMNS = {
        "YEAR",
        "MONTH",
        "DATE",
        "PROCESSED_DATE",
        "HARMONIZED_REGION",
        "HARMONIZED_COUNTRY",
        "HARMONIZED_ADVERTISER",
        "HARMONIZED_MEDIA_TYPE",
        "CURRENCY",
        "GROSS_SPEND_IN_LOCAL_CURRENCY",
        "HARMONIZED_CATEGORY",
        "RAW_SUBCATEGORY",
        "RAW_BRAND",
        "RAW_SUBBRAND",
        "RAW_PRODUCT_NAME",
        "HARMONIZED_PRODUCT_NAME"
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_expected_columns(self, df) -> pd.DataFrame:
        """
        The transformed data must have at least the minimal set of
        columns that we expect for competitive harmonization project.
        """
        if set(self.EXPECTED_COLUMNS) - set(df.columns):
            self.logger.warning(
                f"QA => Missing these expected/standard columns in the "
                f"transformed data: {set(self.EXPECTED_COLUMNS) - set(df.columns)}")

        if set(df.columns) - set(self.EXPECTED_COLUMNS):
            self.logger.info(
                f"QA => Found these columns in transformed data that are not "
                f"part of the expected column set: "
                f"{set(df.columns) - set(self.EXPECTED_COLUMNS)}\n")

        return df

    def check_how_many_years_is_in_year_column(self, df) -> pd.DataFrame:
        # datetime.datetime.now().year
        return df

    def assert_number_of_columns_equals(self, df, num_of_cols_expected) -> pd.DataFrame:
        """
        Assert that the total number of columns in the dataframe
        is equal to num_of_cols_expected (int).

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
            raise qa_errors.ColumnCountError(
                f"Expected column count of: " \
                f"{num_of_cols_expected} but found: " \
                f"{df.shape[1]} in the current dataframe.")

        return df

    def assert_no_na_values_in_columns(self,
                                       df,
                                       list_of_col_names) -> pd.DataFrame:
        """
        Check if there is any NaN/Null/None values in the list of
        columns provided. If there is any, raise NaNFoundError.

        Args:
            df: Raw dataframe to check for Nan values.
            list_of_col_names: List of column names (each is of string type)
            in which we should look for NaN/NULL values.
            REF1: https://stackoverflow.com/a/42923089
            REF2: https://stackoverflow.com/a/27159258
            REF3: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.isnull.html

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            NaNFoundError: If there is any NaN/NULL value in the given list
            of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"\nQA => List of column names must "
                                                      f"be of list type with individual "
                                                      f"column names being string values.")

        if df[list_of_col_names].isnull().values.any():
            raise qa_errors.NaNFoundError(f"\nQA => NaN/None/NaT value is "
                                                 f"found in one of these columns: "
                                                 f"{list_of_col_names}")
        # self.logger.info(f"QA => Successfully confirmed that there is no NA/NULL/empty "
        #                  f"value in these columns: {str(list_of_col_names)}")

        return df

    def assert_no_empty_str_values_in_columns(self,
                                              df,
                                              list_of_col_names) -> pd.DataFrame:
        """
        Check if there is any empty string values in the list of
        columns provided. If there is any, raise EmptyStringFoundError.

        Args:
            df: Raw dataframe to check for empty string values.
            list_of_col_names: List of column names (each is of string type)
            in which we should look for empty string values.
            REF1: https://stackoverflow.com/a/52843708

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            EmptyStringFoundError: If there is any empty string value
            in the given list of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"\nQA => List of column names must "
                                                      f"be of list type with individual "
                                                      f"column names being string values.")

        cols_with_empty_str = []
        for col_name in list_of_col_names:
            if df[df[col_name] == ''].index.any():
                cols_with_empty_str.append(col_name)

        if cols_with_empty_str:
            raise qa_errors.EmptyStringFoundError(
                f"\nQA => Empty string value found in these column(s): "
                f"{cols_with_empty_str}")

        return df

    def assert_no_less_than_values_in_columns(self,
                                              df,
                                              threshold_value,
                                              list_of_col_names) -> pd.DataFrame:
        """
        Check if there is any value which is less than the threshold_value
        in the list of columns provided.
        If there is any, raise LessThanThresholdValueFoundError.

        Args:
            df: Raw dataframe to check for values less than the threshold values.
            threshold_value: Value to compare against individual values in
            the dataframe's columns.
            list_of_col_names: List of column names (each is of string type)
            whose values we should compare against the threshold value.

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            LessThanThresholdValueFoundError: If there is any empty string value
            in the given list of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"\nQA => List of column names must "
                                                      "be of list type with individual "
                                                      "column names being string values.")

        for col_name in list_of_col_names:
            if any(df[col_name] < threshold_value):
                raise qa_errors.LessThanThresholdValueFoundError(
                    f"\nQA => Value(s) less than this threshold value: "
                    f"{threshold_value}\nfound in this column: {col_name}")

        return df


    def check_possible_duplicates_in_columns(self,
                                             df,
                                             list_of_col_names) -> pd.DataFrame:
        """
        This method will check if any of the given list of columns
        has duplicate values in it. It will do so by first
        turning all letters of each value in individual column to small case.
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
            list_of_col_names: List of column names in which
             the code will look for duplicates.

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
                raise qa_errors.PossibleDuplicateError(err_msg)

        return df