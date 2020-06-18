"""
This class has functions to aggregate Budget roll-up data
for WorldView Media (WVM) dashboard. This is used as
step 2 of Budget roll-up data processing procedures.

Author: Phyo Thiha and Jholman Jaramillo
Last Modified: June 16, 2020
"""

import datetime
import re

import pandas as pd

from constants.budget_rollup_constants import *

from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_post_transform_qa_functions import CommonPostTransformQAFunctions
from qa_functions.qa_errors import \
    UnexpectedColumnValuesFoundError, \
    EmptyStringFoundError, \
    ColumnListMismatchError


class WvmBudgetRollupAggregateFunctions(CommonTransformFunctions, CommonPostTransformQAFunctions):


    def assert_input_file_has_essential_columns(self,
                                                df):
        if set(ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT) != set(df.columns):
            raise ColumnListMismatchError(
                f"The list of columns in the input file \n"
                f"{set(df.columns)} \n"
                f"is different from essential columns we need "
                f"to aggregate budget roll-up data \n"
                f"{set(ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT)}"
            )

        return df

    def sum_budget_data_by_region(
            self,
            df
    ):
        """
        We will need to sum the budget roll-up spend data by
        Region and combine them with the original budget roll-up
        data for Market Investment Trend view.
        """
        return self.sum_column_data_by_group_by(
            df,
            [HARMONIZED_REGION_COLUMN_NAME],
            HARMONIZED_BUDGET_COLUMN_NAME,
            AGGREGATED_BY_REGION_LABEL)

    def select_only_aggregated_sum_data_by_region(
            self,
            df
    ):
        """
        We will only write the rows representing
        the summed budget data to support the
        Market Investment Trend view.
        """
        return df[df[HARMONIZED_COUNTRY_COLUMN_NAME] == AGGREGATED_BY_REGION_LABEL]

    def copy_HARMONIZED_REGION_values_to_HARMONIZED_COUNTRY_column(
            self,
            df
    ):
        """
        Market Investment Trend view shows Region values in Market filter
        (client's decision...). To support that, we need to copy Harmonized
        Region names to Harmonized Country column for summed rows.
        """
        return self.copy_col1_value_to_col2_if_col2_has_specific_value(
            df,
            HARMONIZED_REGION_COLUMN_NAME,
            HARMONIZED_COUNTRY_COLUMN_NAME,
            AGGREGATED_BY_REGION_LABEL)

    def append_space_character_in_HARMONIZED_COUNTRY_column(
            self,
            df
    ):
        return self.append_characters_in_front_of_column_value(
            df,
            [HARMONIZED_COUNTRY_COLUMN_NAME],
            ' '
        )

    def sum_budget_data_by_region_and_macro_channel(
            self,
            df
    ):
        """
        We will need to sum the budget roll-up spend data by
        Region and combine them with the original budget roll-up
        data for Market Investment Trend view.
        """
        return self.sum_column_data_by_group_by(
            df,
            [
                HARMONIZED_REGION_COLUMN_NAME,
                HARMONIZED_MACRO_CHANNEL_COLUMN_NAME
             ],
            HARMONIZED_BUDGET_COLUMN_NAME,
            AGGREGATED_BY_REGION_AND_MACRO_CHANNEL_LABEL)

    def select_only_aggregated_sum_data_by_region_and_macro_channel(
            self,
            df
    ):
        """
        We will only write the rows representing
        the summed budget data to support the
        Market Investment Trend view.
        """
        return df[df[HARMONIZED_COUNTRY_COLUMN_NAME] == AGGREGATED_BY_REGION_AND_MACRO_CHANNEL_LABEL]


    def copy_HARMONIZED_REGION_values_to_HARMONIZED_COUNTRY_column_for_Digital_Investment_Trend(
            self,
            df
    ):
        """
        Market Investment Trend view shows Region values in Market filter
        (client's decision...). To support that, we need to copy Harmonized
        Region names to Harmonized Country column for summed rows.
        """
        return self.copy_col1_value_to_col2_if_col2_has_specific_value(
            df,
            HARMONIZED_REGION_COLUMN_NAME,
            HARMONIZED_COUNTRY_COLUMN_NAME,
            AGGREGATED_BY_REGION_AND_MACRO_CHANNEL_LABEL)


    def sum_budget_data_by_region_and_brand(
            self,
            df
    ):
        """
        We will need to sum the budget roll-up spend data by
        Region and combine them with the original budget roll-up
        data for Market Investment Trend view.
        """
        return self.sum_column_data_by_group_by(
            df,
            [HARMONIZED_REGION_COLUMN_NAME],
            HARMONIZED_BUDGET_COLUMN_NAME,
            AGGREGATED_BY_REGION_AND_BRAND)

    def select_only_aggregated_sum_data_by_region_and_brand(
            self,
            df
    ):
        """
        We will only write the rows representing
        the summed budget data to support the
        Market Investment Trend view.
        """
        return df[df[HARMONIZED_COUNTRY_COLUMN_NAME] == AGGREGATED_BY_REGION_AND_BRAND]

    def add_all_brands_value_in_harmonized_brand_column(
            self,
            df):
        """
        This functionadd the brand value " All Brands" for the sum of each region.
        """
        df[HARMONIZED_BRAND_COLUMN_NAME] = ' All Brands'

        return df

    def copy_HARMONIZED_REGION_values_to_HARMONIZED_COUNTRY_column_for_Category_Investment_Trend(
            self,
            df
    ):
        """
        Market Investment Trend view shows Region values in Market filter
        (client's decision...). To support that, we need to copy Harmonized
        Region names to Harmonized Country column for summed rows.
        """
        return self.copy_col1_value_to_col2_if_col2_has_specific_value(
            df,
            HARMONIZED_REGION_COLUMN_NAME,
            HARMONIZED_COUNTRY_COLUMN_NAME,
            AGGREGATED_BY_REGION_AND_BRAND)


    # TODO:
    #  CP_Market_Investment_Trend => create aggregate rows groupby Harmonized_Region, then copy the Harmonized_Region value in Harmonized_Country (only output aggregate data) => CP_MARKET_INVESTMENT_TREND.csv
    # CP_Digital_Investment_Trend => create aggregate rows groupby Harmonized_Region and only for Macro_Channel=Digital, then copy the Harmonized_Region value in Harmonized_Country (only output aggregate data) => CP_DIGITAL_INVESTMENT_TREND.csv
    # CP_Category_Investment_Trend
    # => do the same thing as CP_Market_Investment_Trend BUT we need to mark the lines here as ' All Brands'
    def debug(self,
              df):
        import pdb
        pdb.set_trace()
        return df

