"""This is the subclass of Transform function for Chile (LATAM division).

We will define transform functions specific to Chile here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamChileTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    CHILE_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Chile-specific mappings that cannot be used for other LATAM countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamChileTransformFunctions.CHILE_SPECIFIC_CATEGORY_MAPPINGS)
