"""This is the subclass of Transform function for Canada (NA division).

We will define transform functions specific to Canada here.

Author: Maicol Contreras
Last Modified: November 23, 2020
"""
import pandas as pd
from datetime import datetime as dt

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class NaCanadaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    CANADA_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Canada-specific mappings that cannot be used for other NA countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **NaCanadaTransformFunctions.CANADA_SPECIFIC_CATEGORY_MAPPINGS)

    def create_a_new_dataframe_using_a_pivot_table_and_validating_the_category_column(
            self,
            df):
        """
        Function to organize the data and pivot the category columns that contain spend values.
        """
        temp_df = pd.read_excel(self.config[KEY_CURRENT_INPUT_FILE],
                                header=self.config[KEY_HEADER],
                                skipfooter=self.config['skipfooter'])
        temp_df.dropna(thresh=11,inplace=True)
        index_columns = [
            'Category', 'Company', 'Division', 'Brand', 'Media', 'Submedia',
            'Region', 'Province', 'Market', 'Month', 'Year', 'Total Media']
        columns_to_pivot = [c for c in temp_df.columns.tolist() if c not in index_columns]

        df = pd.melt(temp_df,id_vars=index_columns,
                     value_vars=columns_to_pivot,
                     var_name='Class',
                     value_name='Local_Spend')
        df.dropna(subset=['Local_Spend'],inplace=True)
        df['Month'] = df['Month'].astype(int).apply(lambda x:dt.strptime(str(x),'%Y%m'))

        return df
