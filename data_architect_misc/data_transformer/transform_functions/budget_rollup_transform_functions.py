"""This is the subclass of Transform function for Switzerland.

We will define transform functions specific to Switzerland here.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import datetime
import re

import pandas as pd

from constants.budget_rollup_constants import *

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


class BudgetRollupTransformFunctions(CommonTransformFunctions, CommonPostTransformQAFunctions):

    def assert_no_empty_value_in_DIMENSION_COLUMNS(self,
                                                   df) -> pd.DataFrame:
        return self.assert_no_empty_str_values_in_columns(df, list(DIMENSION_COLUMNS))

    def assert_no_unexpected_value_in_REGION_column(self,
                                                    df) -> pd.DataFrame:
        return self.assert_only_expected_constants_exist_in_column(
            df,
            RAW_REGION_COLUMN_NAME,
            EXPECTED_REGION_COLUMN_VALUES
        )

    def capitalize_all_REGION_column_values(self,
                                            df) -> pd.DataFrame:
        return self.capitalize_all_letters_of_each_word_in_columns(
            df,
            [RAW_REGION_COLUMN_NAME]
        )

    def create_HARMONIZED_REGION_column_using_REGION_column_values(
            self,
            df
    ) -> pd.DataFrame:
        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match(
            df,
            RAW_REGION_COLUMN_NAME,
            HARMONIZED_REGION_COLUMN_NAME,
            RAW_TO_HARMONIZED_REGION_NAME_MAPPING)

    def update_HARMONIZED_REGION_for_Hills_when_CATEGORY_or_SEGMENT_MACRO_is_pet_related(
            self,
            df
    ) -> pd.DataFrame:
        # We will try to use REGEX and case-insensitive matching to make this robust
        # REF: https://stackoverflow.com/a/48020525
        # df[((df['Category']=='Pet') | (df['Segment Macro']=='Pet Food'))]
        df.loc[
            ((df['Category'].str.contains(r'^pet', flags=re.IGNORECASE)) | (df['Segment Macro'].str.contains(r'^pet.*?food', flags=re.IGNORECASE))),
            HARMONIZED_REGION_COLUMN_NAME
        ] = HILLS_REGION_NAME

        return df

    def capitalize_HARMONIZED_REGION_column_values(self,
                                                   df) -> pd.DataFrame:
        return self.capitalize_all_letters_of_each_word_in_columns(
            df,
            [HARMONIZED_REGION_COLUMN_NAME]
        )


    def add_sum_of_budget_rows_for_each_region_year_and_macro_channel_pair(self,
                                                                           df,
                                                                           list_of_col_names_to_group_by,
                                                                           col_name_to_sum
                                                                           )  -> pd.DataFrame:
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
                                                                   df) -> pd.DataFrame:
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
              df) -> pd.DataFrame:
        import pdb
        pdb.set_trace()
        return df

    def debug(self,
              df) -> pd.DataFrame:
        import pdb
        pdb.set_trace()
        return df


