"""
This class has functions to apply FX rates and constant
dollar ratios to the Budget roll-up data.

Author: Phyo Thiha and Jholman Jaramillo
Last Modified: June 26, 2020
"""
import datetime
import re

import pandas as pd

from constants.budget_rollup_constants import *
from constants.fx_rates_constants import CONSTANT_DOLLAR_COLUMN_SUFFIX, HARMONIZED_COUNTRY_COLUMN_FX_RATES, \
    CONSTANT_DOLLAR_COLUMN_FX_RATES, YEAR_COLUMN_FX_RATES, ESSENTIAL_COLUMNS_FOR_CONSTANT_USD_DATA

from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_post_transform_qa_functions import CommonPostTransformQAFunctions
from qa_functions.qa_errors import ColumnListMismatchError


class WvmBudgetRollupApplyConstantDollarRatiosFunctions(CommonTransformFunctions,
                                                        CommonPostTransformQAFunctions):

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
        # Select constant dollar key from multi-index dataframe.
        # Then, drop budget roll-up data related columns and
        # assign it to the new variable/dataframe.
        const_dollar_ratio_df = df.xs(KEY_FOR_CONSTANT_DOLLAR_RATIO_DATA).drop(
            ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT_BUDGET_DATA,
            axis=1
        )

        # Unpivot constant dollar ratio dataframe
        const_dollar_ratio_df = const_dollar_ratio_df.set_index(HARMONIZED_COUNTRY_COLUMN_FX_RATES).unstack()

        # Create a new data frame only for Budget data
        budget_df = df.xs(KEY_FOR_BUDGET_DATA)[ESSENTIAL_COLUMNS_FOR_TRANSFORMED_OUTPUT_BUDGET_DATA]

        # 2. Rename columns from unpivoted data
        unpivoted_fx_df = const_dollar_ratio_df.reset_index().rename(
             columns={
                 'level_0': YEAR_COLUMN_FX_RATES,
                 0: CONSTANT_DOLLAR_COLUMN_FX_RATES
             })

        # Merge budget_df with unpivoted_fx_df in 1 dataframe
        df = budget_df.merge(unpivoted_fx_df, left_on=['Harmonized_Year', 'Harmonized_Country'],
                             right_on=['YEAR', 'HARMONIZED_COUNTRY'])

        # 3. Remove the suffixes from constant_dollar_ratio_cols
        # unpivoted_fx_df[YEAR_COLUMN_FX_RATES] = unpivoted_fx_df[YEAR_COLUMN_FX_RATES].str.replace(CONSTANT_DOLLAR_COLUMN_SUFFIX, '')
        # current_year = str(datetime.datetime.now().year)
        # current_year_le = ''.join([current_year, 'LE'])
        # unpivoted_fx_df.loc[unpivoted_fx_df['YEAR'] == current_year, ['YEAR']] = current_year_le
        #
        # df = pd.concat([df.xs(KEY_FOR_BUDGET_DATA), unpivoted_fx_df],
        #                keys=(KEY_FOR_BUDGET_DATA,
        #                      KEY_FOR_CONSTANT_DOLLAR_RATIO_DATA))
        return df

    def apply_constant_dollar_ratios_to_budget_usd(
            self,
            df
    ):
        #Create a New column with the calculation between (Harmonized_Budget_USD * Harmonized_Constant_USD)
        df[HARMONIZED_CONSTANT_COLUMN_DATA] = df[HARMONIZED_BUDGET_COLUMN_BUDGET_DATA] * df[CONSTANT_DOLLAR_COLUMN_FX_RATES]

        return df

    def debug(self, df):
        import pdb; pdb.set_trace()
        return df