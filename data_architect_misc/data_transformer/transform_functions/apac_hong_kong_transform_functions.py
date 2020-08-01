"""This is the subclass of Transform function for Hong Kong (APAC division).

We will define transform functions specific to Hong Kong here.

Author: Jholman Jaramillo
Last Modified: July 30, 2020
"""

import re

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class ApacHongKongTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    HONG_KONG_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*Birth.*Control.*": "Other",
        "(?i).*Condom.*": "Other",
        "(?i).*Contact.*Lens.*Cleansers.*": "Other",
        "(?i).*Humidifier.*Dehumidifier.*": "Other",
        "(?i).*Hepatic.*": "Other",
        "(?i).*Heart.*Internal.*Circulation.*": "Other",
        "(?i).*Razor.*": "Other",
        "(?i).*Sauce.*Dressing.*Ingredients.*": "Other",
        "(?i).*Soup.*": "Other",
        "(?i).*Tea.*": "Other",

        "(?i)Tissue.*Napkins.*": "Home Care",

        "(?i)Sun.*Products.*": "Personal Care",
        "(?i)Cleansers.*Toners.*": "Personal Care",
        "(?i)Baby.*Products.*": "Personal Care",
        "(?i)Sheet.*Masks.*": "Personal Care",
        "(?i)Children.*Supplements.*": "Personal Care",
        "(?i)Perfume.*Fragrance.*": "Personal Care",
    }

    def __init__(self, config):
        self.config = config

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            existing_category_col_name: str):
        """
        We have some malaysia-specific category mappings, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **ApacHongKongTransformFunctions.HONG_KONG_SPECIFIC_CATEGORY_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match \
            (df,
             existing_category_col_name,
             comp_harm_constants.CATEGORY_COLUMN,
             category_mappings
             )