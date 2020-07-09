import logging
import re

import pandas as pd

import transform_errors
from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_DELIMITER, KEY_HEADER
from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_comp_harm_qa_functions import CommonCompHarmQAFunctions


class CommonCompHarmTransformFunctions(CommonTransformFunctions, CommonCompHarmQAFunctions):
    """
    This class houses all common data transformation functions
    specifically related to competitive harmonization project.

    Add any function that can be used across data processing of
    more than one countries in competitive harmonization project
    here.

    NOTE: Some of the function names (e.g., add_HARMONIZED_REGION_column)
    in this class do not follow PEP 8 style guide because
    we want to make sure the column names stand out for
    our team members when they use them.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def extract_date_range_from_file_path_and_name(file_path_and_name):
        # If this method is returning 'IndexError: list index out of range'
        # error, that means no match is found and you need to inspect your
        # file name to make sure it has date range pattern like this:
        # '*_YYYYMMDD_YYYYMMDD*rows', which is specific to comp harm project.
        return re.findall(r'_(\d{8}_\d{8}).*rows', file_path_and_name)[0]

    @staticmethod
    def has_same_date_range_in_their_names(
            file1_path_and_name,
            file2_path_and_name):
        # This method extracts date range of the data from the file names
        # assuming that the file names are given following the standards
        # used in comp_harm project ('*_YYYYMMDD_YYYYMMDD*rows'), and
        # compare them. Based on the comparison, it returns boolean value
        # if the date ranges in these file names match (or not).
        return CommonCompHarmTransformFunctions.extract_date_range_from_file_path_and_name(file1_path_and_name) == \
               CommonCompHarmTransformFunctions.extract_date_range_from_file_path_and_name(file2_path_and_name)

    def create_new_dataframe_from_input_CSV_files(
            self,
            df,
            list_of_file_path_and_names
    ):
        """
        This function will create a new dataframe from the
        list of files provided as parameter. Use this
        function to merge two or more transformed output
        files into one.

        But before creating a new dataframe, this function
        will check to make sure that the base input file
        we provided in commandline (with '-i' flag) or
        JSON config has the same date range in its name
        (e.g., Transformed_Vietnam_20200101_20200331_*)
        as the file names in list_of_file_path_and_names.

        The reason why we had to do this check is because
        we want to make sure our team members pay attention
        to the files they are processing and whenever they
        process new files, they update the input parameters
        of this function in the JSON config file.

        Args:
            df: Base dataframe loaded from input file
            provided via commandline
            list_of_file_path_and_names: List of path and
            file names that we want to load into the new
            dataframe for later transformation.
            delimiter: Delimiter for the input CSV file.

        Returns:
            New dataframe that is composed of data from
            the input files provided as paramter to this
            function.
        """
        base_file_path_and_name = self.config[KEY_CURRENT_INPUT_FILE]
        for file_path_and_name in list_of_file_path_and_names:
            if not CommonCompHarmTransformFunctions.has_same_date_range_in_their_names(
                base_file_path_and_name,
                file_path_and_name
            ):
                raise transform_errors.InputFilesDateRangeMismatchError(base_file_path_and_name, file_path_and_name)

        df = pd.DataFrame()
        for cur_file in list_of_file_path_and_names:
            temp_df = pd.read_csv(cur_file,
                                  delimiter=self.config[KEY_DELIMITER],
                                  header=self.config[KEY_HEADER])
            df = df.append(temp_df)

        return df

    def add_PROCESSED_DATE_column_with_current_date(self, df):
        """
        Creates PROCESSED_DATE column with current date values
        (of date data type).

        Args:
            df: Raw dataframe to transform.

        Returns:
            The dataframe with PROCESSED_DATE with current date values.
        """
        return self.add_date_column_with_current_date(
            df,
            comp_harm_constants.PROCESSED_DATE_COLUMN)

    def add_HARMONIZED_YEAR_column_with_constant_integer_value(
            self,
            df,
            int_year_value: int):
        """
        Add HARMONIZED_YEAR column with year value (integer) provided.

        Args:
            df: Raw dataframe to transform.
            int_year_value: Year (integer) value to add.

        Returns:
            Dataframe with HARMONIZED_YEAR column holding integer values.
        """
        return self.add_year_column_with_fixed_int_value(
            df,
            int_year_value,
            comp_harm_constants.YEAR_COLUMN)

    def add_HARMONIZED_YEAR_column_by_renaming_existing_column(
            self,
            df,
            raw_year_col_name: str):
        """
        This method simply renames an existing Year column
        (with integer year values) with standardized year
        column name for the competitive harmonization project.

        Args:
            df: Raw dataframe to transform.
            raw_year_col_name: Name of the existing column, which
            has Year values (integer values).

        Returns:
            Dataframe with original year column renamed to
            standardized year column name.
        """
        return self.rename_columns(
            df,
            {raw_year_col_name: comp_harm_constants.YEAR_COLUMN})

    def add_HARMONIZED_YEAR_column_using_existing_date_column_values(
            self,
            df,
            date_col_name: str):
        """
        Add HARMONIZED_YEAR column with year value (integer)
        extracted from existing date column in the dataframe.

        Args:
            df: Raw dataframe to transform.
            date_col_name: Existing date column name in the dataframe
            from which this code will extract year value from.

        Returns:
            Dataframe with HARMONIZED_YEAR column holding integer values.
        """
        return self.add_year_column_using_existing_date_column_with_date_values(
            df,
            date_col_name,
            comp_harm_constants.YEAR_COLUMN)

    def add_HARMONIZED_MONTH_column_by_renaming_existing_column(
            self,
            df,
            raw_month_col_name: str):
        """
        This method simply renames an existing Month column
        (with integer year values) with standardized month
        column name for the competitive harmonization project.

        Args:
            df: Raw dataframe to transform.
            raw_month_col_name: Name of the existing column, which
            has Month values (integer values).

        Returns:
            Dataframe with original month column renamed to
            standardized month column name.
        """
        return self.rename_columns(
            df,
            {raw_month_col_name: comp_harm_constants.MONTH_COLUMN})

    def add_HARMONIZED_MONTH_column_using_existing_date_column_values(
            self,
            df,
            date_col_name: str):
        """
        Add HARMONIZED_MONTH column with month value (integer)
        extracted from existing date column in the dataframe.

        Args:
            df: Raw dataframe to transform.
            date_col_name: Existing date column name in the dataframe
            from which this code will extract month value from.

        Returns:
            Dataframe with HARMONIZED_MONTH column holding integer values.
        """
        return self.add_month_column_using_existing_date_column_with_date_values(
            df,
            date_col_name,
            comp_harm_constants.MONTH_COLUMN)

    def add_HARMONIZED_MONTH_column_using_existing_month_column_with_full_month_names(
            self,
            df,
            existing_month_col_name_with_full_month_names: str):
        """
            Creates a new column for integer HARMONIZED_MONTH values using
            full month names (such as 'January', 'February', etc.) from
            an existing month column.

            Args:
                df: Raw dataframe to transform.
                existing_col_name_with_full_month_names: Column name in the
                raw dataframe that will be used as reference to assign
                integer month values in the new HARMONIZED_MONTH column.

            Returns:
                The dataframe with newly added HARMONIZED_MONTH column
                with integer month value.
        """
        return self.add_integer_month_column_using_existing_month_col_with_full_month_names(
            df,
            existing_month_col_name_with_full_month_names,
            comp_harm_constants.MONTH_COLUMN)

    def add_HARMONIZED_DATE_column_using_existing_YEAR_and_MONTH_columns_with_integer_values(
            self,
            df):
        """
            Creates a new column for DATE values using existing YEAR and
            MONTH columns both of which have integer values (such as
            2020 for year and 1-12 for month). The newly created
            HARMONIZED_DATE column will have values like 6/1/2019
            that are of date data type.

            Args:
                df: Raw dataframe to transform.

            Returns:
                The dataframe with newly added HARMONIZED_DATE column with
                values of date type.
        """
        return self.add_date_column_using_existing_year_and_month_columns_with_integer_values(
            df,
            comp_harm_constants.YEAR_COLUMN,
            comp_harm_constants.MONTH_COLUMN,
            comp_harm_constants.DATE_COLUMN)

    def add_HARMONIZED_REGION_column(self, df, region_name):
        """
        Add HARMONIZED_REGION column with region name provided.

        Args:
            df: Raw dataframe to transform.
            region_name: Name of region to add from standardized REGIONS
            defined in comp_harm_constants.py file.

        Returns:
            Dataframe with HARMONIZED_REGION column added.
        """
        return self.add_new_column_with_fixed_str_value(
            df,
            comp_harm_constants.REGION_COLUMN,
            region_name)

    def add_HARMONIZED_COUNTRY_column_using_existing_country_column(
            self,
            df,
            existing_country_col_name: str):
        """
        Add HARMONIZED_COUNTRY column based on string values found
        in an existing country column. The HARMONIZED_COUNTRY column
        will contain standard names of the countries used by competitive
        harmonization project.

        If the raw country name does not have corresponding mapping
        defined as COUNTRY_MAPPINGS in comp_harm_constants.py file,
        the raw value will be assigned in the harmonized column.

        Args:
            df: Raw dataframe to transform.
            existing_country_col_name: Name of the existing column,
            which has raw country names (string values).

        Returns:
            Dataframe with HARMONIZED_COUNTRY column which holds
            standardized country names used by competitive harmonization
            project.
        """
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match\
                (df,
                 existing_country_col_name,
                 comp_harm_constants.COUNTRY_COLUMN,
                 comp_harm_constants.COUNTRY_MAPPINGS)

    def add_HARMONIZED_COUNTRY_column_using_fixed_str_value(
            self,
            df,
            fixed_str_value: str):
        """
        Add HARMONIZED_COUNTRY column based on string values provided
        as parameter (standard name of a country used in competitive
        harmonization project) to this function.

        Args:
            df: Raw dataframe to transform.
            fixed_str_value: Name of the country that is to be used
            in the new HARMONIZED_COUNTRY column.

        Returns:
            Dataframe with HARMONIZED_COUNTRY column which holds
            standardized country names used by competitive harmonization
            project.
        """
        return self.add_new_column_with_fixed_str_value\
                (df,
                 comp_harm_constants.COUNTRY_COLUMN,
                 fixed_str_value)

    def add_HARMONIZED_ADVERTISER_column_using_existing_advertiser_column(
            self,
            df,
            existing_advertiser_col_name: str):
        """
        Add HARMONIZED_ADVERTISER column based on string values found
        in an existing advertiser column. The HARMONIZED_ADVERTISER column
        will contain standard names of the countries used by the competitive
        harmonization project.

        If the raw advertiser name does not have corresponding mapping
        defined as ADVERTISER_MAPPINGS in comp_harm_constants.py file,
        the raw value will be assigned in the harmonized column.

        Args:
            df: Raw dataframe to transform.
            existing_advertiser_col_name: Name of the existing column,
            which has raw advertiser names (string values).

        Returns:
            Dataframe with HARMONIZED_ADVERTISER column which holds
            standardized advertiser names used by the competitive
            harmonization project.
        """
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match\
                (df,
                 existing_advertiser_col_name,
                 comp_harm_constants.ADVERTISER_COLUMN,
                 comp_harm_constants.ADVERTISER_MAPPINGS)

    def add_HARMONIZED_MEDIA_TYPE_column_using_existing_media_type_column(
            self,
            df,
            existing_media_type_col_name: str=comp_harm_constants.RAW_MEDIA_TYPE_COLUMN):
        """
        Add HARMONIZED_MEDIA_TYPE column based on string values found
        in an existing advertiser column. The HARMONIZED_MEDIA_TYPE column
        will contain standard names of the media types used by the
        competitive harmonization project.

        If the raw media type name does not have corresponding mapping
        defined as MEDIA_TYPE_MAPPINGS in comp_harm_constants.py file,
        the raw value will be assigned in the harmonized column.

        Args:
            df: Raw dataframe to transform.
            existing_media_type_col_name: Name of the existing column,
            which has raw media type names (string values). We will
            use default as 'RAW_MEDIA_TYPE' because that's the default
            standard collumn name for media type in Comp. Harm. project.

        Returns:
            Dataframe with HARMONIZED_MEDIA_TYPE column which holds
            standardized media type names used by the competitive
            harmonization project.
        """
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            existing_media_type_col_name,
            comp_harm_constants.MEDIA_TYPE_COLUMN,
            comp_harm_constants.MEDIA_TYPE_MAPPINGS)

    def add_HARMONIZED_MEDIA_TYPE_column_using_fixed_str_value(
            self,
            df,
            fixed_str_value: str):
        """
        Add HARMONIZED_MEDIA_TYPE column based on string values provided
        as parameter (standard name of the media type used in competitive
        harmonization project) to this function.

        Args:
            df: Raw dataframe to transform.
            fixed_str_value: Name of the country that is to be used
            in the new HARMONIZED_MEDIA_TYPE column.

        Returns:
            Dataframe with HARMONIZED_MEDIA_TYPE column which holds
            standardized media type names used by competitive
            harmonization project.
        """
        return self.add_new_column_with_fixed_str_value\
                (df,
                 comp_harm_constants.MEDIA_TYPE_COLUMN,
                 fixed_str_value)

    def add_HARMONIZED_CURRENCY_column(self,
                                       df,
                                       currency_name):
        """
        Add HARMONIZED_CURRENCY column with the currency name provided.

        Args:
            df: Raw dataframe to transform.
            currency_name: Name of the currency to add from the list of
            standardized CURRENCIES defined in comp_harm_constants.py file.

        Returns:
            Dataframe with HARMONIZED_CURRENCY column added.
        """
        return self.add_new_column_with_fixed_str_value(
            df,
            comp_harm_constants.CURRENCY_COLUMN,
            currency_name)

    def add_HARMONIZED_GROSS_SPEND_column(
            self,
            df,
            existing_gross_spend_col_name):
        """
        Add HARMONIZED_CURRENCY column with the currency name provided.

        Args:
            df: Raw dataframe to transform.
            existing_gross_spend_col_name: Name of the raw gross spend
            column.

        Returns:
            Dataframe with HARMONIZED_HARMONIZED column that has values
            from the original (raw) gross spend column trimmed to just
            two decimal digits.
        """
        df[comp_harm_constants.GROSS_SPEND_COLUMN] = df[existing_gross_spend_col_name]

        return self.update_decimal_places_in_columns(
            df,
            [comp_harm_constants.GROSS_SPEND_COLUMN],
            2)

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column(
            self,
            df,
            existing_category_col_name: str):
        """
        Add HARMONIZED_CATEGORY column based on string values found
        in an existing advertiser column. The HARMONIZED_CATEGORY column
        will contain standard names of the categories used by the
        competitive harmonization project.

        If a raw category name does not have corresponding mapping
        defined as CATEGORY_MAPPINGS in comp_harm_constants.py file,
        the raw value will be assigned in the harmonized column.

        Args:
            df: Raw dataframe to transform.
            existing_category_col_name: Name of the existing column,
            which has raw category names (string values).

        Returns:
            Dataframe with HARMONIZED_CATEGORY column which holds
            standardized category names used by the competitive
            harmonization project.
        """
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match\
                (df,
                 existing_category_col_name,
                 comp_harm_constants.CATEGORY_COLUMN,
                 comp_harm_constants.CATEGORY_MAPPINGS)

    def add_RAW_SUBCATEGORY_column_by_renaming_existing_column(
            self,
            df,
            raw_subcategory_col_name: str):
        """
        Although this method name starts with 'add_*', it actually simply
        renames an existing column (Subcategory, Brand, Subbrand, Product Name)
        to standardized column name.

        I decided to name it as such so that it is easier for team members
        who aren't very familiar with coding to follow the "flow" in JSON
        config file.

        Args:
            df: Raw dataframe to transform.
            raw_subcategory_col_name: Name of the existing column, which
            has Subcategory names (string values).

        Returns:
            Dataframe with original column (Subcategory, Brand, Subbrand, etc)
            renamed to standardized column name.
        """
        return self.rename_columns(
            df,
            {raw_subcategory_col_name: comp_harm_constants.RAW_SUBCATEGORY_COLUMN})

    def add_RAW_BRAND_column_by_renaming_existing_column(
            self,
            df,
            raw_brand_col_name: str):
        """
        Same as 'add_RAW_SUBCATEGORY_column' but this one is for
        RAW_BRAND column.

        Against DRY practices, I decided to duplicate and slightly
        modified 'add_RAW_SUBCATEGORY_column' here because I want
        to make sure my team members are forced to declare this method
        via JSON config file (otherwise, I'm afraid they'll forget
        or just not pay attention much on data transformation process).

        Args:
            df: Raw dataframe to transform.
            raw_brand_col_name: Name of the existing column, which
            has Brand names (string values).

        Returns:
            Dataframe with original column (Subcategory, Brand, Subbrand, etc)
            renamed to standardized column name.
        """
        return self.rename_columns(
            df,
            {raw_brand_col_name: comp_harm_constants.RAW_BRAND_COLUMN})

    def add_RAW_SUBBRAND_column_by_renaming_existing_column(
            self,
            df,
            raw_subbrand_col_name: str):
        """
        Same as 'add_RAW_SUBCATEGORY_column' but this one is for
        RAW_SUBBRAND column.

        NOTE: For competitive harmonization team members, only call
        this method IF the raw data frame has subbrand info.

        Args:
            df: Raw dataframe to transform.
            raw_subbrand_col_name: Name of the existing column, which
            has Subbrand names (string values).

        Returns:
            Dataframe with original column (Subcategory, Brand, Subbrand, etc)
            renamed to standardized column name.
        """
        return self.rename_columns(
            df,
            {raw_subbrand_col_name: comp_harm_constants.RAW_SUBBRAND_COLUMN})

    def add_RAW_SUBBRAND_column_with_empty_values(
            self,
            df
    ):
        """
        Add RAW_SUBBRAND column with the empty strings (because
        we sometimes don't receive subbrand info from raw data).

        Args:
            df: Raw dataframe to transform.

        Returns:
            Dataframe with RAW_SUBBRAND column (with empty string
            values) added.
        """
        return self.add_new_column_with_fixed_str_value(
            df,
            comp_harm_constants.RAW_SUBBRAND_COLUMN,
            "")

    def add_RAW_PRODUCT_NAME_column_by_renaming_existing_column(
            self,
            df,
            raw_product_col_name: str):
        """
        Same as 'add_RAW_SUBCATEGORY_column' but this one is for
        RAW_PRODUCT_NAME column.

        Args:
            df: Raw dataframe to transform.
            raw_product_col_name: Name of the existing column, which
            has Product names (string values).

        Returns:
            Dataframe with original column (Subcategory, Brand, Subbrand, etc)
            renamed to standardized column name.
        """
        return self.rename_columns(
            df,
            {raw_product_col_name: comp_harm_constants.RAW_PRODUCT_NAME_COLUMN})

    def add_empty_HARMONIZED_PRODUCT_NAME_column(
            self,
            df):
        """
        Add HARMONIZED_PRODUCT_NAME column with null values (pretty
        much creating an empty column to be filled by automated mapping
        process or human mapper later).

        Args:
            df: Raw dataframe to transform.

        Returns:
            Dataframe with HARMONIZED_PRODUCT_NAME column with null
            values added.
        """
        return self.add_new_column_with_fixed_str_value(
            df,
            comp_harm_constants.PRODUCT_NAME_COLUMN,
            "")

    def filter_and_rearrange_columns_for_final_output(self,
                                                      df):
        """
        This method should be called at the end of the data transformation
        process so that the output file (or destination) will have only
        necessary columns for competitive harmonization project in the
        order that is easy to read/review with human eyes.

        Args:
            df: Raw dataframe to transform.

        Returns:
            Dataframe with only necessary standard columns in the order
            that is easy to read/review by human.
        """
        return self.update_order_of_columns_in_dataframe(
            df,
            [
                comp_harm_constants.PROCESSED_DATE_COLUMN,
                comp_harm_constants.YEAR_COLUMN,
                comp_harm_constants.MONTH_COLUMN,
                comp_harm_constants.DATE_COLUMN,
                comp_harm_constants.REGION_COLUMN,
                comp_harm_constants.COUNTRY_COLUMN,
                comp_harm_constants.ADVERTISER_COLUMN,
                comp_harm_constants.MEDIA_TYPE_COLUMN,
                comp_harm_constants.CURRENCY_COLUMN,
                comp_harm_constants.GROSS_SPEND_COLUMN,
                comp_harm_constants.CATEGORY_COLUMN,
                comp_harm_constants.RAW_SUBCATEGORY_COLUMN,
                comp_harm_constants.RAW_BRAND_COLUMN,
                comp_harm_constants.RAW_SUBBRAND_COLUMN,
                comp_harm_constants.RAW_PRODUCT_NAME_COLUMN,
                comp_harm_constants.PRODUCT_NAME_COLUMN
            ]
        )
