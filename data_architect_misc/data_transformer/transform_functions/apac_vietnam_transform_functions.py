"""This is the subclass of Transform function for Ukraine (AED division).

We will define transform functions specific to Ukraine here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""

import pandas as pd

from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions
from qa_functions.common_comp_harm_qa_functions import CommonCompHarmQAFunctions


class ApacVietnamTransformFunctions(CommonCompHarmTransformFunctions, CommonCompHarmQAFunctions):

    # @staticmethod
    # def _is_contents_of_the_lists_are_in_same_order(list1, list2):
    #     for i, l1 in enumerate(list1):
    #         if l1 != list2[i]:
    #             return False
    #     return True
    #
    #
    # def assert_the_order_of_sheets_is_as_expected(
    #         self,
    #         df,
    #         list_of_expected_sheet_order,
    #         **kwargs
    # ):
    #     temp_df = pd.read_excel(
    #         kwargs[KEY_CONFIG][KEY_CURRENT_INPUT_FILE],
    #         sheet_name=None)
    #     # Unfortunately, we have to read the file again
    #     # (with all the sheets at once) and save it in a
    #     # temp_df to detect the order of the sheets in it.
    #     # Here, we expect the user to be using Python 3.7+
    #     # for dictionary to respect (keep) the order of the keys.
    #     all_sheets = temp_df.keys()
    #
    #     # First, filter out the sheets that we are not interested
    #     sheets_of_interest = [s for s in all_sheets if s in list_of_expected_sheet_order]
    #
    #     if not ApacVietnamTransformFunctions._is_contents_of_the_lists_are_in_same_order(
    #         sheets_of_interest,
    #         list_of_expected_sheet_order
    #     ):
    #         raise OrderOfListContentsDifferentError(
    #             list_of_expected_sheet_order,
    #             sheets_of_interest)
    #     return df

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
