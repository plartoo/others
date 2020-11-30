"""This is the subclass of Transform function for Taiwan (APAC division).

We will define transform functions specific to Taiwan here.

Author: Jholman Jaramillo
Last Modified: September 10, 2020
"""

import re
import pandas as pd

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions

class ApacTaiwanTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    TAIWAN_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*Manual.*Powered.*TB.*": "Oral Care",

        "(?i).*Air.*Fresheners.*": "Home Care",
        "(?i).*Floor.*Cleaners.*": "Home Care",
        "(?i).*Hand.*Dish.*": "Home Care",
        "(?i).*Liquid.*Fabric.*": "Home Care",
        "(?i).*Wipes.*Tissues.*": "Home Care",

        "(?i).*Baby.*Accesories.*": "Personal Care",
        "(?i).*Body.*Fragrance.*": "Personal Care",
        "(?i).*Feminine.*Protection.*": "Personal Care",
        "(?i).*Lipsticks.*Lip.*balm.*": "Personal Care",
        "(?i).*Intimate.*Care.*": "Personal Care",
        "(?i).*Regimen.*Products.*": "Personal Care",
        "(?i).*Razor.*": "Personal Care",
        "(?i).*Shaver.*": "Personal Care",
        "(?i).*Soap.*": "Personal Care",
        "(?i).*Talcum.*Powder.*": "Personal Care"
    }

    def __init__(self, config):
        self.config = config
        # Define self.category_mappings below if we want to use
        # specific category mapping for this country
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **ApacTaiwanTransformFunctions.TAIWAN_SPECIFIC_CATEGORY_MAPPINGS)

    def create_new_dataframe_from_given_sheet_names_and_add_advertiser_or_category_column_using_sheet_name(
            self,
            df,
            colum_name_to_be_assigned):

        """
        This function is creating a new column named Advertiser
        to include advertiser names selected from sheet names
        also he we will append every sheet in one dataframe.

        Args:
            df: Raw dataframe to capitalize the beginning of each word.
            colum_name_to_be_assigned: The name of the column where the sheet names values will be assigned for Advetiser or Categories.

            - In Taiwan 'CP' raw data the sheet names have the "Advertiser" names (E.g: Sheet name: BCM-Colgate Palmolive)
            - In Taiwan 'Non CP' raw data the sheet name have the "Category" names (E.g: Sheet name: BCM-Facial Cleansers)
        """
        df = pd.DataFrame()
        excel_sheets = pd.read_excel(self.config[KEY_CURRENT_INPUT_FILE], sheet_name=None)

        for sheet in excel_sheets.keys():
            temp_df = pd.read_excel(self.config[KEY_CURRENT_INPUT_FILE], sheet_name=sheet)
            temp_df[colum_name_to_be_assigned] = re.split(r'(-)', sheet)[2]

            df = df.append(temp_df)

        return df
