"""This is the subclass of Transform function for Puerto Rico (LATAM division).

We will define transform functions specific to Puerto Rico here.

Author: Maicol Contreras
Last Modified: November 17, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamPuertoRicoTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    PUERTO_RICO_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i)STORE-HOME-FURNISHING": "Other",
        "(?i)STORE-HOME\\sIMPROVEMENT": "Other",
        "(?i)NURSING\\sHOME": "Other",
        
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamPuertoRicoTransformFunctions.PUERTO_RICO_SPECIFIC_CATEGORY_MAPPINGS)
