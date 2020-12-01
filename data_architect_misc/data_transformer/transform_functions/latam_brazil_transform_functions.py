"""This is the subclass of Transform function for Brazil (LATAM division).

We will define transform functions specific to Brazil here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamBrazilTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    BRAZIL_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Brazil-specific mappings that cannot be used for other LATAM countries here.
    }

    def __init__(self, config):
        self.config = config
        # Define self.category_mappings below if we want to use
        # specific category mapping for this country
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamBrazilTransformFunctions.BRAZIL_SPECIFIC_CATEGORY_MAPPINGS)
