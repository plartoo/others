"""This is the subclass of Transform function for Ukraine (AED division).

We will define transform functions specific to Ukraine here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""

import pandas as pd

from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions
from qa_functions.common_comp_harm_qa_functions import CommonCompHarmQAFunctions


class ApacVietnamTransformFunctions(CommonCompHarmTransformFunctions, CommonCompHarmQAFunctions):

    def load_data_from_another_sheet_in_excel_file_and_append_to_the_main_dataframe(
            self,
            df,
            *args,
            **kwargs
    ):
        import pdb;
        pdb.set_trace()
        return df

    def debug(
            self,
            df,
            **kwargs
    ):

        import pdb; pdb.set_trace()
        return df
