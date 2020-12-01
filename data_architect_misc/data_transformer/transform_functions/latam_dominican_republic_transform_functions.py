"""This is the subclass of Transform function for Dominican Republic (LATAM division).

We will define transform functions specific to Dominican Republic here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""

import pandas as pd
import os,re
from glob import glob

from constants import comp_harm_constants
from constants.transform_constants import KEY_DELIMITER, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamDominicanRepublicTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    DOMINICAN_REPUBLIC_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Dominican Republic-specific mappings that cannot be used for other LATAM countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamDominicanRepublicTransformFunctions.DOMINICAN_REPUBLIC_SPECIFIC_CATEGORY_MAPPINGS)

    def add_RAW_MEDIA_column_for_multiple_files_using_specific_string_part_of_filename(
            self,
            df,
            folder_name
    ):
        """
        For Dominican Republic, we create the raw media type column by extracting
        part of file name. For example, if the raw file name is:
        DOM_N_M-Radio_ALL_ARI_20200901_20200930_20201103_NM.xlsx
        we will extract 'Radio' and put it under HARMONIZED_MEDIA_TYPE column.

        If the file name does not conform to the standard and this code
        extracted unexpected media type, the QA process will catch it.
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
