"""This is the subclass of Transform function for United Kingdom (EU division).

Author: Phyo Thiha
Last Modified: February 19, 2021
"""
import pandas as pd
from datetime import datetime as dt

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuUnitedKingdomTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    UK_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any country-specific mappings below.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **EuUnitedKingdomTransformFunctions.UK_SPECIFIC_CATEGORY_MAPPINGS)

