"""This is the subclass of Transform function for Panama (LATAM division).

We will define transform functions specific to Panama here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamPanamaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    PANAMA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*ARTICULO.*SEX.*": "Other",
        "(?i).*ADITIVO.*LAVADO.*": "Other",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamPanamaTransformFunctions.PANAMA_SPECIFIC_CATEGORY_MAPPINGS)
