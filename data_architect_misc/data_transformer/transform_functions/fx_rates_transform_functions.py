"""This is the subclass of Transform function for Turkey (AED division).

We will define transform functions specific to Turkey here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""
import datetime
import re

import pandas as pd
import numpy as np

from transform_functions.common_transform_functions import CommonTransformFunctions
from qa_functions.common_post_transform_qa_functions import CommonPostTransformQAFunctions
from qa_functions.qa_errors import InsufficientNumberOfColumnsError, InvalidValueFoundError, UnexpectedColumnNameFound


class FxRatesTransformFunctions(CommonTransformFunctions, CommonPostTransformQAFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def select_desired_columns(self,
                               df) -> pd.DataFrame:
        """
        We only need Actual and Estimated FX rate columns
        in addition to 'COUNTRY' name column.
        """
        desired_cols = ['COUNTRY'] \
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
        if 'COUNTRY' != df.columns.tolist()[0]:
            raise UnexpectedColumnNameFound(
                f"The first column in the dataframe is not 'COUNTRY'. "
                f"The other transfrom functions rely on the first column "
                f"being 'COUNTRY'. Please fix it in the raw data file "
                f"and rerun the code."
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

        first_days_of_all_months = ['-'.join([str(year),str(i),'1'])
                                    for i in range(1,13)]
        yyyy_mm_dd = [datetime.datetime.strptime(d,'%Y-%m-%d').strftime('%Y-%m-%d') for d in first_days_of_all_months]
        # ASSUMPTION: we assume that the first column is 'COUNTRY'
        month_cols = df.columns.tolist()[1:]
        old_to_new_name_dict = dict(zip(month_cols, yyyy_mm_dd))

        return self.rename_columns(df, old_to_new_name_dict)

    def unpivot_fx_data(self,
                        df) -> pd.DataFrame:
        # REF: https://stackoverflow.com/a/18259236/1330974
        # First, set the index to COUNTRY column then unstack
        df1 = df1=df.set_index('COUNTRY')
        df2 = df1.unstack().reset_index(name='FX_Rates')

        return self.rename_columns(df2, {'level_0': 'DATE'})

    # def debug(
    #         self,
    #         df
    # ) -> pd.DataFrame:
    #     import pdb
    #     pdb.set_trace()
    #     return df
# ,
#             {
#                 "function_name": "debug",
#                 "function_args": ""
#             }