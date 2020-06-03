"""This is the subclass of Transform function for Turkey (AED division).

We will define transform functions specific to Turkey here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""
import datetime
import re

import pandas as pd

from constants.fx_rates_constants import \
    DATE_COLUMN, \
    RAW_COUNTRY_COLUMN, \
    HARMONIZED_COUNTRY_COLUMN, \
    FX_RATES_COLUMN, \
    FX_COUNTRY_NAME_TO_HARMONIZED_COUNTRY_NAME_MAPPINGS, \
    COUNTRIES_THAT_USE_USD, \
    COUNTRIES_THAT_USE_EURO, \
    USD_FX_Rate, \
    EURO_CURRENCY_NAME
from constants.comp_harm_constants import COUNTRIES as COMP_HARM_PROJECT_COUNTRIES

from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_post_transform_qa_functions import CommonPostTransformQAFunctions
from qa_functions.qa_errors import \
    InsufficientNumberOfColumnsError, \
    InvalidValueFoundError, \
    UnexpectedColumnNameFound, \
    UnexpectedColumnValuesFound


def generate_one_yyyy_mm_dd_string_for_each_month_of_the_year(year):
    first_days_of_all_months = ['-'.join([str(year), str(i), '1'])
                                for i in range(1, 13)]
    return [datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%Y-%m-%d') for d in first_days_of_all_months]


class FxRatesTransformFunctions(CommonTransformFunctions, CommonPostTransformQAFunctions):

    def select_desired_columns(self,
                               df) -> pd.DataFrame:
        """
        We only need Actual and Estimated FX rate columns
        in addition to 'COUNTRY' name column.
        """
        desired_cols = [RAW_COUNTRY_COLUMN] \
                       + [col_name for col_name in df.columns.tolist()
                          if (str(col_name).startswith('ACT')
                              or str(col_name).startswith('EST'))]
        return df[desired_cols]

    def assert_the_first_column_is_COUNTRY_column(self,
                                                  df) -> pd.DataFrame:
        """
        We must make sure the first column in
        the loaded dataframe is 'COUNTRY' colum.
        Otherwise, some of the ensuing the transform
        functions rely on 'COUNTRY' column being the
        first one.
        """
        if RAW_COUNTRY_COLUMN != df.columns.tolist()[0]:
            raise UnexpectedColumnNameFound(
                f"The first column in the dataframe is not 'COUNTRY'. "
                f"The other transform functions rely on the first column "
                f"being '{RAW_COUNTRY_COLUMN}'. "
                f"Please fix this in the raw data file and rerun the code."
            )

        return df

    def copy_country_names_to_row_below(self,
                                        df,
                                        list_of_col_names) -> pd.DataFrame:
        """
        We need to copy country names to the rows below
        because we need the FX rates in the second row.
        """
        return self.copy_value_from_row_above_to_empty_rows_below(df, list_of_col_names)

    def drop_rows_with_even_number_as_index(self,
                                            df) -> pd.DataFrame:
        """
        We will only extract the local currency to USD FX rate factor.
        For that, we only need to keep rows with odd-numbered indexes.
        REF: https://stackoverflow.com/a/55684977/1330974
        """
        return df.iloc[1::2].reset_index(drop=True)

    def assert_FX_columns_for_all_months_exist(self,
                                               df):
        """ Check if there are 12 columns with FX rates """
        # First, join column names with '|' in a single string.
        col_names = '|'.join(df.columns.tolist()[1:])

        # Second, find either 'ACT' or 'EST' because these
        # represents columns FX rates for each month
        result = re.findall(r'(ACT)|(EST)', col_names)
        expected_col_count = 12
        if len(result) != expected_col_count:
            raise InsufficientNumberOfColumnsError(
                f"Expected FX rate column count of: "
                f"{expected_col_count} but found: "
                f"{len(result)} in the current dataframe."
            )

        return df

    def rename_columns_with_year_and_month_name_for_each(
            self,
            df,
            year
    ):
        """
        Given a year provided as parameter to this method
        and **assuming that the existing columns are already
        in the right order (from January to December)**,
        rename the existing column names with new column
        names having YYYY-MM-DD format.
        """
        cur_year = datetime.datetime.now().year
        if cur_year != year:
            raise InvalidValueFoundError(
                f"The year provided, {year}, is not the same as "
                f"the current year. Please comment out this "
                f"line in python code if you want to proceed "
                f"with the rest of the step even when the year "
                f"that you are using is different than the current "
                f"year (e.g., you are processing data from previous "
                f"years)."
            )

        # ASSUMPTION: we assume that the first column is 'COUNTRY'
        month_cols = df.columns.tolist()[1:]
        yyyy_mm_dd = generate_one_yyyy_mm_dd_string_for_each_month_of_the_year(year)
        old_to_new_name_dict = dict(zip(month_cols, yyyy_mm_dd))

        return self.rename_columns(df, old_to_new_name_dict)

    def unpivot_fx_data(self,
                        df) -> pd.DataFrame:
        # REF: https://stackoverflow.com/a/18259236/1330974
        # First, set the index to COUNTRY column then unstack
        df1=df.set_index(RAW_COUNTRY_COLUMN)
        df2 = df1.unstack().reset_index(name=FX_RATES_COLUMN)

        return self.rename_columns(df2, {'level_0': DATE_COLUMN})

    def add_HARMONIZE_COUNTRY_column_using_existing_country_column(
            self,
            df,
            existing_country_col_name=RAW_COUNTRY_COLUMN,
            harmonized_country_col_name=HARMONIZED_COUNTRY_COLUMN
    ) -> pd.DataFrame:
        """
        Update raw country names with standard country names
        we use in our WorldView Media (WVM) dashboard project
        (as listed in constants.wvm_dashboard_constants).

        If there is no entry in the mapping dictionary,
        we will leave the corresponding cell in the new
        column empty and remove them.
        """
        df = self.add_new_column_with_values_based_on_another_column_values_using_exact_str_match(
            df,
            existing_country_col_name,
            harmonized_country_col_name,
            FX_COUNTRY_NAME_TO_HARMONIZED_COUNTRY_NAME_MAPPINGS
        )

        return df[df[harmonized_country_col_name].notna()].reset_index(drop=True)

    def assert_HARMONIZED_COUNTRY_column_includes_all_expected_countries(
            self,
            df,
            harmonized_country_col_name=HARMONIZED_COUNTRY_COLUMN
    ) -> pd.DataFrame:
        """
        Make sure that we know if CP changes country names in
        FX rate files by raising error when we find that
        not all HARMONIZED country names in mapping dictionary
        show up in the resulting dataframe after mapping.
        """
        expected_harmonized_country_names = set(FX_COUNTRY_NAME_TO_HARMONIZED_COUNTRY_NAME_MAPPINGS.values())
        mapped_harmonized_country_names = set(df[harmonized_country_col_name].unique())

        if expected_harmonized_country_names != mapped_harmonized_country_names:
            raise UnexpectedColumnValuesFound(
                f"We found that these expected countries are missing from "
                f"'{harmonized_country_col_name} column: '"
                f"{expected_harmonized_country_names - mapped_harmonized_country_names}. "
                f"Make sure all expected countries show up in '{harmonized_country_col_name}' "
                f"column or update the country mapping in constants.wvm_dashboard_constants file."
            )

        return df

    def add_rows_for_countries_that_use_USD(self,
                                            df) -> pd.DataFrame:
        """
        GCC, Puerto Rico, USA use USD as currency in the data we receive.
        We will populate rows for these countries with 1.0 as FX rates.
        """
        cur_year = datetime.datetime.now().year
        yyyy_mm_dd = generate_one_yyyy_mm_dd_string_for_each_month_of_the_year(cur_year)

        for country in COUNTRIES_THAT_USE_USD:
            df1 = pd.DataFrame(columns=df.columns)
            for i, d in enumerate(yyyy_mm_dd):
                df1.loc[i] = [d, country, USD_FX_Rate, country]
            df = pd.concat([df, df1])

        return df.reset_index(drop=True)

    def add_rows_for_countries_that_use_EURO(self,
                                             df) -> pd.DataFrame:
        """
        Some EU countries use Euro as currency in the data we receive.
        We will populate rows for these countries by using Euro to USD FX rates.
        """

        for country in COUNTRIES_THAT_USE_EURO:
            # REF: https://stackoverflow.com/a/53954986
            df1 = df[df[HARMONIZED_COUNTRY_COLUMN] == EURO_CURRENCY_NAME].copy(deep=True)
            df1.loc[df1[HARMONIZED_COUNTRY_COLUMN] == EURO_CURRENCY_NAME, HARMONIZED_COUNTRY_COLUMN] = country
            df = pd.concat([df, df1])

        return df.reset_index(drop=True)

    def check_HARMONIZED_COUNTRY_column_for_missing_country_names(
            self,
            df,
            harmonized_country_col_name=HARMONIZED_COUNTRY_COLUMN
    ) -> pd.DataFrame:
        """
        Check harmonized country column to see if we are missing
        any country name from the list of countries we process
        for competitive harmonization project.
        """
        mapped_harmonized_country_names = set(df[harmonized_country_col_name].unique())

        if COMP_HARM_PROJECT_COUNTRIES - mapped_harmonized_country_names:
            raise UnexpectedColumnValuesFound(
                f"We found that these expected countries are missing from "
                f"'{harmonized_country_col_name} column: '"
                f"{COMP_HARM_PROJECT_COUNTRIES - mapped_harmonized_country_names}. "
                f"Make sure all expected countries show up in '{harmonized_country_col_name}' "
                f"column or update the country mapping in constants.wvm_dashboard_constants file."
            )

        return df

    def rearrange_columns_for_final_output(self,
                                           df) -> pd.DataFrame:
        """
        Rearrange the order of columns (just for aesthetic sake)
        so that country and harmonized country columns appear
        next to each other in the final output.
        """
        return self.update_order_of_columns_in_dataframe(
            df,
            [
                DATE_COLUMN,
                RAW_COUNTRY_COLUMN,
                HARMONIZED_COUNTRY_COLUMN,
                FX_RATES_COLUMN
            ]
        )

    # def debug(
    #         self,
    #         df
    # ) -> pd.DataFrame:
    #     import pdb
    #     pdb.set_trace()
    #     return df
    #
    # , {
    #     "function_name": "debug",
    #     "function_args": ""
    # }
