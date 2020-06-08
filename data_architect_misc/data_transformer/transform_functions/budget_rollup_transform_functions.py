"""This is the subclass of Transform function for Switzerland.

We will define transform functions specific to Switzerland here.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import datetime
import re

import pandas as pd

from constants.budget_rollup_constants import *

from constants.comp_harm_constants import COUNTRIES as COMP_HARM_PROJECT_COUNTRIES



from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_post_transform_qa_functions import CommonPostTransformQAFunctions
from qa_functions.qa_errors import \
    InsufficientNumberOfColumnsError, \
    InvalidValueFoundError, \
    UnexpectedColumnNameFound, \
    UnexpectedColumnValuesFound


class BudgetRollupTransformFunctions(CommonTransformFunctions, CommonPostTransformQAFunctions):

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
            raise UnexpectedColumnValuesFound(
                f"Found value less than {EXPECTED_MINIMUM_YEAR} "
                f"or greater than {current_year} in "
                f"{HARMONIZED_YEAR_COLUMN_NAME}.")

        return df

    def update_HARMONIZED_YEAR_names_with_suffix_LE(
            self,
            df):
        current_year = str(datetime.datetime.now().year)
        old_to_new_value_mapping = {
            current_year: ''.join([current_year,'LE'])
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
            df ):
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

    def create_HARMONIZED_CHANNEL_column_using_CHANNEL_column_values(
            self,
            df ):
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


    def add_sum_of_budget_rows_for_each_region_year_and_macro_channel_pair(self,
                                                                           df,
                                                                           list_of_col_names_to_group_by,
                                                                           col_name_to_sum
                                                                           ) :
        """
        For each unique pair of region, year and macro channel, add a total line
        item for Budget (USD) in the dataframe.
        This is needed to create total Division-wide displays in the dashboard.
        REF: https://stackoverflow.com/q/58276169/1330974
        """
        df_grouped_and_summed = df.groupby(list_of_col_names_to_group_by)[col_name_to_sum]\
            .sum().reset_index()
        df = pd.concat([df, df_grouped_and_summed], sort=False).fillna('Total')\
            .sort_values(by=list_of_col_names_to_group_by).reset_index(drop=True)

        return df


    def add_char_in_front_of_region_names_in_total_rows(self,
                                                        df,
                                                        char_to_add_in_front):
        """
        In Tableau, the filters are sorted by alphabetical order.
        In order to make sure Division filters appear on top of the filter
        options, we need to append space character in front of Division
        total rows under 'Region' column.
        REF1: https://stackoverflow.com/a/49995329/1330974
        E.g., df.loc[df.Hub == 'Total', 'Region'] = df['Region'].apply(lambda x: f" {x}")
        REF2: https://stackoverflow.com/a/45651450/1330974
        E.g., df.loc[df.Hub == 'Total','Region'] = '*' + df[df.Hub == 'Total']['Region']
        """
        df.loc[df.Hub == 'Total', 'Region'] = df['Region'].apply(lambda x: f" {x}")

        return df


    def capitalize_market_name_if_they_are_the_same_as_region_name(self,
                                                                   df):
        """
        Neel decided that in Tableau dashboard market filters, we want to show
        'Division' values with capitalized letters so that users can select them
        to see the total division value (although there's already 'All' option
        to choose in market filter).

        This method make sure that the region values that are copied to market
        columns are capitalized.
        """
        df.loc[df.Region == df.Market, 'Market'] = df['Market'].apply(lambda x: x.upper())

        return df

    def update_(self,
              df):
        import pdb
        pdb.set_trace()
        return df

    def debug(self,
              df):
        import pdb
        pdb.set_trace()
        return df


