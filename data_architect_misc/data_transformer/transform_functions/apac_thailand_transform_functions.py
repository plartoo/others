"""This is the subclass of Transform function for Thailand (APAC division).

We will define transform functions specific to Thailand here.

Author: Jholman Jaramillo
Last Modified: August 31, 2020
"""

import re

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class ApacThailandTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    THAILAND_SPECIFIC_CATEGORY_MAPPINGS = {

        "(?i).*Baby.*Product.*": "Personal Care",
        "(?i).*Colourant.*": "Personal Care",
        "(?i).*Facial.*Cleanser.*": "Personal Care",
        "(?i).*Facial.*Moisturizing.*": "Personal Care",
        "(?i).*Fragrance.*": "Personal Care",
        "(?i)Hair.*": "Personal Care",
        "(?i).*Lip.*": "Personal Care",
        "(?i).*Make.*Up.*": "Personal Care",
        "(?i).*Personal.*Product.*": "Personal Care",
        "(?i).*Skincare.*": "Personal Care",
        "(?i).*Soap.*": "Personal Care",
        "(?i).*Sunblock.*": "Personal Care",
        "(?i)Toiletries.*Product.*": "Personal Care",
        "(?i).*Talcum.*": "Personal Care",

        "(?i).*Air.*Freshener.*": "Home Care",
        "(?i).*Bleach.*": "Home Care",
        "(?i).*Dishwashing.*": "Home Care",
        "(?i).*Deodorizer.*": "Home Care",
        "(?i).*Fabric.*Softener.*": "Home Care",
        "(?i).*Floor.*Cleaner.*": "Home Care",
        "(?i).*Toilet.*Cleaner.*": "Home Care",
        "(?i)Multi.*Purpose.*Cleaner.*": "Home Care",

        "(?i).*Breath.*Refreshment.*": "Oral Care",

        "(?i).*Glasses.*": "Other",
        "(?i).*Sponges.*": "Other",
        "(?i).*Scouring.*Pads.*": "Other"
    }

    def __init__(self, config):
        self.config = config

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            existing_category_col_name: str):
        """
        We have some Thailand-specific category mappings, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **ApacThailandTransformFunctions.THAILAND_SPECIFIC_CATEGORY_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match \
            (df,
             existing_category_col_name,
             comp_harm_constants.CATEGORY_COLUMN,
             category_mappings
             )

