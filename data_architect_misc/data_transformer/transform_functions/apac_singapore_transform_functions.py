"""This is the subclass of Transform function for Singapore (APAC division).

We will define transform functions specific to Singapore here.

Author: Jholman Jaramillo
Last Modified: September 03, 2020
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


class ApacSingaporeTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    SINGAPORE_SPECIFIC_BRAND_MAPPINGS = {
        "(?i).*Colgate.*": "COLGATE-PALMOLIVE",
        "(?i).*Sensodyne.*": "GSK",
        "(?i).*Darlie.*": "HAWLEY & HAZEL",
        "(?i).*Oral.*B.*": "P&G",
        "(?i).*Lyon.*Systema.*": "Lion Corporation"
    }

    def __init__(self, config):
        self.config = config

    def add_RAW_BRAND_column_for_multiple_files_using_specific_string_part_of_filename(
            self,
            df,
            folder_name
    ):
        """
        For Singapore we create the raw advertiser columns selecting the name from the filename assigned,
        each file has one advertiser name in the file name, (E.g. SGP_N_ALL_INV_ADE_Colgate_20200601_20200630_20200729_JC,
        SGP_N_ALL_INV_ADE_Sensodyne_20200601_20200630_20200729_JC)
        this function will be specific for Singapore.
        """
        list_of_file_path_and_names = glob(''.join([folder_name, '/*']))

        df = pd.DataFrame()
        for file_path_and_name in list_of_file_path_and_names:
            df = pd.read_excel(file_path_and_name, header=self.config[KEY_HEADER])
            file_name = os.path.basename(file_path_and_name)
            # REF: https://stackoverflow.com/questions/27387415/how-would-i-get-everything-before-a-in-a-string-python
            df[comp_harm_constants.RAW_BRAND_COLUMN] = re.split(r'(_)', file_name)[10]
            df.to_excel(file_path_and_name, index = False)

        return df

    def borrow_brand_names_in_SG_for_HARMONIZED_ADVERTISER_column(
            self,
            df,
            existing_brand_col_name: str):
        """
        We have some Singapore-specific brand mappings, so we will
        mapped Advertisers names based on Brand column values.

        We mapped in Singapore the Advertisers using brand names because based on th brand names we can manage
        the advertiser that is the owner of this brand, we did somethinf similar in the previous process
        we used to transformer Singapore data.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        brand_mappings = dict(**ApacSingaporeTransformFunctions.SINGAPORE_SPECIFIC_BRAND_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match \
            (df,
             existing_brand_col_name,
             comp_harm_constants.ADVERTISER_COLUMN,
             brand_mappings
             )

    def add_Unknown_for_empty_values_in_Advertiser_column(
            self,
            df):
        """
        This functions was added to manage those advertiser that are not related
        to the Brand names we clasificated in the function
        "borrow_brand_names_in_SG_for_HARMONIZED_ADVERTISER_column",
        we will assign "Unknow" when using the SINGAPORE_SPECIFIC_BRAND_MAPPINGS none advertiser
        could be found for the Brand Name in the SG data
        """
        df[comp_harm_constants.ADVERTISER_COLUMN] = df[comp_harm_constants.ADVERTISER_COLUMN].replace('', "Unknow")
        return df
