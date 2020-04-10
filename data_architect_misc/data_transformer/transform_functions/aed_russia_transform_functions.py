"""This is the subclass of Transform function for Russia (AED division).

We will define transform functions specific to Russia here.

Author: Phyo Thiha
Last Modified: April 7, 2020
"""

import pandas as pd

from transform_functions.transform_functions import CommonTransformFunctions


class CustomFunctions(CommonTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def implement_gcc_specific_functions_in_this_file(self,
                                                       df
                                                       )  -> pd.DataFrame:
        """
        """
        return df

