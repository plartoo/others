"""This is the subclass of Transform function for Ecuador (LATAM division).

We will define transform functions specific to Ecuador here.

Author: Maicol Contreras
Last Modified: October 21, 2020
"""

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamEcuadorTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    ECUADOR_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*FORMULA.*INFANTIL.*": "Other",
        "(?i).*GOMA.*MASCAR.*": "Other",
        "(?i).*CONSULTA.*POPULAR.*": "Other",
        "(?i).*BALANCEADOS.*": "Other",
        "(?i).*MUTUALISTA.*": "Other",
        "(?i).*CONSERVAS.*": "Other",
        "(?i).*ALCOPOPS.*": "Other",
    }

    def __init__(self, config):
        self.config = config

    def apply_country_specific_category_mapping_to_HARMONIZED_CATEGORY_column(self,
                                                   df,
                                                   existing_category_col_name: str
                                                   ):
        """
        Helper function to invoke the common comp harm function that will help us apply
        country-specific mappings for HARMONIZED_CATEGORY column.
        """
        return self. add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            df,
            LatamEcuadorTransformFunctions.ECUADOR_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name
        )
