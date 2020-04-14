"""This is the subclass of Transform function for Kazakhstan (AED division).

We will define transform functions specific to Kazakhstan here.

Author: Maicol Contreras
Last Modified: April 13, 2020
"""

import pandas as pd

from transform_functions.comp_harm_transform_functions import CommonCompHarmTransformFunctions


class CustomFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def implement_country_specific_transform_functions_in_this_file_like_this(
            self,
            df
    ) -> pd.DataFrame:
        """Insert description here."""
        return df
