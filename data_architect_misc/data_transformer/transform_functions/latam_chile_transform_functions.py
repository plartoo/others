"""This is the subclass of Transform function for Chile (LATAM division).

We will define transform functions specific to Chile here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamChileTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    CHILE_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*ISOTONICA.*": "Other",
        "(?i).*MASA\sREFRIGERADA.*": "Other",
        "(?i).*DELIVERY\sOTROS.*": "Other",
        "(?i).*(\b)?GIN(\b)?.*": "Other",
        "(?i).*(\b)?LANA(\b)?.*": "Other",
        "(?i).*(\b)?PUERTA(\b)?.*": "Other",
        "(?i).*CECINAS.*": "Other",
        "(?i).*QUINCALLERIA.*": "Other",
        "(?i).*LINEA\sTRABAJO.*": "Other",
        "(?i).*PISCO.*": "Other",
        "(?i).*ISAPRES.*": "Other",
        "(?i).*BODEGAJE.*": "Other",
        "(?i).*GRUPO\sGENERADOR.*": "Other",
        "(?i).*CALENTADOR\sAMBIENTAL.*": "Other",
        "(?i).*COCHE.*BEBE.*": "Other",
        "(?i).*PAPEL\sMURAL.*": "Other",
        "(?i).*PREVISION\sPRIVADA.*": "Other",
        "(?i).*CORRETAJE.*": "Other",
        "(?i).*ELECTRO\sBLANCA.*": "Other",
        "(?i).*TUBO.*SANITARIO.*": "Other",

        "(?i).*TRAPEADOR.*": "Home Care",
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
            LatamChileTransformFunctions.CHILE_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name
        )
