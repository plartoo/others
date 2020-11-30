"""
This is the subclass of Transform function for Malaysia (APAC division).

We will define transform functions specific to Malaysia here.

Author: Phyo Thiha
Last Modified: Nov 30, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class ApacMalaysiaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    MALAYSIA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*Digestive.*.*": "Other",
        "(?i).*Respiratory.*": "Other",
        "(?i).*Tea.*": "Other",
        "(?i).*JAM.*SPREADS.*": "Other",
        "(?i).*HEADACHE.*": "Other",

        "(?i)Air.*care.*": "Home Care",

        "(?i)Bath.*Additives.*": "Personal Care",
    }

    def __init__(self, config):
        self.config = config
        # Define self.category_mappings below if we want to use
        # specific category mapping for this country
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **ApacMalaysiaTransformFunctions.MALAYSIA_SPECIFIC_CATEGORY_MAPPINGS)
