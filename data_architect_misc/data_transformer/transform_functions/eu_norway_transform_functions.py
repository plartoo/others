"""This is the subclass of Transform function for Norway (EU division).

We will define transform functions specific to Norway here.

Author: Maicol Contreras
Last Modified: December 21, 2020
"""
from constants import comp_harm_constants
import pandas as pd
import xlrd
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuNorwayTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    NORWAY_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Norway-specific mappings that cannot be used for other EU countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **EuNorwayTransformFunctions.NORWAY_SPECIFIC_CATEGORY_MAPPINGS)

    @staticmethod
    def _columns_reference(columns_ref):
        # In Norway raw file, we need to validate that all columns always come with the same name
        # In some ocassions, the local agency shares with us the data with other column but the same data.
        # We make sure the name of the columns using a remap of columns.
        try:
            new_column = { 
                "grossprice" : "gross"
                }
            column = new_column[columns_ref.lower()]
        except:
            column = columns_ref
        finally:
            return column

    def join_sheets_in_a_unique_dataframe(self,df):
        columns_to_use = ['category', 'subcategory', 'brand', 'product', 'advertiser', 'period', 'media channel', 'gross']
        final_df = pd.DataFrame(columns=columns_to_use)
        wb = xlrd.open_workbook(self.config['current_input_file'])
        worksheets = wb.sheet_names()
        worksheets_to_use = [sheet for sheet in worksheets if len(sheet.split())==2 and sheet.split()[1].isnumeric()]
        for worksheet in worksheets_to_use:
            if wb.sheet_by_name(worksheet).visibility == 0:
                dt_to_clean = pd.read_excel(self.config['current_input_file'],skiprows=self.config['header'],sheet_name=worksheet)
                dt_to_clean.dropna(how='all',axis=1,inplace=True) #Delete columns with NA values
                dt_to_clean.dropna(how='all',axis=0,inplace=True) #Delete rows with NA values 
                columns_to_check = [EuNorwayTransformFunctions._columns_reference(str(x)) for x in dt_to_clean.columns.str.lower().tolist()]
                dt_to_clean.columns = columns_to_check
                dt_to_clean.dropna(subset=columns_to_use,inplace=True)
                final_df = final_df.append(dt_to_clean[columns_to_use],sort=False)
        return final_df