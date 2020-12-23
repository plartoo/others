"""This is the subclass of Transform function for Poland (EU division).

We will define transform functions specific to Poland here.

Author: Maicol Contreras
Last Modified: December 23, 2020
"""
from constants import comp_harm_constants
import pandas as pd
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuPolandTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    POLAND_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Poland-specific mappings that cannot be used for other EU countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **EuPolandTransformFunctions.POLAND_SPECIFIC_CATEGORY_MAPPINGS)

    @staticmethod
    def _columns_reference(columns_ref):
        # In Poland raw file, we need to validate that all columns always come with the same name
        # In some ocassions, the local agency shares with us the data with other column but the same data.
        # We make sure the name of the columns using a remap of columns.
        try:
            new_column = { 
                "klasa(2)" : "category",
                "reklamodawca" : "advertiser",
                "media" : "media type",
                "koszt [zł]" : "spend",
                "podklasa(3)" : "subcategory",
                "subbrand" : "product",
                "rate card spend in pln" : "spend",
                "data" : "date"
                }
            column = new_column[columns_ref.lower()]
        except:
            column = columns_ref
        finally:
            return column

    def join_sheets_in_a_unique_dataframe(self,df):
        columns_to_use = ['category', 'subcategory', 'brand', 'product', 'advertiser', 'date', 'media type', 'spend']
        final_df = pd.DataFrame(columns=columns_to_use)
        wb = pd.ExcelFile(self.config['current_input_file'])
        worksheets = wb.book.sheets()
        for sheet in worksheets:
            if sheet.visibility == 0 and (len(sheet.name.split())==2 and sheet.name.split()[1].isnumeric()):
                dt_to_clean = wb.parse(sheet.name,header=self.config['header'])
                columns_to_check = [EuPolandTransformFunctions._columns_reference(str(x)) for x in dt_to_clean.columns.str.lower().tolist()]
                dt_to_clean.columns = columns_to_check
                dt_to_clean.dropna(subset=columns_to_use,inplace=True)
                final_df = final_df.append(dt_to_clean[columns_to_use],sort=False)
        return final_df