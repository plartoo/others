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
