"""This is the subclass of Transform function for France (Eu division).

We will define transform functions specific to France here.

Author: Maicol Contreras
Last Modified: December 2, 2020
"""
import pandas as pd

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuFranceTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    FRANCE_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any France-specific mappings that cannot be used for other EU countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ITALIAN_CATEGORY_MAPPINGS,
            **EuFranceTransformFunctions.FRANCE_SPECIFIC_CATEGORY_MAPPINGS)

    @staticmethod
    def _columns_reference(columns_ref):
        # In France raw file, we need to validate that all columns always come with the same name
        # In some ocassions, the local agency shares with us the data with other column but the same data.
        # We make sure the name of the columns using a remap of columns.
        try:
            new_column = { 
                "SPEND (K€)" : "SPEND", 
                "SPEND (€)" : "SPEND"
                }
            column = new_column[columns_ref.upper()]
        except:
            column = columns_ref
        finally:
            return column

    def merge_all_sheets_in_just_one_datraframe(
            self,
            df):
        """
        Function to reshape the France raw data which comes in different sheets. The idea is to get 
        The main sheets and then join all these sheets in one dataframe.
        """        
        general_columns = ["CATEGORY","BRAND","PRODUCT","ADVERTISER","MEDIA TYPE","YEAR","MONTH","SPEND"]
        final_df = pd.DataFrame(columns=general_columns)
        worsheets_to_use = ["Print","TV","Display-Cinema-OOH-TV Sponso","Radio"]
        for sheets in worsheets_to_use:
            dt = pd.read_excel(self.config["current_input_file"],sheet_name = sheets)
            dt.dropna(axis=0,subset=['DAY'],inplace=True)
            dt.columns = [EuFranceTransformFunctions._columns_reference(x) for x in dt.columns]
            dt = dt[general_columns]
            dt.YEAR = dt.YEAR.astype(int)
            final_df = final_df.append(dt,sort=False)
        return final_df
