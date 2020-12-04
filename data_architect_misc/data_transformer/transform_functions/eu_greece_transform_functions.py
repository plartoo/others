"""This is the subclass of Transform function for Greece (EU division).

We will define transform functions specific to Greece here.

Author: Maicol Contreras
Last Modified: December 4, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuGreeceTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    GREECE_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Greece-specific mappings that cannot be used for other EU countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **EuGreeceTransformFunctions.GREECE_SPECIFIC_CATEGORY_MAPPINGS)
