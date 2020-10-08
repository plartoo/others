"""This is the subclass of Transform function for Taiwan (APAC division).

We will define transform functions specific to Taiwan here.

Author: Jholman Jaramillo
Last Modified: September 10, 2020
"""

import re
import os
import pandas as pd
from glob import glob

import transform_errors
from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_DELIMITER, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions
from qa_functions.common_comp_harm_qa_functions import CommonCompHarmQAFunctions

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

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            existing_category_col_name: str):
        """
        We have some Taiwan-specific category mappings, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **ApacTaiwanTransformFunctions.TAIWAN_SPECIFIC_CATEGORY_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match \
            (df,
             existing_category_col_name,
             comp_harm_constants.CATEGORY_COLUMN,
             category_mappings
             )
