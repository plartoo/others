"""This is the subclass of Transform function for Canada (NA division).

We will define transform functions specific to Canada here.

Author: Maicol Contreras
Last Modified: November 23, 2020
"""

import pandas as pd
import re
from datetime import datetime as dt

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_DELIMITER, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class NaCanadaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    CANADA_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Canada-specific mappings that cannot be used for other NA countries here.
    }

    def __init__(self, config):
        self.config = config
    
    def create_a_new_dataframe_using_a_pivot_table_and_validating_the_category_column(self,
                                                   df
                                                   ):
        temp_df = pd.read_excel(self.config[KEY_CURRENT_INPUT_FILE],header=self.config[KEY_HEADER],skipfooter=self.config['skipfooter'])
        temp_df.dropna(thresh=11,inplace=True)
        index_columns = ['Category', 'Company', 'Division', 'Brand', 'Media', 'Submedia',
        'Region', 'Province', 'Market', 'Month', 'Year', 'Total Media']
        columns_to_pivot = [c for c in temp_df.columns.tolist() if c not in index_columns]
        df = pd.melt(temp_df,id_vars=index_columns,value_vars=columns_to_pivot,var_name='Class',value_name='Local_Spend')
        df.dropna(subset=['Local_Spend'],inplace=True)
        df['Month'] = df['Month'].astype(int).apply(lambda x:dt.strptime(str(x),'%Y%m'))
        """
        function to organize the data and pivot the category columns that contains the spend values
        """
        return df

    def apply_country_specific_category_mapping_to_HARMONIZED_CATEGORY_column(self,
                                                   df,
                                                   existing_category_col_name: str,
                                                   leave_empty_if_no_match = False
                                                   ):
        """
        Helper function to invoke the common comp harm function that will help us apply
        country-specific mappings for HARMONIZED_CATEGORY column.
        """
        return self. add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            df,
            NaCanadaTransformFunctions.CANADA_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name,
            leave_empty_if_no_match
        )
