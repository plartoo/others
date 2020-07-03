"""
This class has functions to aggregate Budget roll-up data
for WorldView Media (WVM) dashboard. This is used as
step 2 of Budget roll-up data processing procedures.

Author: Phyo Thiha and Jholman Jaramillo
Last Modified: June 16, 2020
"""

from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_post_transform_qa_functions import CommonPostTransformQAFunctions
from qa_functions.qa_errors import ColumnListMismatchError

from constants.budget_rollup_constants import *

class WvmBudgetRollupAggregateFunctions(CommonTransformFunctions, CommonPostTransformQAFunctions):

    def assert_input_file_has_essential_columns(self,
                                                df):
        if set(ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT_BUDGET_USD_AND_CONSTANT_USD_DATA) != set(df.columns):
            raise ColumnListMismatchError(

                f"The list of columns in the input file \n"
                f"{set(df.columns)} \n"
                f"is different from essential columns we need "
                f"to aggregate budget roll-up data \n"
                f"{set(ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT_BUDGET_USD_AND_CONSTANT_USD_DATA)}"
            )

        return df

    def sum_budget_and_constant_dollar_spends_by_year_and_region_for_Market_Investment_Trend_view(
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
                HARMONIZED_YEAR_COLUMN_BUDGET_DATA,
                HARMONIZED_REGION_COLUMN_BUDGET_DATA
            ],
            [
                HARMONIZED_BUDGET_COLUMN_BUDGET_DATA,
                HARMONIZED_CONSTANT_DOLLAR_COLUMN_BUDGET_DATA
            ],
            AGGREGATED_BY_YEAR_AND_REGION_LABEL_FOR_MARKET_INVESTMENT_TREND_VIEW)

    def select_only_aggregated_sum_data_by_region_for_Market_Investment_Trend_view(
            self,
            df
    ):
        """
        We will only write the rows representing the summed budget data
        to support the Market Investment Trend view.
        """
        return df[df[HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA]
                  == AGGREGATED_BY_YEAR_AND_REGION_LABEL_FOR_MARKET_INVESTMENT_TREND_VIEW]

    def copy_HARMONIZED_REGION_values_to_HARMONIZED_COUNTRY_column_for_Market_Investment_Trend_view(
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
            HARMONIZED_REGION_COLUMN_BUDGET_DATA,
            HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA,
            AGGREGATED_BY_YEAR_AND_REGION_LABEL_FOR_MARKET_INVESTMENT_TREND_VIEW)

    def append_space_character_in_HARMONIZED_COUNTRY_column(
            self,
            df
    ):
        """
        This is to make sure the REGION names appear first in the
        Market filter in Tableau (another unusual request by
        the client).
        """
        return self.append_characters_in_front_of_column_value(
            df,
            [HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA],
            ' '
        )

    def sum_budget_and_constant_dollar_spends_by_year_region_and_macro_channel_for_Digital_Investment_Trend_view(
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
                HARMONIZED_YEAR_COLUMN_BUDGET_DATA,
                HARMONIZED_REGION_COLUMN_BUDGET_DATA,
                HARMONIZED_MACRO_CHANNEL_COLUMN_BUDGET_DATA
             ],
            [
                HARMONIZED_BUDGET_COLUMN_BUDGET_DATA,
                HARMONIZED_CONSTANT_DOLLAR_COLUMN_BUDGET_DATA
            ],
            AGGREGATED_BY_YEAR_REGION_AND_MACRO_CHANNEL_LABEL_FOR_DIGITAL_INVESTMENT_TREND_VIEW)

    def select_only_aggregated_sum_data_by_region_and_macro_channel_for_Digital_Investment_Trend_view(
            self,
            df
    ):
        """
        We will only write the rows representing
        the summed budget data to support the
        Market Investment Trend view.
        """
        return df[df[HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA]
                  == AGGREGATED_BY_YEAR_REGION_AND_MACRO_CHANNEL_LABEL_FOR_DIGITAL_INVESTMENT_TREND_VIEW]


    def copy_HARMONIZED_REGION_values_to_HARMONIZED_COUNTRY_column_for_Digital_Investment_Trend_view(
            self,
            df
    ):
        """
        Digital Investment Trend view shows Region values in Market filter
        (client's decision...). To support that, we need to copy Harmonized
        Region names to Harmonized Country column for summed rows.
        """
        return self.copy_col1_value_to_col2_if_col2_has_specific_value(
            df,
            HARMONIZED_REGION_COLUMN_BUDGET_DATA,
            HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA,
            AGGREGATED_BY_YEAR_REGION_AND_MACRO_CHANNEL_LABEL_FOR_DIGITAL_INVESTMENT_TREND_VIEW)


    def sum_budget_and_constant_dollar_spends_by_year_and_region_for_Category_Investment_Trend_view(
            self,
            df
    ):
        """
        We will need to sum the budget roll-up spend data by
        Region and combine them with the original budget roll-up
        data for Category Investment Trend view.
        """
        return self.sum_column_data_by_group_by(
            df,
            [
                HARMONIZED_YEAR_COLUMN_BUDGET_DATA,
                HARMONIZED_REGION_COLUMN_BUDGET_DATA
            ],
            [
                HARMONIZED_BUDGET_COLUMN_BUDGET_DATA,
                HARMONIZED_CONSTANT_DOLLAR_COLUMN_BUDGET_DATA
             ],
            AGGREGATED_BY_YEAR_AND_REGION_LABEL_FOR_CATEGORY_INV_TREND_VIEW)

    def select_only_aggregated_sum_data_by_region_for_Category_Investment_Trend_view(
            self,
            df
    ):
        """
        We will only write the rows representing the summed budget data
        to support the Category Investment Trend view.
        """
        return df[df[HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA]
                  == AGGREGATED_BY_YEAR_AND_REGION_LABEL_FOR_CATEGORY_INV_TREND_VIEW]

    def copy_HARMONIZED_REGION_values_to_HARMONIZED_COUNTRY_column_for_Category_Investment_Trend_view(
            self,
            df
    ):
        """
        Category Investment Trend view shows Region values in Market filter
        (client's decision...). To support that, we need to copy Harmonized
        Region names to Harmonized Country column for summed rows.
        """
        return self.copy_col1_value_to_col2_if_col2_has_specific_value(
            df,
            HARMONIZED_REGION_COLUMN_BUDGET_DATA,
            HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA,
            AGGREGATED_BY_YEAR_AND_REGION_LABEL_FOR_CATEGORY_INV_TREND_VIEW)

    def add_all_brands_value_in_HARMONIZED_BRAND_column_for_Category_Investment_Trend_view(
            self,
            df):
        """
        This function adds the brand value " All Brands" for the sum of each region
        under HARMONIZED_BRAND column. This allows us to display 'All Brands' as
        a filter option in Category Investment Trend view.
        """
        df[HARMONIZED_BRAND_COLUMN_BUDGET_DATA] = ' All Brands'

        return df
