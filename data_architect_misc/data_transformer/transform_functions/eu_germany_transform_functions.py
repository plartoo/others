"""This is the subclass of Transform function for Germany (EU division).

We will define transform functions specific to Germany here.

Author: Maicol Contreras
Last Modified: December 3, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuGermanyTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    GERMANY_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Germany-specific mappings that cannot be used for other EU countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.GERMAN_CATEGORY_MAPPINGS,
            **EuGermanyTransformFunctions.GERMANY_SPECIFIC_CATEGORY_MAPPINGS)
