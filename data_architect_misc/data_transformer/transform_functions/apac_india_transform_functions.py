"""This is the subclass of Transform function for Ukraine (AED division).

We will define transform functions specific to Ukraine here.

Author: Jholman Jaramillo
Last Modified: July 10, 2020
"""

import re

import pandas as pd

from constants import comp_harm_constants
from transform_errors import ExpectedColumnNotFoundError
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class ApacIndiaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    INDIA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*Auto.*": "Other",
        "(?i).*Media.*": "Other",
        "(?i).*Services.*": "Other",
        "(?i).*Corporate.*Brand.*Image.*": "Other"
    }

    def __init__(self, config):
        self.config = config

    def assert_that_actual_tam_cost_column_exists(
            self,
            df,
            regex_for_expected_column :str
    ):
        """
        In India, the guy who prepares raw data for us does NOT
        keep the cost column names consistent. So we need to
        always check and pick the right column for the actual
        cost.

        **The actual cost column should contain spend values
        that are multiplied with 1000 already.** Usually,
        that column name has 'Actual .* Cost' in it.
        """
        return self.check_expected_columns_are_present_by_using_regex(
            df,
            regex_for_expected_column
        )

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            existing_category_col_name: str):
        """
        We have some india-specific category mappings, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **ApacIndiaTransformFunctions.INDIA_SPECIFIC_CATEGORY_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match\
                (df,
                 existing_category_col_name,
                 comp_harm_constants.CATEGORY_COLUMN,
                 category_mappings
                 )