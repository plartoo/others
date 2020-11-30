"""This is the subclass of Transform function for Ukraine (AED division).

We will define transform functions specific to Ukraine here.

Author: Jholman Jaramillo
Last Modified: Nov 30, 2020
"""

from constants import comp_harm_constants
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
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **ApacIndiaTransformFunctions.INDIA_SPECIFIC_CATEGORY_MAPPINGS)

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
