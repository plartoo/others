import logging
import re

import pandas as pd
from glob import glob
import re

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

    def create_new_dataframe_from_input_CSV_files(
            self,
            df,
            folder_name
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
        as the file names in folder_name.

        The reason why we had to do this check is because
        we want to make sure our team members pay attention
        to the files they are processing and whenever they
        process new files, they update the input parameters
        of this function in the JSON config file.

        Args:
            df: Base dataframe loaded from input file
            provided via commandline
            folder_name: List of path and
            file names that we want to load into the new
            dataframe for later transformation.
            delimiter: Delimiter for the input CSV file.

        Returns:
            New dataframe that is composed of data from
            the input files provided as paramter to this
            function.
        """
        list_of_file_path_and_names = glob(''.join([folder_name,'/*']))
        base_file_path_and_name = self.config[KEY_CURRENT_INPUT_FILE]

        for file_path_and_name in list_of_file_path_and_names:
            if not CommonCompHarmQAFunctions.has_same_date_range_in_their_names(
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

    def create_new_dataframe_from_input_EXCEL_files(
            self,
            df,
            folder_name
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
        as the file names in folder_name.

        The reason why we had to do this check is because
        we want to make sure our team members pay attention
        to the files they are processing and whenever they
        process new files, they update the input parameters
        of this function in the JSON config file.

        Args:
            df: Base dataframe loaded from input file
            provided via commandline
            folder_name: List of path and
            file names that we want to load into the new
            dataframe for later transformation.
            delimiter: Delimiter for the input CSV file.

        Returns:
            New dataframe that is composed of data from
            the input files provided as paramter to this
            function.
        """
        list_of_file_path_and_names = glob(''.join([folder_name,'/*']))
        base_file_path_and_name = self.config[KEY_CURRENT_INPUT_FILE]

        for file_path_and_name in list_of_file_path_and_names:
            if not CommonCompHarmQAFunctions.has_same_date_range_in_their_names(
                base_file_path_and_name,
                file_path_and_name
            ):
                raise transform_errors.InputFilesDateRangeMismatchError(base_file_path_and_name, file_path_and_name)

        df = pd.DataFrame()
        for cur_file in list_of_file_path_and_names:
            temp_df = pd.read_excel(cur_file)
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

    def add_HARMONIZED_YEAR_column_using_existing_column_with_year_values(
            self,
            df,
            col_name_with_year_value: str):
        """
        Add HARMONIZED_YEAR column with year value (integer)
        extracted from existing date column in the dataframe.

        Here, the year values from the existing column can be in the formats
        as follows: 'Apr - 2020' (India); '1/1/2020' (Kenya)'

        Args:
            df: Raw dataframe to transform.
            col_name_with_year_value: : Existing column name in the dataframe
            from which this code will extract the year value from.

        Returns:
            Dataframe with HARMONIZED_YEAR column holding integer values.
        """
        return self.add_year_column_using_existing_column_with_year_values(
            df,
            col_name_with_year_value,
            comp_harm_constants.YEAR_COLUMN)

    def add_HARMONIZED_YEAR_column_from_existing_column_in_Spanish_date_with_regex(
            self,
            df,
            col_name_with_year_value: str,
            regex_for_format):
        """
        In countries like Peru, the year's value come in the form of something like,
        'Setiembre del 2020' and we need to harmonize them.
        """
        import re

        df[comp_harm_constants.YEAR_COLUMN] = df[col_name_with_year_value].apply(
            lambda x:re.findall(regex_for_format, x)[0])

        return self.add_year_column_using_existing_column_with_year_values(
            df,
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

    def add_HARMONIZED_MONTH_column_using_existing_column_with_month_values(
            self,
            df,
            col_name_with_year_value: str):
        """
        Add HARMONIZED_MONTH column with month values (integer or string)
        extracted from existing date column in the dataframe.

        Here, the month values from the existing column can be in the formats
        as follows: 'Apr - 2020' (India); '1/1/2020' (Kenya)'

        Args:
            df: Raw dataframe to transform.
            col_name_with_year_value: Existing column name in the dataframe
            from which this code will extract the month value from.

        Returns:
            Dataframe with HARMONIZED_MONTH column holding integer values.
        """
        return self.add_month_column_using_existing_column_with_month_values(
            df,
            col_name_with_year_value,
            comp_harm_constants.MONTH_COLUMN)

    def add_HARMONIZED_MONTH_column_using_existing_month_column_with_only_full_month_names(
            self,
            df,
            existing_month_col_name_with_only_full_month_names: str):
        """
            Creates a new column for integer HARMONIZED_MONTH values using
            full month names (such as 'January', 'February', etc.) from
            an existing month column.

            For example, in GCC input files, the 'YEAR_MONTH' column only
            contains full month name (not year values). For those, we cannot
            convert them to date-time values in Pandas like we do in most
            other countries. This function can be used in that scenario.

            Args:
                df: Raw dataframe to transform.
                existing_month_col_name_with_only_full_month_names: Column
                name in the raw dataframe, which has only full month name
                (not year or date values). This column values will be used
                as reference to assign integer month values in the new
                HARMONIZED_MONTH column.

            Returns:
                The dataframe with newly added HARMONIZED_MONTH column
                with integer month value.
        """
        return self.add_integer_month_column_using_existing_month_col_with_full_month_names(
            df,
            existing_month_col_name_with_only_full_month_names,
            comp_harm_constants.MONTH_COLUMN)

    
    def add_HARMONIZED_MONTH_using_existing_column_with_month_values_and_float_values(
            self,
            df,
            col_name_with_month_value: str):
        df[col_name_with_month_value] = df[col_name_with_month_value].astype(int)
        """
        Add HARMONIZED_MONTH column with month values (integer or string)
        extracted from existing date column in the dataframe.

        Here, the month values from the existing column can be in the formats
        as follows: 'Apr - 2020' (India); '1/1/2020' (Kenya)'

        Args:
            df: Raw dataframe to transform.
            col_name_with_year_value: Existing column name in the dataframe
            from which this code will extract the month value from.

        Returns:
            Dataframe with HARMONIZED_MONTH column holding integer values.
        """
        return self.rename_columns(
            df,
            {col_name_with_month_value: comp_harm_constants.MONTH_COLUMN})
    
    def add_HARMONIZED_MONTH_column_from_existing_column_in_Spanish_date_with_regex(
            self,
            df,
            col_name_with_month_value: str,
            regex_for_format):
        """
        In countries like Guatemala, the month's name come in the form of something like,
        '01Abr20' and we need to harmonize them.
        """
        import re

        df[col_name_with_month_value] = df[col_name_with_month_value].str.lower().apply(
            lambda x:re.findall(regex_for_format, x)[0])
        df[col_name_with_month_value] = df[col_name_with_month_value].map(
            comp_harm_constants.MONTH_REFERENCE_BY_LANGUAGE)

        return self.rename_columns(
            df,
            {col_name_with_month_value: comp_harm_constants.MONTH_COLUMN})

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

    def replace_empty_string_values_with_NOT_AVAILABLE(
            self,
            df,
            column_name):
        """
        This functions was added to manage those Advertiser that are not in the raw data files,
        we will assign "Not available" for those values that will not have an Advertiser name related
        """
        if column_name not in df:
            df[column_name] = comp_harm_constants.NOT_AVAILABLE
        else:
            df[column_name] = df[column_name].replace('', comp_harm_constants.NOT_AVAILABLE)
        return df

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
    
    def replace_non_standard_category_values_with_EMPTY_values(self,
            df,
            new_col_name = comp_harm_constants.CATEGORY_COLUMN):
        temporal_categories = comp_harm_constants.CATEGORIES.copy()
        temporal_categories.remove('Other')
        df[new_col_name] = df[new_col_name].apply(lambda x : x if x in temporal_categories else None)

        return df

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            dict_country_specific_categories,
            existing_category_col_name: str):
        """
        We have some specific category mappings in different countries, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **dict_country_specific_categories)
        
        # We found that there are a lot of possible mappings for 'Other' category.
        # So instead of creating individual mappings for them in regex, which slows 
        # down the data processing by a lot, we will just mark them as 'Not Available'
        # and we will remap them SQL after product mappings are done.

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            existing_category_col_name,
            comp_harm_constants.CATEGORY_COLUMN,
            category_mappings)

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column(
            self,
            df,
            existing_category_col_name: str):
        """
        Add HARMONIZED_CATEGORY column based on string values found
        in raw category column. The HARMONIZED_CATEGORY column
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
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            existing_category_col_name,
            comp_harm_constants.CATEGORY_COLUMN,
            comp_harm_constants.CATEGORY_MAPPINGS)

    def add_HARMONIZED_SUBCATEGORY_column_with_NOT_AVAILABLE_string_values(
        self, 
        df):
        return self.replace_empty_string_values_with_NOT_AVAILABLE(
            df,
            comp_harm_constants.SUBCATEGORY_COLUMN)

    def update_HARMONIZED_CATEGORY_column_using_raw_subcategory_column_values(
            self,
            df,
            raw_subcategory_column_name: str,
            regex_mappings_from_raw_subcategory_values_to_harmonized_category_values: dict
    ):
        """
        Update values in HARMONIZED_CATEGORY column based on string values
        found of raw subcategory column.

        This method needs to be called when the raw subcategory column's
        values are better suited to deduce HARMONIZED_CATEGORY values.
        For example, in Philippines raw data, we call
        add_HARMONIZED_CATEGORY_column_using_existing_category_column
        method and even after that there are some veterinary products
        that needs to be mapped in the raw category column. But we can
        better deduce the harmonized category by using raw subcategory
        column. So we can call this function AFTER calling
        add_HARMONIZED_CATEGORY_column_using_existing_category_column
        like this:
        update_HARMONIZED_CATEGORY_column_using_raw_subcategory_colum_values(
        df, 'Subcategory', {'(i?)Animal Feeds': 'Pet Nutrition'}

        Args:
            df: Raw dataframe to transform.
            raw_subcategory_column_name: Raw subcategory colum name.
            regex_mappings_from_raw_subcategory_values_to_harmonized_category_values:
            Dictionary of regular-expression-based mappings between values in
            raw subcategory column and values that should be updated to in
            HARMONIZED_CATEGORY column.

        Returns:
            Dataframe with HARMONIZED_CATEGORY column values updated
            based on the raw subcategory column values.
        """
        return self.update_col1_values_based_on_values_in_col2_using_regex_mapping\
                (df,
                 comp_harm_constants.CATEGORY_COLUMN,
                 raw_subcategory_column_name,
                 regex_mappings_from_raw_subcategory_values_to_harmonized_category_values)

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

    def add_RAW_SUBCATEGORY_column_with_empty_values(
            self,
            df
    ):
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
        return self.add_new_column_with_fixed_str_value(
            df,
            comp_harm_constants.RAW_SUBCATEGORY_COLUMN,
            "")

    def add_RAW_CATEGORY_column_by_renaming_existing_column(
            self,
            df,
            raw_category_col_name: str
    ):
        """
        Although this method name starts with 'add_*', it actually simply
        renames an existing column (Category, Subcategory, Brand, Subbrand, Product Name)
        to standardized column name.

        I decided to name it as such so that it is easier for team members
        who aren't very familiar with coding to follow the "flow" in JSON
        config file.

        Args:
            df: Raw dataframe to transform.
            raw_category_col_name: Name of the existing column, which
            has category names (string values).

        Returns:
            Dataframe with original column (Category, Subcategory, Brand, Subbrand, etc)
            renamed to standardized column name.
        """
        return self.rename_columns(
            df,
            {raw_category_col_name: comp_harm_constants.RAW_CATEGORY_COLUMN})

    def add_RAW_BRAND_column_by_renaming_existing_column(
            self,
            df,
            raw_brand_col_name: str):
        """
        Same as 'add_RAW_BRAND_column' but this one is for
        RAW_BRAND column.

        Against DRY practices, I decided to duplicate and slightly
        modified 'add_RAW_BRAND_column' here because I want
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

    def add_RAW_BRAND_column_with_empty_values(
            self,
            df
    ):
        """
        Add RAW_BRAND column with the empty strings (because
        we sometimes don't receive brand info from raw data).

        Args:
            df: Raw dataframe to transform.

        Returns:
            Dataframe with RAW_BRAND column (with empty string
            values) added.
        """
        return self.add_new_column_with_fixed_str_value(
            df,
            comp_harm_constants.RAW_BRAND_COLUMN,
            "")

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

    def add_empty_HARMONIZED_columns_for_automated_mapping(
            self,
            df):
        """
        Add HARMONIZED_SUBCATEGORY and HARMONIZED_PRODUCT_NAME columns
        with null (empty string) values so that these can be populated
        by automated mapping process or human mapper).

        Args:
            df: Raw dataframe to transform.

        Returns:
            Dataframe with empty HARMONIZED columns added.
        """
        columns_to_add = [
            comp_harm_constants.PRODUCT_NAME_COLUMN,
            comp_harm_constants.SUBCATEGORY_COLUMN
        ]

        for col_name in columns_to_add:
            df = self.add_new_column_with_fixed_str_value(
                df,
                col_name,
                "")

        return df

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
            comp_harm_constants.EXPECTED_COLUMNS
        )
    def multiply_values_in_column_by_a_thousand(
            self,
            df,
            column_name):
        """
        This function could be used to multiply any column value passed to this function by 1000

        """
        df[column_name] = df[column_name] * 1000
        return df

    def multiply_HARMONIZED_GROSS_SPEND_by_thousand(
            self,
            df):
        """
        This function multiply HARMONIZED_GROSS_SPEND values by 1000 for be used
        in those countries were could be necessary due in some countries like APAC countries
        usually gross values are without multiply by thousand.
        """
        return self.multiply_values_in_given_column_by_thousand(df, comp_harm_constants.GROSS_SPEND_COLUMN)

    def trim_HARMONIZED_GROSS_SPEND_column_to_two_decimals(
            self,
            df):
        """
        This function will be used to assure that spend values has 2 decimal places.
        """
        return self.update_decimal_places_in_columns(
            df,
            [comp_harm_constants.GROSS_SPEND_COLUMN],
            2)
