"""This is the subclass of Transform function for Russia (AED division).

We will define transform functions specific to Russia here.

Author: Phyo Thiha
Last Modified: April 7, 2020
"""

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class AedRussiaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    RUSSIA_SPECIFIC_CATEGORY_MAPPINGS = {
            "OC/PC": "Oral Care",
            "OC/HC/PC": "Oral Care",
            "HC/PC": "Oral Care"
        }

    def __init__(self, config):
        self.config = config
        # Define self.category_mappings below if we want to use
        # specific category mapping for this country
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **AedRussiaTransformFunctions.RUSSIA_SPECIFIC_CATEGORY_MAPPINGS)

