"""This is the subclass of Transform function for Costa_Rica (LATAM division).

We will define transform functions specific to Costa_Rica here.

Author: Maicol Contreras
Last Modified: October 15, 2020
"""

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamCostaRicaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    COSTA_RICA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*AUTOLAVADO.*": "Other",
        "(?i).*FUMIGADOR.*": "Other",
        "(?i).*ESCOLAR.*": "Other",
        "(?i).*PARASICOLOGIA.*": "Other",
        "(?i).*ANCIANO.*": "Other",
        "(?i).*PROGRAMACION.*": "Other",
        "(?i).*HIGIENE\sINSTITUCIO.*": "Other",
        "(?i).*ESTRENIMIENTO.*": "Other",
        "(?i).*OPERADORES\sMOV\sFUL.*": "Other",
        "(?i).*PARAGUERIAS.*": "Other",
        "(?i).*VARIOS.*": "Other",
        "(?i).*(\b)?MASA(\b)?.*": "Other",
        "(?i).*(\b)?MENTA(\b)?.*": "Other",
        "(?i).*CONTRADROGA.*": "Other",
        "(?i).*DISCOMOVILES.*": "Other",
        "(?i).*COURIER.*": "Other",
        "(?i).*BEBE.*GENERICO.*": "Other",
        "(?i).*CENTRO.*COM.*OTROS.*": "Other",
    }

    def __init__(self, config):
        self.config = config

    def apply_country_specific_category_mapping_to_HARMONIZED_CATEGORY_column(
            self,
            df,
            existing_category_col_name: str):
        """
        Helper function to invoke the common comp harm function that will help us apply
        country-specific mappings for HARMONIZED_CATEGORY column.
        """
        return self. add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            df,
            LatamCostaRicaTransformFunctions.COSTA_RICA_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name
        )
