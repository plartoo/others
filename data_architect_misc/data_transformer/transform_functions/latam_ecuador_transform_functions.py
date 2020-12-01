"""This is the subclass of Transform function for Ecuador (LATAM division).

We will define transform functions specific to Ecuador here.

Author: Maicol Contreras
Last Modified: October 21, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamEcuadorTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    ECUADOR_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*FORMULA.*INFANTIL.*": "Other",
        "(?i).*GOMA.*MASCAR.*": "Other",
        "(?i).*CONSULTA.*POPULAR.*": "Other",
        "(?i).*BALANCEADOS.*": "Other",
        "(?i).*MUTUALISTA.*": "Other",
        "(?i).*CONSERVAS.*": "Other",
        "(?i).*ALCOPOPS.*": "Other",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamEcuadorTransformFunctions.ECUADOR_SPECIFIC_CATEGORY_MAPPINGS)
