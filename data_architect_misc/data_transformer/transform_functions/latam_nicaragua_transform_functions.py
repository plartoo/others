"""This is the subclass of Transform function for Nicaragua (LATAM division).

We will define transform functions specific to Nicaragua here.

Author: Maicol Contreras
Last Modified: August 3, 2020
"""

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamNicaraguaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    NICARAGUA_SPECIFIC_CATEGORY_MAPPINGS = {
            "(?i).*CREMAS\sPARA\sLA\sPIEL.*": "Personal Care",
            "(?i).*HIGIENE\sINTIMA\sFEMENINA.*": "Personal Care",
            "(?i).*HIGIENE\sPRODUCTOS\sINFANTILES.*": "Personal Care",
    }

    def __init__(self, config):
        self.config = config
    
    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            existing_category_col_name: str):
        """
        We have some Nicaragua-specific category mappings, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **LatamNicaraguaTransformFunctions.NICARAGUA_SPECIFIC_CATEGORY_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match \
            (df,
             existing_category_col_name,
             comp_harm_constants.CATEGORY_COLUMN,
             category_mappings
             )
