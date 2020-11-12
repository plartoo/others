"""This is the subclass of Transform function for Dominican Republic (LATAM division).

We will define transform functions specific to Dominican Republic here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""

import pandas as pd
import os,re
from glob import glob

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_DELIMITER, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamDominicanRepublicTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    DOMINICAN_REPUBLIC_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*TRAPEADOR.*": "Home Care",
    }

    def __init__(self, config):
        self.config = config

    def add_RAW_MEDIA_column_for_multiple_files_using_specific_string_part_of_filename(
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
            temp_df = pd.read_csv(file_path_and_name, header=self.config[KEY_HEADER]-2, delimiter=self.config[KEY_DELIMITER])
            file_name = os.path.basename(file_path_and_name)
            # REF: https://stackoverflow.com/questions/27387415/how-would-i-get-everything-before-a-in-a-string-python
            temp_df[comp_harm_constants.RAW_MEDIA_TYPE_COLUMN] = re.split(r'([_-])', file_name)[6]
            df = df.append(temp_df)

        return df

    def apply_country_specific_category_mapping_to_HARMONIZED_CATEGORY_column(self,
                                                   df,
                                                   existing_category_col_name: str,
                                                   leave_empty_if_no_match = False
                                                   ):
        """
        Helper function to invoke the common comp harm function that will help us apply
        country-specific mappings for HARMONIZED_CATEGORY column.
        """
        return self. add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            df,
            LatamDominicanRepublicTransformFunctions.DOMINICAN_REPUBLIC_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name,
            leave_empty_if_no_match
        )
