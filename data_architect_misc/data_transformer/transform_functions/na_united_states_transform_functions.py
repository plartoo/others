"""This is the subclass of Transform function for United States (NA division).

We will define transform functions specific to United States here.

Author: Maicol Contreras
Last Modified: November 24, 2020
"""

import pandas as pd
import re
import numpy as np
from time import strptime

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_DELIMITER, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class NaUnitedStatesTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    UNITED_STATES_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any United States-specific mappings that cannot be used for other NA countries here.
    }

    def __init__(self, config):
        self.config = config

    def create_a_new_date_column_based_taking_the_date_from_the_TOTAL_column(self,
                                                   df
                                                   ):
        df = pd.read_excel(self.config[KEY_CURRENT_INPUT_FILE],header=self.config[KEY_HEADER],skipfooter=self.config['skipfooter'],sheet_name=self.config['input_sheet_name'])
        raw_date = [date for date in df.columns.tolist() if '(B) DOLS' in date]
        df.insert(len(df.columns)-1,column='MONTH',value=np.nan)
        df.insert(len(df.columns)-1,column='YEAR',value=np.nan)
        df.loc[:,'MONTH'] = strptime(raw_date[0].split(' ')[0],'%b').tm_mon
        df.loc[:,'YEAR'] = raw_date[0].split(' ')[1]

        """
        function to create a date column getting the date range from the Total column
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
            NaUnitedStatesTransformFunctions.UNITED_STATES_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name,
            leave_empty_if_no_match
        )
