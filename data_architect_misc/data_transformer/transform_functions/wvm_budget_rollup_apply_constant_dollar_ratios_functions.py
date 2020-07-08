"""
This class has functions to apply FX rates and constant
dollar ratios to the Budget roll-up data.

Author: Phyo Thiha and Jholman Jaramillo
Last Modified: June 26, 2020
"""
import pandas as pd

from constants.budget_rollup_constants import *
from constants.fx_rates_constants import HARMONIZED_COUNTRY_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA, \
    CONSTANT_DOLLAR_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA, YEAR_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA

from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_comp_harm_qa_functions import CommonCompHarmQAFunctions


class WvmBudgetRollupApplyConstantDollarRatiosFunctions(CommonTransformFunctions,
                                                        CommonCompHarmQAFunctions):

    def __init__(self, config):
        self.config = config

    def load_constant_dollar_ratios_to_dataframe(
            self,
            df,
            constant_dollar_ratios_file
    ):
        df_fx = pd.read_excel(constant_dollar_ratios_file)
        df = pd.concat([df, df_fx], keys=(KEY_FOR_BUDGET_DATA,
                                          KEY_FOR_CONSTANT_DOLLAR_RATIO_DATA))
        return df

    def unpivot_constant_dollar_ratios_data(
            self,
            df
    ):
        # 1. Select constant dollar key from multi-index dataframe.
        # Then, drop budget roll-up data related columns and
        # assign it to the new variable/dataframe.
        const_dollar_ratio_df = df.xs(KEY_FOR_CONSTANT_DOLLAR_RATIO_DATA).drop(
            ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT_BUDGET_DATA,
            axis=1
        )

        # 2. Unpivot constant dollar ratio dataframe
        const_dollar_ratio_df = const_dollar_ratio_df.set_index(HARMONIZED_COUNTRY_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA).unstack()

        # 3. Rename columns from unpivoted data
        const_dollar_ratio_df = const_dollar_ratio_df.reset_index().rename(
             columns={
                 'level_0': YEAR_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA,
                 0: CONSTANT_DOLLAR_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA
             })

        # 4. We need to create some temp columns to join on;
        # Otherwise, some country names and some year (e.g., 2020LE)
        # won't match between two data sets.
        const_dollar_ratio_df['Temp_Harmonized_Year_1'] = const_dollar_ratio_df[YEAR_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA]
        const_dollar_ratio_df['Temp_Harmonized_Year_1'] = const_dollar_ratio_df['Temp_Harmonized_Year_1'].str.replace('LE','')
        const_dollar_ratio_df['Temp_Country_1'] = const_dollar_ratio_df[
            HARMONIZED_COUNTRY_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA].str.lower()

        # 5. Create a new data frame only for Budget data with temp columns to join on
        budget_df = df.xs(KEY_FOR_BUDGET_DATA)[ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT_BUDGET_DATA]
        budget_df['Temp_Harmonized_Year_2'] = budget_df[HARMONIZED_YEAR_COLUMN_BUDGET_DATA]
        budget_df['Temp_Harmonized_Year_2'] = budget_df['Temp_Harmonized_Year_2'].str.replace('LE','')

        # We need to undo 'Hills *' prefixes in the Budget data
        budget_df[HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA] = budget_df[HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA].str.replace('Hills ','')
        budget_df['Temp_Country_2'] = budget_df[HARMONIZED_COUNTRY_COLUMN_BUDGET_DATA].str.lower()

        # 5. Left join budget_df with const_dollar_ratio_df
        df = budget_df.merge(const_dollar_ratio_df,
                             how='left',
                             left_on=['Temp_Harmonized_Year_2',
                                      'Temp_Country_2'],
                             right_on=['Temp_Harmonized_Year_1',
                                       'Temp_Country_1'])

        return df

    def apply_constant_dollar_ratios_to_budget_usd(
            self,
            df
    ):
        # Create a new column with the formula below:
        # (Harmonized_Budget_USD * Constant_Dollar_Ratio)
        df[HARMONIZED_CONSTANT_DOLLAR_COLUMN_BUDGET_DATA] = df[HARMONIZED_BUDGET_COLUMN_BUDGET_DATA] \
                                                            * df[CONSTANT_DOLLAR_COLUMN_FX_RATES_AND_CONSTANT_DOLLAR_DATA]

        return df

    def copy_original_budget_usd_values_to_constant_usd_column_for_countries_that_do_not_have_constant_dollar_ratios(
            self,
            df
    ):
        df.loc[
            df[HARMONIZED_CONSTANT_DOLLAR_COLUMN_BUDGET_DATA].isnull(),
            HARMONIZED_CONSTANT_DOLLAR_COLUMN_BUDGET_DATA
        ] = df[HARMONIZED_BUDGET_COLUMN_BUDGET_DATA]

        return df

    def filter_and_rearrange_columns_for_final_output_of_budget_usd_and_constant_usd(
            self,
            df
    ):
        return self.update_order_of_columns_in_dataframe(
            df,
            ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT_BUDGET_USD_AND_CONSTANT_USD_DATA
        )
