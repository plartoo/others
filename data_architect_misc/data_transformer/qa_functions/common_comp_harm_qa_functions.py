"""
Include this python file in the common_comp_harm_post_transform_qa_config.json
file with the key like this:
"custom_transform_functions_file": "./transform_functions/common_comp_harm_qa_functions.py",

and run the transform.py like this:
>> python transform.py

Author: Phyo Thiha
Last Modified: July 29, 2020
"""
import datetime
import logging
import re

import pandas as pd

import transform_errors
from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE
from qa_functions import qa_errors
from transform_errors import OrderOfListContentsDifferentError, ExpectedColumnNotFoundError


class CommonCompHarmQAFunctions:
    """
    This class is the collection of QA functions that must be run
    against the transformed data. The QA functions here will either
    give warnings or throw errors (if the impact is serious).

    Note: This class is named 'CustomFunctions' instead of
    'CustomQAFunctions' because the way we load custom function
    modules (in transform_utils.py) is expecting a class named,
    'CustomFunctions' if any custom function file is provided.

    Technically, we can create a 'CustomQAFunctions' class first
    and then have 'CustomFunctions' class inherit the former
    in this module. That is, create
    class CustomFunctions(CustomQAFunctions).

    But I personally don't like creating multiple-layered
    classes just because it follows OOP best practices.
    As a result, I have decided not inherit 'CustomFunctions' from
    'CustomQAFunctions'.
    """

    # the earliest year we started collecting data for comp. harm project
    MIN_YEAR = 2015
    MIN_MONTH = 1
    MAX_MONTH = 12
    # one billion is already quite big for a spend line item in comp. harm project
    MAX_SPEND = 1000000000
    ESSENTIAL_COLUMNS = [
        comp_harm_constants.YEAR_COLUMN,
        comp_harm_constants.MONTH_COLUMN,
        comp_harm_constants.DATE_COLUMN,
        comp_harm_constants.REGION_COLUMN,
        comp_harm_constants.COUNTRY_COLUMN,
        comp_harm_constants.ADVERTISER_COLUMN,
        comp_harm_constants.MEDIA_TYPE_COLUMN,
        comp_harm_constants.CATEGORY_COLUMN,
        comp_harm_constants.GROSS_SPEND_COLUMN
    ]

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def extract_date_range_string_from_file_path_and_name(file_path_and_name):
        # If this method is returning 'IndexError: list index out of range'
        # error, that means no match is found and you need to inspect your
        # file name to make sure it has date range pattern like this:
        # '*_YYYYMMDD_YYYYMMDD*rows', which is specific to comp harm project.
        return re.findall(r'_(\d{8}_\d{8}).*rows', file_path_and_name)[0]

    @staticmethod
    def extract_date_ranges_from_file_path_and_name(file_path_and_name):
        """
        Extract datetime objects from the date range string in the
        form of YYYYMMDD_YYYYMMDD and returns two datetime objects in
        a tuple.
        """
        date_range_str = CommonCompHarmQAFunctions.extract_date_range_string_from_file_path_and_name(
            file_path_and_name
        )
        return [datetime.datetime.strptime(d_str, '%Y%m%d') for d_str in date_range_str.split('_')]

    @staticmethod
    def has_same_date_range_in_their_names(
            file1_path_and_name,
            file2_path_and_name):
        # This method extracts date range of the data from the file names
        # assuming that the file names are given following the standards
        # used in comp_harm project ('*_YYYYMMDD_YYYYMMDD*rows'), and
        # compare them. Based on the comparison, it returns boolean value
        # if the date ranges in these file names match (or not).
        return CommonCompHarmQAFunctions.extract_date_range_string_from_file_path_and_name(file1_path_and_name) == \
               CommonCompHarmQAFunctions.extract_date_range_string_from_file_path_and_name(file2_path_and_name)

    def assert_date_range_in_file_name_is_the_same_as_what_is_in_the_data(self, df):
        d_start, d_end = CommonCompHarmQAFunctions.extract_date_ranges_from_file_path_and_name(
            self.config[KEY_CURRENT_INPUT_FILE])
        max_yr_in_df = max(df[comp_harm_constants.YEAR_COLUMN])
        min_yr_in_df = min(df[comp_harm_constants.YEAR_COLUMN])
        max_month_in_df = max(df[comp_harm_constants.MONTH_COLUMN])
        min_month_in_df = min(df[comp_harm_constants.MONTH_COLUMN])
        if ((d_start.year != min_yr_in_df) or (d_start.month != min_month_in_df)
                or (d_end.year != max_yr_in_df) or (d_end.month != max_month_in_df)):
            raise transform_errors.InputFileNameAndDataDateRangeMismatchError(
                self.config[KEY_CURRENT_INPUT_FILE])
        return df

    @staticmethod
    def _is_contents_of_the_lists_are_in_same_order(list1, list2):
        for i, l1 in enumerate(list1):
            if l1 != list2[i]:
                return False
        return True

    def assert_the_order_of_sheets_is_as_expected(
            self,
            df,
            list_of_expected_sheet_order
    ):
        """
        There are times when we load data from Excel file
        with multiple sheets, we need to load the first
        sheet, and then load the remaining sheets with
        transform functions. In that scenario, we need
        to make sure that the input file never changes
        the order of these sheets without us knowing it
        (i.e. getting an error if the order of the
        sheets change in the input file.)

        For example, in Vietnam input files, we have three
        sheets ('Spots', 'Press' and 'Radio' in that order).
        In the JSON config, we specify the transform module
        to read just the first sheet and we assume it is
        always 'Spots' sheet. If, for some reason, the
        input file changes the order of these sheets,
        we need the user to know about it immediately and
        that's when this function must be used to raise
        the alarm to the user.
        """
        # Unfortunately, we have to read the file again
        # (with all the sheets at once) and save it in a
        # temp_df to detect the order of the sheets in it.
        # Here, we expect the user to be using Python 3.7+
        # for dictionary to respect (keep) the order of the keys.
        temp_df = pd.read_excel(
            self.config[KEY_CURRENT_INPUT_FILE],
            sheet_name=None)
        all_sheets = temp_df.keys()

        # First, filter out the sheets that we are not interested
        sheets_of_interest = [s for s in all_sheets if s in list_of_expected_sheet_order]

        if not CommonCompHarmQAFunctions._is_contents_of_the_lists_are_in_same_order(
                sheets_of_interest,
                list_of_expected_sheet_order
        ):
            raise OrderOfListContentsDifferentError(
                list_of_expected_sheet_order,
                sheets_of_interest)
        return df

    def check_expected_columns_are_present(self, df):
        """
        The transformed data must have at least the minimal set of
        columns that we expect for competitive harmonization project.
        """
        if set(comp_harm_constants.EXPECTED_COLUMNS) - set(df.columns):
            self.logger.warning(
                f"QA => Missing these expected/standard columns in the "
                f"transformed data: {set(comp_harm_constants.EXPECTED_COLUMNS) - set(df.columns)}")

        if set(df.columns) - set(comp_harm_constants.EXPECTED_COLUMNS):
            self.logger.info(
                f"QA => Found these columns in transformed data that are not "
                f"part of the expected column set: "
                f"{set(df.columns) - set(comp_harm_constants.EXPECTED_COLUMNS)}\n")

        return df

    def check_expected_columns_are_present_by_using_regex(
            self,
            df,
            regex_pattern_for_expected_col_name: str
    ):
        """
        This function will use regular expression to
        check and see if the expected column(s) is(are)
        present in the dataframe.

        For example, the guy who prepares raw data for us
        in India does NOT keep the cost column names consistent.
        So we need to always check and see if he sent us the
        actual cost column with expected name. Usually, we know
        that the actual cost column has words like 'Actual' and
        'Cost' together in it. So we will run this function
        for India data processing like this:
        check_expected_columns_are_present_by_using_regex(df,
        ['Actual.*Cost'].
        """
        expected_col_found = False
        for col_name in df.columns:
            if re.findall(regex_pattern_for_expected_col_name, col_name, re.IGNORECASE):
                expected_col_found = True

        if not expected_col_found:
            raise ExpectedColumnNotFoundError(
                f"The column with actual cost (which is usually named "
                f"with regex pattern '{regex_pattern_for_expected_col_name}' "
                f"is NOT found in the dataframe. "
                f"Please make sure to double check the input file "
                f"and update the config file to pick the right column "
                f"for spend values.")

        return df

    def assert_number_of_columns_equals(
            self,
            df,
            num_of_cols_expected
    ):
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
                f"Expected column count of: "
                f"{num_of_cols_expected} but found: "
                f"{df.shape[1]} in the current dataframe.")

        return df

    def check_distinct_year_values_in_year_column(self, df):
        """
        Display distinct year values in the transformed data.
        If there are more than one year (which is unusual for
        typical data file in competitive harmonization project),
        the WARNING log message will be used. Otherwise, INFO
        log message will be used.
        """
        years = sorted(df[comp_harm_constants.YEAR_COLUMN].unique())

        if len(years) > 1:
            self.logger.warning(f"QA => More than ONE year value is found: "
                                f"{years}"
                                f"\nMake sure this is expected for the data.")
        else:
            self.logger.info(f"QA => Year value found in the data: {years}")

        return df

    def assert_if_year_values_are_within_valid_range(self, df):
        """
        Checks if distinct year values found in the transformed
        data are within valid range. The valid range is between
        2015 (the year we started collecting data for competitive
        harmonization project) to the current year.
        """
        years = sorted(df[comp_harm_constants.YEAR_COLUMN].unique())
        cur_year = datetime.datetime.now().year

        if not all([(y >= self.MIN_YEAR) and (y <= cur_year) for y in years]):
            raise qa_errors.InvalidValueFoundError(
                f"Unexpected year found in the data. Please inspect the "
                f"following year values: {years} to make sure that none of "
                f"them are beyond the expected range and match what's in "
                f"the raw data."
            )
        return df

    def check_distinct_month_values_in_month_column(self, df):
        """
        Display distinct month values in the transformed data.
        If there are more than one month, the WARNING log
        message will be used. Otherwise, INFO log message
        will be used.
        """
        months = sorted(df[comp_harm_constants.MONTH_COLUMN].unique())

        if len(months) > 1:
            self.logger.warning(f"QA => More than ONE month value is found: "
                                f"{months}"
                                f"\nMake sure this is expected for the data.")
        else:
            self.logger.info(f"QA => Month value found in the data: {months}")

        return df

    def assert_if_month_values_are_within_valid_range(self, df):
        """
        Asserts if month values found in the transformed data
        are within the valid range (from 1 to 12). If not,
        raises InvalidValueFoundError.
        """
        months = sorted(df[comp_harm_constants.MONTH_COLUMN].unique())

        if not all([(y >= self.MIN_MONTH) and
                    (y <= self.MAX_MONTH) for y in months]):
            raise qa_errors.InvalidValueFoundError(
                f"Unexpected month value found in the data. Please inspect "
                f"the following month values: {months} to make sure that "
                f"none of these are beyond the expected range (1 to 12) "
                f"and match what's in the raw data."
            )

        return df

    def assert_if_date_values_matches_with_year_and_month_column_values(
            self,
            df):
        """
        Asserts that the year and month values in respective harmonized
        columns are the same as the ones in harmonized date column.

        REF: https://stackoverflow.com/a/25149272/1330974

        If year or month values don't match with what's in the date
        column, raise ValueComparisonError.
        """
        df_year_comparison = df.loc[df[comp_harm_constants.YEAR_COLUMN]
                                    != pd.DatetimeIndex(df[comp_harm_constants.DATE_COLUMN]).year]
        df_month_comparison = df.loc[df[comp_harm_constants.MONTH_COLUMN]
                                     != pd.DatetimeIndex(df[comp_harm_constants.DATE_COLUMN]).month]

        if not df_year_comparison.empty:
            raise qa_errors.ValueComparisonError(
                f"Value in harmonized year column does not match the value "
                f"in harmonized date column as shown in row(s) below:\n"
                f"{df_year_comparison}")

        if not df_month_comparison.empty:
            raise qa_errors.ValueComparisonError(
                f"Value in harmonized month column does not match the value "
                f"in harmonized date column as shown in row(s) below:\n"
                f"{df_month_comparison}")

        return df

    def assert_no_null_value_in_columns(self,
                                        df,
                                        list_of_col_names):
        """
        Asserts if there is any NULL (NaN) values in the list of
        columns provided. If there is any, raise NullValueFoundError.

        Args:
            df: Raw dataframe to check for NULL/NaN values.
            list_of_col_names: List of column names (each is of string type)
            in which we should look for NULL/NaN values.
            REF1: https://stackoverflow.com/a/42923089
            REF2: https://stackoverflow.com/a/27159258
            REF3: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.isnull.html

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            NullValueFoundError: If there is any NULL/NaN value in the given list
            of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with individual "
                                               f"column names being string values.")

        if df[list_of_col_names].isnull().values.any():
            raise qa_errors.NullValueFoundError(f"Null (NaN) value is "
                                                f"found in one of these "
                                                f"columns: {list_of_col_names}")

        return df

    def assert_no_null_value_in_essential_columns(self,
                                                  df):
        """
        Asserts that essential columns (i.e. HARMONIZED_YEAR,
        HARMONIZED_MONTH, HARMONIZED_DATE, HARMONIZED_REGION,
        HARMONIZED_COUNTRY, HARMONIZED_ADVERTISER,
        HARMONIZED_MEDIA_TYPE and HARMONIZED_CATEGORY)
        do not have NULL (NaN) value in them.

        If there is any NULL (NaN) value, throw NullValueFoundError
        and force the data person to take a look at it.
        """
        cols_with_null = []
        for col_name in self.ESSENTIAL_COLUMNS:
            if df[[col_name]].isnull().values.any():
                cols_with_null.append(col_name)

        if cols_with_null:
            raise qa_errors.NullValueFoundError(f"Null (NaN) value is "
                                                f"found in one of these "
                                                f"columns: {cols_with_null}")

        return df

    def assert_no_empty_str_values_in_columns(self,
                                              df,
                                              list_of_col_names):
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
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with "
                                               f"individual column names being "
                                               f"string values.")

        cols_with_empty_str = []
        for col_name in list_of_col_names:
            # Here, I am converting df[col_name] to str type first
            # to avoid the dreaded FutureWarning from numpy
            # Read more here:
            # https://stackoverflow.com/a/46721064/1330974
            if not df.loc[df[col_name].astype(str) == ''].empty:
                cols_with_empty_str.append(col_name)

        if cols_with_empty_str:
            raise qa_errors.EmptyStringFoundError(
                f"Empty string value found in these column(s): "
                f"{cols_with_empty_str}")

        return df

    def assert_no_empty_str_value_in_essential_columns(
            self,
            df):
        """
        Asserts that essential columns (i.e. HARMONIZED_YEAR,
        HARMONIZED_MONTH, HARMONIZED_DATE, HARMONIZED_REGION,
        HARMONIZED_COUNTRY, HARMONIZED_ADVERTISER,
        HARMONIZED_MEDIA_TYPE and HARMONIZED_CATEGORY)
        do not have any empty string value in them.

        If there is any empty string value, throw NullValueFoundError
        and force the data person to take a look at it.
        """
        return self.assert_no_empty_str_values_in_columns(
            df, self.ESSENTIAL_COLUMNS)

    def assert_only_expected_constants_exist_in_column(
            self,
            df,
            column_name,
            list_or_set_of_expected_values
    ):
        """
        This method asserts that a given column contains
        only a subset or whole of the expected values.
        If it does not, then the error is raised.

        E.g., We can use this method to check if a particular
        column in the transformed data only contain
        specific values (e.g., either 'M' or 'F' for gender).
        """
        diff = set(df[column_name]) - set(list_or_set_of_expected_values)
        if diff:
            raise qa_errors.InvalidValueFoundError(
                f"'{column_name}' column has some unexpected values "
                f"as listed here:\n{diff}")

        return df

    def check_expected_constants_exist_in_column(
            self,
            df,
            column_name,
            set_of_expected_values
    ):
        """
        Some columns in the transformed data should only contain
        specific values (e.g., either 'M' or 'F' for gender).

        This methods inspects distinct values from a given column
        and if any of these values is not found within the
        standard/expected set, it warns the data person so that
        s/he can add the unexpected values to the expected values
        set as needed.
        """
        diff = set(df[column_name]) - set(set_of_expected_values)
        if diff:
            self.logger.warning(
                f"QA => '{column_name}' column has some unexpected "
                f"values as listed here:\n{diff}")

        return df

    def assert_REGION_values_are_valid(self,
                                       df):
        """
        Checks to make sure the values in REGION column are
        based on standard region values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.REGION_COLUMN,
            comp_harm_constants.REGIONS
        )

    def assert_COUNTRY_values_are_valid(self,
                                        df):
        """
        Checks to make sure the values in COUNTRY column are
        based on standard region values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.COUNTRY_COLUMN,
            comp_harm_constants.COUNTRIES
        )

    def checks_ADVERTISER_values_that_do_not_have_mapping(
            self,
            df):
        """
        Checks to make sure the values in ADVERTISER column are
        based on the ADVERTISER_MAPPINGS that we have been building
        gradually for competitive harmonization project.

        If any new advertiser value is found, this method will
        output an WARNING message so that data person can add
        new advertisers to the mapping if relevant.
        """
        potentially_new_advertisers = (
                set(df[comp_harm_constants.ADVERTISER_COLUMN]) -
                set(comp_harm_constants.ADVERTISER_MAPPINGS.values())
        )
        if potentially_new_advertisers:
            self.logger.warning(
                f"QA => We do NOT have these advertisers in our standard "
                f"competitor mapping list in comp_harm_constants.py file. "
                f"If any of them are our global competitors, "
                f"please make sure to update the global advertiser mapping "
                f"list in comp_harm_constants.py file.\n"
                f"{sorted(potentially_new_advertisers)}")

        return df

    def assert_MEDIA_TYPE_values_are_valid(
            self,
            df):
        """
        Asserts that the values in MEDIA_TYPE column are
        based on standard media type values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.MEDIA_TYPE_COLUMN,
            comp_harm_constants.MEDIA_TYPES
        )

    def alert_standard_MEDIA_TYPE_values_that_are_not_found_in_data(
            self,
            df):
        """
        Checks and alert about  the potentially missing
        MEDIA_TYPE values based on all standard media type
        values for competitive harmonization project.
        """
        potentially_missing_media_types = (
                comp_harm_constants.MEDIA_TYPES -
                set(df[comp_harm_constants.MEDIA_TYPE_COLUMN])
        )
        if potentially_missing_media_types:
            self.logger.warning(
                f"QA => These MEDIA_TYPEs are NOT found in the transformed data. "
                f"Make sure that it is normal/exepcted:\n"
                f"{sorted(potentially_missing_media_types)}")

        return df

    def assert_CATEGORY_values_are_valid(
            self,
            df):
        """
        Checks to make sure the values in CATEGORY column are
        based on standard category values for competitive
        harmonization project. If not, throw InvalidValueError.
        """
        return self.assert_only_expected_constants_exist_in_column(
            df,
            comp_harm_constants.CATEGORY_COLUMN,
            comp_harm_constants.CATEGORIES
        )

    def assert_no_less_than_values_in_columns(self,
                                              df,
                                              threshold_value,
                                              list_of_col_names):
        """
        Check if there is any value which is less than the threshold_value
        in the list of columns provided.
        If there is any, raise InvalidValueFoundError.

        Args:
            df: Raw dataframe to check for values.
            threshold_value: Value to compare against individual values in
            the given dataframe's columns.
            list_of_col_names: List of column names (each is of string type)
            whose values we should compare against the threshold value.

        Returns:
            The original dataframe is returned if the assertion is successful.

        Raises:
            InvalidValueFoundError: If there is any empty string value
            in the given list of columns.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with individual "
                                               f"column names being string values.")

        for col_name in list_of_col_names:
            if any(df[col_name] < threshold_value):
                raise qa_errors.InvalidValueFoundError(
                    f"Value(s) less than {threshold_value} are "
                    f"found in this column: {col_name}")

        return df

    def assert_GROSS_SPEND_column_has_no_negative_value(self,
                                                        df):
        """
        Asserts that GROSS_SPEND column has no negative value in it.
        If found, throw InvalidValueFoundError.
        """
        return self.assert_no_less_than_values_in_columns(
            df,
            0,
            [comp_harm_constants.GROSS_SPEND_COLUMN])

    def assert_no_greater_than_values_in_columns(
            self,
            df,
            threshold_value,
            list_of_col_names):
        """
        Check if there is any value which is greater than the threshold_value
        in the list of columns provided.

        If there is any, WARN data person to inspect it.

        Args:
            df: Dataframe to check for values.
            threshold_value: Value to compare against individual values in
            the given dataframe's columns.
            list_of_col_names: List of column names (each is of string type)
            whose values we should compare against the threshold value.

        Returns:
            The original dataframe is returned if the assertion is successful.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with individual "
                                               f"column names being string values.")

        for col_name in list_of_col_names:
            if any(df[col_name] > threshold_value):
                self.logger.warning(
                    f"Value(s) greater than {threshold_value} are "
                    f"found in this column: {col_name}")

        return df

    def assert_GROSS_SPEND_column_has_no_ridiculously_high_spend_value(
            self,
            df):
        """
        Asserts that GROSS_SPEND column has no ridiculously big
        (now, set to 1 billion) values in it for each cell.
        In competitive harmonization project's context, any spend
        line bigger than 1 billion should be inspected by data person.

        If found, WARN data person about it.
        """
        return self.assert_no_greater_than_values_in_columns(
            df,
            self.MAX_SPEND,
            [comp_harm_constants.GROSS_SPEND_COLUMN])

    def assert_float_values_in_columns_have_either_one_or_two_decimals(
            self,
            df,
            list_of_col_names
    ):
        """
        Asserts that float values in a given column have either
        one or two decimals, no more.

        If any violation is found, raise InvalidValueFoundError.

        Args:
            df: Dataframe to check for values.
            list_of_col_names: List of column names (each is of string type)
            whose values we should check for decimals.

        Returns:
            The original dataframe is returned if the assertion is successful.
        """
        if not isinstance(list_of_col_names, list):
            raise qa_errors.InputDataTypeError(f"List of column names must "
                                               f"be of list type with individual "
                                               f"column names being string values.")

        for col_name in list_of_col_names:
            df1 = df[col_name].astype(str) \
                .map(lambda x: [x, '0'] if len(x.split('.')) == 1 else x.split('.'))

            if any([len(x) > 2 for x in df1.values]):
                raise qa_errors.InvalidValueFoundError(
                    f"Some of the values in '{col_name}' column have "
                    f"more than two decimal characters such as '4.32.1'.")

            if any([len(x[1]) > 2 for x in df1.values]):
                raise qa_errors.InvalidValueFoundError(
                    f"Some of the values in '{col_name}' column have "
                    f"more than two decimal digits such as '4.321'.")

        return df

    def assert_GROSS_SPEND_column_values_have_two_decimals(
            self,
            df):
        """
        Asserts that GROSS_SPEND column values are only two
        decimals and no more.

        If any violation is found, raise InvalidValueFoundError.
        """
        return self.assert_float_values_in_columns_have_either_one_or_two_decimals(
            df,
            [comp_harm_constants.GROSS_SPEND_COLUMN]
        )

    def check_possible_duplicates_in_columns(self,
                                             df,
                                             list_of_col_names):
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
