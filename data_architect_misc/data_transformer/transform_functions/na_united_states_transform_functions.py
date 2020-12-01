"""This is the subclass of Transform function for United States (NA division).

We will define transform functions specific to United States here.

Author: Maicol Contreras
Last Modified: November 24, 2020
"""
import pandas as pd
import numpy as np
from time import strptime

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER
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
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **NaUnitedStatesTransformFunctions.UNITED_STATES_SPECIFIC_CATEGORY_MAPPINGS)

    def add_HARMONIZED_MONTH_and_HARMONIZED_YEAR_columns_by_extracting_info_from_raw_spend_column(
            self,
            df):
        """
        Function to extract Month and Year values from a spend column header 
        and create HARMONIZED_MONTH and HARMONIZED_YEAR columns out of it.

        In USA raw data files, we do not have dedicated columns for 
        Date/Month/Year, but we have a column header like this:
        'Sep 2020 (B) DOLS (000)'. This function helps extracts 
        the Month and Year info from such column header to create 
        HARMONIZED columns.
        """
        df_temp = pd.read_excel(self.config[KEY_CURRENT_INPUT_FILE],
                           header=self.config[KEY_HEADER],
                           skipfooter=self.config['skipfooter'],
                           sheet_name=self.config['input_sheet_name'])

        raw_date = [date for date in df_temp.columns.tolist() if '(B) DOLS' in date]
        df.loc[:, comp_harm_constants.MONTH_COLUMN] = strptime(raw_date[0].split(' ')[0],'%b').tm_mon
        df.loc[:, comp_harm_constants.YEAR_COLUMN] = raw_date[0].split(' ')[1]

        return df

