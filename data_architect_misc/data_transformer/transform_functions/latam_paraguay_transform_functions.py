"""This is the subclass of Transform function for Paraguay (LATAM division).

We will define transform functions specific to Paraguay here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamParaguayTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    PARAGUAY_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Paraguay-specific mappings that cannot be used for other LATAM countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamParaguayTransformFunctions.PARAGUAY_SPECIFIC_CATEGORY_MAPPINGS)
