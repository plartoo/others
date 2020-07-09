"""This is the subclass of Transform function for Ukraine (AED division).

We will define transform functions specific to Ukraine here.

Author: Phyo Thiha
Last Modified: April 13, 2020
"""

import pandas as pd

from constants.comp_harm_constants import RAW_MEDIA_TYPE_COLUMN
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions
from qa_functions.common_comp_harm_qa_functions import CommonCompHarmQAFunctions


class ApacVietnamTransformFunctions(CommonCompHarmTransformFunctions, CommonCompHarmQAFunctions):

    def __init__(self, config):
        self.config = config

    def create_new_dataframe_from_given_sheet_names_and_add_media_type_column_using_sheet_name(
            self,
            df,
            list_of_sheet_names
    ):

        """
        This function is creating a new column named RAW_MEDIA_TYPE
        to include media names selected from sheet names
        also he we will append every sheet in one dataframe.
        """

        df = pd.DataFrame()
        for sheet in list_of_sheet_names:
            temp_df = pd.read_excel(
                self.config[KEY_CURRENT_INPUT_FILE],
                sheet_name=sheet,
                header=self.config[KEY_HEADER])

            # Create  RAW_MEDIA_TYPE column based on sheet names.
            temp_df[RAW_MEDIA_TYPE_COLUMN] = sheet

            # Append all sheet with same columns names,
            # those columns names that do not match will
            # be at the end of the dataframe
            # (E.g., "Header type" column).
            df = df.append(temp_df)

        return df

