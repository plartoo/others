"""This is the subclass of Transform function for Indonesia (APAC division).

We will define transform functions specific to Indonesia here.

Author: Jholman Jaramillo
Last Modified: August 3, 2020
"""

import re

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class ApacIndonesiaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    INDONESIA_SPECIFIC_CATEGORY_MAPPINGS = {

        "(?i).*Antacid.*": "Other",
        "(?i).*Adult.*Diaper.*": "Other",
        "(?i).*Apparel.*": "Other",
        "(?i).*Condiment.*": "Other",
        "(?i).*Dessert.*": "Other",

        "(?i).*Razor.*": "Other",
        "(?i).*Headache.*Remedies.*": "Other",
        "(?i).*Coffee.*": "Other",
        "(?i).*Wine.*": "Other",
        "(?i).*Liquid.*Milk.*": "Other",
        "(?i).*Online.*Services.*": "Other",
        "(?i).*Rub.*Balm.*": "Other",
        "(?i).*Seasoning.*": "Other",
        "(?i).*Snack.*": "Other",

        "(?i).*Bleach.*": "Home Care",

        "(?i).*Acne.*Treatment.*": "Personal Care",
        "(?i).*Baby.*Soap.*": "Personal Care",
        "(?i).*Baby.*talc.*": "Personal Care",
        "(?i).*Handsoap.*": "Personal Care",
        "(?i).*Toilet.*Soap.*": "Personal Care",
        "(?i).*Dishwash.*Liquids.*": "Personal Care",
        "(?i).*Eye.*Care.*": "Personal Care",
        "(?i).*Foundation.*": "Personal Care",
        "(?i).*Baby.*": "Personal Care",
        "(?i).*Perfume.*": "Personal Care",
        "(?i)Sheet.*Masks.*": "Personal Care",
        "(?i)Sun.*Products.*": "Personal Care",
        "(?i).*Talcum.*Powder.*": "Personal Care",
        "(?i).*Birth.*Control.*": "Other",

    }

    def __init__(self, config):
        self.config = config

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            existing_category_col_name: str):
        """
        We have some Indonesia-specific category mappings, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **ApacIndonesiaTransformFunctions.INDONESIA_SPECIFIC_CATEGORY_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match \
            (df,
             existing_category_col_name,
             comp_harm_constants.CATEGORY_COLUMN,
             category_mappings
             )
