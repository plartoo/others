"""This is the subclass of Transform function for Ukraine (AED division).

We will define transform functions specific to Ukraine here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""

import pandas as pd

from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class AedIndiaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    def __init__(self, config):
        self.config = config

    def implement_country_specific_transform_functions_in_this_file_like_this(
            self,
            df
    ):
        """Insert description here."""
        return df
