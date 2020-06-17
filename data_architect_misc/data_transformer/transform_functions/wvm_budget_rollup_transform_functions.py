"""
This is the function class to clean and transform Budget roll-up data
for WorldView Media (WVM) dashboard.

Author: Phyo Thiha and Jholman Jaramillo
Last Modified: June 16, 2020
"""

import datetime
import re

from constants.budget_rollup_constants import *

from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_post_transform_qa_functions import CommonPostTransformQAFunctions
from qa_functions.qa_errors import UnexpectedColumnValuesFoundError, EmptyStringFoundError


class WvmBudgetRollupTransformFunctions(CommonTransformFunctions, CommonPostTransformQAFunctions):

    def assert_no_empty_value_in_DIMENSION_COLUMNS(self,
                                                   df):
        return self.assert_no_empty_str_values_in_columns(df, list(DIMENSION_COLUMNS))

    def assert_no_unexpected_value_in_REGION_column(self,
                                                    df):
        return self.assert_only_expected_constants_exist_in_column(
            df,
            RAW_REGION_COLUMN_NAME,
            EXPECTED_REGION_COLUMN_VALUES
        )

    def capitalize_all_REGION_column_values(self,
                                            df):
        return self.capitalize_all_letters_of_each_word_in_columns(
            df,
            [RAW_REGION_COLUMN_NAME]
        )

    def create_HARMONIZED_REGION_column_using_REGION_column_values(
            self,
            df
    ):
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            RAW_REGION_COLUMN_NAME,
            HARMONIZED_REGION_COLUMN_NAME,
            RAW_TO_HARMONIZED_REGION_NAME_MAPPING)

    def update_HARMONIZED_REGION_for_Hills_when_CATEGORY_or_SEGMENT_MACRO_is_pet_related(
            self,
            df
    ):
        # We will try to use REGEX and case-insensitive matching to make this robust
        # REF: https://stackoverflow.com/a/48020525
        # df[((df['Category']=='Pet') | (df['Segment Macro']=='Pet Food'))]
        df.loc[
            ((df[RAW_CATEGORY_COLUMN_NAME].str.contains(r'^pet', flags=re.IGNORECASE))
             | (df[RAW_SEGMENT_MACRO_COLUMN_NAME].str.contains(r'^pet.*?food', flags=re.IGNORECASE))),
            HARMONIZED_REGION_COLUMN_NAME
        ] = HILLS_REGION_NAME

        return df

    def capitalize_HARMONIZED_REGION_column_values(self,
                                                   df):
        return self.capitalize_all_letters_of_each_word_in_columns(
            df,
            [HARMONIZED_REGION_COLUMN_NAME]
        )

    def create_HARMONIZED_MARKET_column_using_MARKET_column_values(
            self,
            df
    ):
        return self.add_new_column_by_copying_values_from_another_column(
            df,
            [RAW_MARKET_COLUMN_NAME],
            [HARMONIZED_MARKET_COLUMN_NAME]
        )

    def update_US_name_to_USA_in_MARKET_column(
            self,
            df
    ):
        return self.update_str_values_in_columns(
            df,
            [HARMONIZED_MARKET_COLUMN_NAME],
            [MARKET_MAPPING_TO_USA]
        )

    def update_Hills_in_HARMONIZED_MARKET_column_to_USA_for_pet_related_lines(
            self,
            df
    ):
        df.loc[
            (((df[RAW_CATEGORY_COLUMN_NAME].str.contains(r'^pet', flags=re.IGNORECASE))
              | (df[RAW_SEGMENT_MACRO_COLUMN_NAME].str.contains(r'^pet.*?food', flags=re.IGNORECASE)))
             & (df[RAW_MARKET_COLUMN_NAME].str.contains(r'^hills', flags=re.IGNORECASE))),
            HARMONIZED_MARKET_COLUMN_NAME
        ] = USA_COUNTRY_STANDARD_NAME

        return df

    def update_HARMONIZED_MARKET_names_with_prefix_Hills(self,
                                                         df):
        df.loc[
            df[HARMONIZED_REGION_COLUMN_NAME].str.contains(r'^hills', flags=re.IGNORECASE),
            HARMONIZED_MARKET_COLUMN_NAME
        ] = PREFIX_FOR_MARKET_HILLS + ' ' + df[HARMONIZED_MARKET_COLUMN_NAME].astype(str)

        return df

    def create_HARMONIZED_COUNTRY_column_using_HARMONIZED_MARKET_column(
            self,
            df
    ):
        """
        We will create Harmonized_Country column because not all countries' names
        in Harmonized_Market are equal to our standard country names.
        """
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            HARMONIZED_MARKET_COLUMN_NAME,
            HARMONIZED_COUNTRY_COLUMN_NAME,
            HARMONIZED_MARKET_TO_COMP_HARM_STANDARD_COUNTRY_NAME_MAPPINGS)

    def assert_no_unexpected_value_in_HARMONIZED_COUNTRY_column(
            self,
            df):
        return self.assert_only_expected_constants_exist_in_column(
            df,
            HARMONIZED_COUNTRY_COLUMN_NAME,
            HARMONIZED_MARKET_TO_COMP_HARM_STANDARD_COUNTRY_NAME_MAPPINGS.values()
        )

    def create_HARMONIZED_YEAR_column_using_YEAR_column_values(
            self,
            df
    ):
        return self.add_new_column_by_copying_values_from_another_column(
            df,
            [RAW_YEAR_COLUMN_NAME],
            [HARMONIZED_YEAR_COLUMN_NAME]
        )

    def assert_no_unexpected_value_in_HARMONIZED_YEAR_column(
            self,
            df):
        # We know that Budget roll-up data does not go beyond 2012
        # and it should also not go after the current year
        current_year = datetime.datetime.now().year

        if EXPECTED_MINIMUM_YEAR < current_year < df.Harmonized_Year.max():
            raise UnexpectedColumnValuesFoundError(
                f"Found value less than {EXPECTED_MINIMUM_YEAR} "
                f"or greater than {current_year} in "
                f"{HARMONIZED_YEAR_COLUMN_NAME}.")

        return df

    def update_HARMONIZED_YEAR_names_with_suffix_LE(
            self,
            df):
        current_year = str(datetime.datetime.now().year)
        old_to_new_value_mapping = {
            current_year: ''.join([current_year, 'LE'])
        }

        return self.update_int_values_in_columns_to_str_values(
            df,
            [HARMONIZED_YEAR_COLUMN_NAME],
            [old_to_new_value_mapping]
        )

    def create_HARMONIZED_CATEGORY_column_using_CATEGORY_column_values(
            self,
            df
    ):
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            RAW_CATEGORY_COLUMN_NAME,
            HARMONIZED_CATEGORY_COLUMN_NAME,
            RAW_TO_HARMONIZED_CATEGORY_NAME_MAPPING)

    def assert_no_unexpected_value_in_HARMONIZED_CATEGORY_column(
            self,
            df):
        return self.assert_only_expected_constants_exist_in_column(
            df,
            HARMONIZED_CATEGORY_COLUMN_NAME,
            set(RAW_TO_HARMONIZED_CATEGORY_NAME_MAPPING.values())
        )

    def create_HARMONIZED_SUBCATEGORY_column_using_SEGMENT_MACRO_column_values(
            self,
            df):
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            RAW_SEGMENT_MACRO_COLUMN_NAME,
            HARMONIZED_SUBCATEGORY_COLUMN_NAME,
            RAW_TO_HARMONIZED_SUBCATEGORY_NAME_MAPPING)

    def assert_no_unexpected_value_in_HARMONIZED_SUBCATEGORY_column(
            self,
            df):
        return self.assert_only_expected_constants_exist_in_column(
            df,
            HARMONIZED_SUBCATEGORY_COLUMN_NAME,
            RAW_TO_HARMONIZED_SUBCATEGORY_NAME_MAPPING.values()
        )

    def create_HARMONIZED_BRAND_column_by_copying_Brand_column_values(
            self,
            df):
        return self.add_new_column_by_copying_values_from_another_column(
            df,
            [RAW_BRAND_COLUMN_NAME],
            [HARMONIZED_BRAND_COLUMN_NAME]
        )

    def create_HARMONIZED_CHANNEL_column_using_CHANNEL_column_values(
            self,
            df):
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            RAW_CHANNEL_COLUMN_NAME,
            HARMONIZED_CHANNEL_COLUMN_NAME,
            RAW_TO_HARMONIZED_CHANNEL_NAME_MAPPING)

    def assert_no_unexpected_value_in_HARMONIZED_CHANNEL_column(
            self,
            df):
        return self.assert_only_expected_constants_exist_in_column(
            df,
            HARMONIZED_CHANNEL_COLUMN_NAME,
            RAW_TO_HARMONIZED_CHANNEL_NAME_MAPPING.values()
        )

    def create_HARMONIZED_MACRO_CHANNEL_column_using_MACRO_CHANNEL_column_values(
            self,
            df):
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            RAW_MACRO_CHANNEL_COLUMN_NAME,
            HARMONIZED_MACRO_CHANNEL_COLUMN_NAME,
            RAW_TO_HARMONIZED_MACRO_CHANNEL_NAME_MAPPING)

    def assert_no_unexpected_value_in_HARMONIZED_MACRO_CHANNEL_column(
            self,
            df):
        return self.assert_only_expected_constants_exist_in_column(
            df,
            HARMONIZED_MACRO_CHANNEL_COLUMN_NAME,
            RAW_TO_HARMONIZED_MACRO_CHANNEL_NAME_MAPPING.values()
        )

    def create_HARMONIZED_BUDGET_USD_column_using_BUDGET_USD_column_values(
            self,
            df):
        # In addition to copying data from raw Budget column,
        # we will strip the values of '$' and ','. We will
        # also convert the data to float and trim it to
        # two-decimal places.
        df[HARMONIZED_BUDGET_COLUMN_NAME] = df[[RAW_BUDGET_COLUMN_NAME]]\
            .replace(r'[,\$\s]', '', regex=True)\
            .replace(r'[\-]', '0', regex=True)

        return df

    def assert_HARMONIZED_BUDGET_USD_column_has_no_empty_values(
            self,
            df):
        if not df[df[HARMONIZED_BUDGET_COLUMN_NAME] == ''].empty:
            # We will not reuse function in common_post_transform_qa_functions.py
            # because we want to give a specific error message for this one.
            raise EmptyStringFoundError(
                f"There are empty cells in the '{HARMONIZED_BUDGET_COLUMN_NAME}' column. "
                f"The budget data should not contain empty values, so please "
                f"check them in the raw file and delete the rows with empty data "
                f"**manually**, if appropriate.")

        return df

    def convert_HARMONIZED_BUDGET_USD_column_to_float(
            self,
            df):
        df[HARMONIZED_BUDGET_COLUMN_NAME] = df[HARMONIZED_BUDGET_COLUMN_NAME].astype(float).round(2)

        return df

    def assert_HARMONIZED_BUDGET_USD_column_has_no_negative_value(
            self,
            df):
        return self.assert_no_less_than_values_in_columns(
            df,
            0,
            [HARMONIZED_BUDGET_COLUMN_NAME])

    def assert_HARMONIZED_BUDGET_USD_column_values_have_two_decimals(
            self,
            df):

        return self.assert_float_values_in_columns_have_either_one_or_two_decimals(
            df,
            [HARMONIZED_BUDGET_COLUMN_NAME]
        )

    def filter_and_rearrange_columns_for_final_output(self,
                                                      df):
        """
        We will only include Harmonized_* columns in the
        transformed output.
        """
        return self.update_order_of_columns_in_dataframe(
            df,
            ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT
        )


    # {
    #   "function_name": "aggregate_HARMONIZED_BUDGET_USD_by_HARMONIZED_YEAR_HARMONIZED_REGION_AND_HARMONIZED_MACRO_CHANNEL"
    # },
    # def aggregate_HARMONIZED_BUDGET_USD_by_HARMONIZED_YEAR_HARMONIZED_REGION_AND_HARMONIZED_MACRO_CHANNEL(
    #         self,
    #         df):
    #     """
    #     For each unique pair of region, year and macro channel, add a total line
    #     item for Budget (USD) in the dataframe.
    #     This is needed to create total Division-wide displays in the dashboard.
    #     REF: https://stackoverflow.com/q/58276169/1330974
    #     """
    #     group_by_cols = [HARMONIZED_YEAR_COLUMN_NAME,
    #                      HARMONIZED_REGION_COLUMN_NAME,
    #                      HARMONIZED_MACRO_CHANNEL_COLUMN_NAME]
    #     df_grouped_and_summed = df.groupby(group_by_cols)[HARMONIZED_BUDGET_COLUMN_NAME] \
    #         .sum().reset_index()
    #     df = pd.concat([df, df_grouped_and_summed], sort=False) \
    #         .fillna(FILLNA_VAL_FOR_AGGREGATED_HARMONIZED_BUDGET) \
    #         .sort_values(by=group_by_cols).reset_index(drop=True)
    #
    #     return df


    # def add_char_in_front_of_region_names_in_total_rows(
    #         self,
    #         df,
    #         char_to_add_in_front):
    #     """
    #     In Tableau, the filters are sorted by alphabetical order.
    #     In order to make sure Division filters appear on top of the filter
    #     options, we need to append space character in front of Division
    #     total rows under 'Region' column.
    #     REF1: https://stackoverflow.com/a/49995329/1330974
    #     E.g., df.loc[df.Hub == 'Total', 'Region'] = df['Region'].apply(lambda x: f" {x}")
    #     REF2: https://stackoverflow.com/a/45651450/1330974
    #     E.g., df.loc[df.Hub == 'Total','Region'] = '*' + df[df.Hub == 'Total']['Region']
    #     """
    #     import pdb
    #     pdb.set_trace()
    #     df.loc[df.Hub == 'Total', 'Region'] = df['Region'].apply(lambda x: f" {x}")
    #     # df.loc[df[HARMONIZED_COUNTRY_COLUMN_NAME] == '', HARMONIZED_COUNTRY_COLUMN_NAME] = ' ' + df[HARMONIZED_REGION_COLUMN_NAME]
    #
    #     return df
    #
    # def add_ALL_BRANDS_value_in_BRAND_column_when_Regions_as_Markets(
    #         self,
    #         df):
    #     """
    #     For those values in Country column with Region values, the brand value " All Brands" represent the summ of all these Brands
    #     """
    #     df[RAW_BRAND_COLUMN_NAME] = df[RAW_BRAND_COLUMN_NAME].replace(r'',' All Brands', regex= True)
    #
    #     return df
    #
    # def capitalize_market_name_if_they_are_the_same_as_region_name(self,
    #                                                                df):
    #     """
    #     Neel decided that in Tableau dashboard market filters, we want to show
    #     'Division' values with capitalized letters so that users can select them
    #     to see the total division value (although there's already 'All' option
    #     to choose in market filter).
    #
    #     This method make sure that the region values that are copied to market
    #     columns are capitalized.
    #     """
    #     df.loc[df.Region == df.Market, 'Market'] = df['Market'].apply(lambda x: x.upper())
    #
    #     return df
    #
    # def debug(self,
    #           df):
    #     import pdb
    #     pdb.set_trace()
    #     return df
    #   {
    #     "function_name": "create_HARMONIZED_BRAND_column_by_copying_Brand_column_values"
    #   },
    #   {
    #     "function_name": "add_char_in_front_of_region_names_in_total_rows",
    #     "function_args": [" "]
    #   },
    #
    #   {
    #     "function_name": "add_ALL_BRANDS_value_in_BRAND_column_when_Regions_as_Markets"
    #   },
    #
    #   {
    #     "function_name": "debug"
    #   },
