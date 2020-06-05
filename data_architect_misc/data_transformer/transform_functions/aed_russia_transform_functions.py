"""This is the subclass of Transform function for Russia (AED division).

We will define transform functions specific to Russia here.

Author: Phyo Thiha
Last Modified: April 7, 2020
"""

import pandas as pd

from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class AedRussiaTransformFunctions(CommonCompHarmTransformFunctions):
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


