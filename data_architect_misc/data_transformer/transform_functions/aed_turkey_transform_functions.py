"""This is the subclass of Transform function for Turkey (AED division).

We will define transform functions specific to Turkey here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""

import pandas as pd

from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class AedTurkeyTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def implement_country_specific_transform_functions_in_this_file_like_this(
            self,
            df
    ):
        """Insert description here."""
        return df
