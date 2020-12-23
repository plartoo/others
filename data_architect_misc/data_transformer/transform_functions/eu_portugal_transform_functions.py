"""This is the subclass of Transform function for Portugal (EU division).

We will define transform functions specific to Portugal here.

Author: Maicol Contreras
Last Modified: December 23, 2020
"""
from constants import comp_harm_constants
import pandas as pd
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuPortugalTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    PORTUGAL_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Portugal-specific mappings that cannot be used for other EU countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **EuPortugalTransformFunctions.PORTUGAL_SPECIFIC_CATEGORY_MAPPINGS)