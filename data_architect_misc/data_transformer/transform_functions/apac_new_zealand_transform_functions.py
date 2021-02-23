"""This is the subclass of Transform function for New Zealand (APAC division).

Author: Phyo Thiha
Last Modified: February 23, 2021
"""
import pandas as pd
from datetime import datetime as dt

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class APACNewZealandTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    NZ_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any country-specific mappings below.
        "(?i).*Cleansers.*Polishers.*": "Home Care",

        # Normally, 'Sanitary' is a vague word, but in New Zealand, it seems like
        # it is consistently feminine sanitary products
        "(?i).*Sanitary Products.*": "Personal Care",

        "(?i).*Cookware.*": "Other",
        "(?i).*Discounters.*Warehouses.*": "Other",
        "(?i).*Disinfectants.*": "Other",
        "(?i).*Ice Cream.*": "Other",
        "(?i).*Insecticides.*": "Other",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **APACNewZealandTransformFunctions.NZ_SPECIFIC_CATEGORY_MAPPINGS)

