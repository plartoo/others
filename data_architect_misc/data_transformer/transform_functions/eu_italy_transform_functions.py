"""This is the subclass of Transform function for Italy (Eu division).

We will define transform functions specific to Italy here.

Author: Maicol Contreras
Last Modified: December 2, 2020
"""
import pandas as pd
from datetime import datetime as dt

from constants import comp_harm_constants
from constants.transform_constants import KEY_CURRENT_INPUT_FILE, KEY_HEADER
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuItalyTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    ITALY_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Italy-specific mappings that cannot be used for other EU countries here.
        "(?i).*ANTICALCARE.*": "Home Care",
        "(?i).*GESTIONE.*CASA.*": "Home Care",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ITALIAN_CATEGORY_MAPPINGS,
            **EuItalyTransformFunctions.ITALY_SPECIFIC_CATEGORY_MAPPINGS)

    @staticmethod
    def _merge_dataframe_columns_into_strings(df_columns):
        # In Italy raw file, we read the first three lines of data including 
        # Media Type, Month-Year and Spot Length. We will combine these into 
        # something like, 'Television_07-01-2020_10' so that we can eventually 
        # unpivot them and split them back into three separate columns.
        concatenated_col_names = []
        for i, columns in enumerate(df_columns):
            str_to_combine = []
            for j, columns_data in enumerate(df_columns[columns]):
                if columns_data:
                    if isinstance(columns_data, dt): 
                        columns_data = columns_data.strftime('%m-%d-%Y')
                    str_to_combine.append(columns_data)
            concatenated_col_names.append('_'.join(str_to_combine))

        return concatenated_col_names

    def create_dataframe_pivotting_the_media_date_and_spend_values(
            self,
            df):
        """
        Function to reshape the Italy raw data which comes in with 
        Media Type, Month-Year and Spot Length preceding the actual 
        column headers.
        """        
        df.drop(df.columns[[0]],axis=1,inplace = True) # Deleting the first column because it is empty
        df_columns = df[0:3].fillna("") # Read the first three rows that include Media type, Month-Year and Spot Length
        df_data = df.drop(df.index[0:3],axis=0) # Read the data frame without the first three rows above

        # Rename the column names with Spot Length to the names which is concatenated version of 
        # Media Type, Month-Year and Spot Length (e.g., 'Television_07-01-2020_10')
        col_names_after_str_concat = EuItalyTransformFunctions._merge_dataframe_columns_into_strings(df_columns)
        df_data.columns = col_names_after_str_concat

        # Keep only the rows with spend data in it (in other words, discard the GRP rows)
        df_data = df_data.loc[df_data['DATA'] == '€']

        # When we updated the column names by concatenating them with '_' above, 
        # we included the column names such as 'Sector', 'Subsector', ..., 'Product'. 
        # We don't need to unpivot them, so we will leave them out with the filter below.
        cols_to_unpivot = [c for c in col_names_after_str_concat if '_' in c]

        # Note: We are unpivoting column by column because it takes a long time 
        # to unpivot them at once (in one function call)
        df_unpivotted = pd.DataFrame()
        pivoted_columns = ['Subcategory','Advertiser','Brand','Product','DATA']
        for columnstomelt in cols_to_unpivot:
            df_unpivot_temp = pd.melt(df_data, id_vars=pivoted_columns, value_vars=columnstomelt, var_name='Merged_Columns', value_name='Values')
            df_unpivot_temp = df_unpivot_temp.loc[df_unpivot_temp['Values'] > 0] # Keep only the values with spend > 0 

            # Creating the Date and Media columns from the combined string column created in earlier steps above
            df_unpivot_temp.loc[:, 'Media'] = df_unpivot_temp['Merged_Columns'].apply(lambda x:x.split('_')[0])
            df_unpivot_temp.loc[:, 'Date'] = df_unpivot_temp['Merged_Columns'].apply(lambda x:x.split('_')[1])

            # Keep adding unpivotted data back to the final dataframe that is to be returned
            df_unpivotted = df_unpivotted.append(df_unpivot_temp, sort=False)

        return df_unpivotted
