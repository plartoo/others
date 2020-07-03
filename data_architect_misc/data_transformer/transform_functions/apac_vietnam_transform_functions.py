"""This is the subclass of Transform function for Ukraine (AED division).

We will define transform functions specific to Ukraine here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""

import pandas as pd

from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class AedUkraineTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    def combining_multiple_excel_worksheets_data_into_one_excel_worksheet(
            self,
            df):
        """
        We will join the worksheets in one worksheet.
        """
        return df
