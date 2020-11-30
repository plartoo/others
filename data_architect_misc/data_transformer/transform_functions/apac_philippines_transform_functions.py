"""This is the subclass of Transform function for Philippines (APAC division).

We will define transform functions specific to Malaysia here.

Author: Jholman Jaramillo
Last Modified: Nov 30, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class ApacPhilippinesTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def __init__(self, config):
        self.config = config
        self.category_mappings = comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS
