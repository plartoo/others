"""This is the subclass of Transform function for Uruguay (LATAM division).

We will define transform functions specific to Uruguay here.

Author: Maicol Contreras
Last Modified: November 19, 2020
"""

import pandas as pd
import re

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamUruguayTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    URUGUAY_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*TRAPEADOR.*": "Home Care",
    }

    def __init__(self, config):
        self.config = config

    def create_the_date_column_using_the_header_inside_of_the_file(self,
                                                   df,
                                                   leave_empty_if_no_match = False
                                                   ):
        """
        Specific function in order to get the date of the data inserted in the header inside of the file.
        """
        dt_temp = pd.read_excel(self.config['current_input_file'])
        get_date = dt_temp[dt_temp.iloc[:,0].str.contains('Nombre: ')==True].dropna(axis=1).iloc[:,0].tolist()
        month_year_string = [date for date in re.split(r':',get_date[0]) if 'desde' in date or 'hasta' in date][0]
        string_to_delete = re.match(r'.*hasta*.',[date for date in re.split(r':',get_date[0]) if 'desde' in date or 'hasta' in date][0]).group()
        month_year = month_year_string.replace(string_to_delete,'')
        df['MES'] = month_year
        
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
            LatamUruguayTransformFunctions.URUGUAY_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name,
            leave_empty_if_no_match
        )
