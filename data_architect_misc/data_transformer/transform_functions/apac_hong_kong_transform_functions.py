"""This is the subclass of Transform function for Hong Kong (APAC division).

We will define transform functions specific to Hong Kong here.

Author: Phyo Thiha
Last Modified: Nov 30, 2020
"""
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
        "(?i).*Dermatology.*": "Other",
        "(?i).*Humidifier.*Dehumidifier.*": "Other",
        "(?i).*Hepatic.*": "Other",
        "(?i).*Heart.*Internal.*Circulation.*": "Other",
        "(?i).*Razor.*": "Other",
        "(?i).*Sauce.*Dressing.*Ingredients.*": "Other",
        "(?i).*Soup.*": "Other",
        "(?i).*Tea.*": "Other",

        "(?i)Tissue.*Napkins.*": "Home Care",

        "(?i)Baby.*Products.*": "Personal Care",
        "(?i)Children.*Supplements.*": "Personal Care",
        "(?i)Cleansers.*Toners.*": "Personal Care",
        "(?i).*Eye.*Care.*": "Personal Care",
        "(?i).*Foundation.*": "Personal Care",
        "(?i)Perfume.*Fragrance.*": "Personal Care",
        "(?i)Sheet.*Masks.*": "Personal Care",
        "(?i)Sun.*Products.*": "Personal Care",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **ApacHongKongTransformFunctions.HONG_KONG_SPECIFIC_CATEGORY_MAPPINGS)
