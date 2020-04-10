"""This is the subclass of Transform function for Russia (AED division).

We will define transform functions specific to Russia here.

Author: Phyo Thiha
Last Modified: April 7, 2020
"""

import pandas as pd

from transform_functions.transform_functions import CommonTransformFunctions


class CustomTransformFunctions(CommonTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def implement_gcc_specific_functions_in_this_file(self,
                                                       df,
                                                       list_of_col_names_to_group_by,
                                                       col_name_to_sum
                                                       )  -> pd.DataFrame:
        """
        """
        return df

