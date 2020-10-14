"""This is the subclass of Transform function for Guatemala (LATAM division).

We will define transform functions specific to Guatemala here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamGuatemalaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    GUATEMALA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*HUEVO.*": "Other",
        "(?i).*SEDAN.*": "Other",
        "(?i).*ILUMINACION.*": "Other",
        "(?i).*EQUIPO.*": "Other",
        "(?i).*BANCA\sONLINE.*": "Other",
        "(?i).*PROD\sNATURALES.*": "Other",
        "(?i).*PICK-UPS.*": "Other",
        "(?i).*FUERZA.*ARMADA.*": "Other",
        "(?i).*OTRO.*PRODUCTO.*INFANTIL.*": "Other",
        "(?i).*PAQUETE.*FIJO.*HOGAR.*": "Other",
        "(?i).*EQUIPO.*INSTRUMENTO.*MEDICO.*": "Other",
        "(?i).*ELEARNING.*": "Other",
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
            LatamGuatemalaTransformFunctions.GUATEMALA_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name
        )
