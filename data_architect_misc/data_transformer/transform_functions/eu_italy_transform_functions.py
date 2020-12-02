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

    def create_dataframe_pivotting_the_media_date_and_spend_values(
            self,
            df):
        """
        Function to organize the data and pivot the media, date and spend columns.
        """
        df_pivot_final = pd.DataFrame()
        permanent_columns = ['Subcategory','Advertiser','Brand','Product','DATA']
        columns_concat = []
        
        df.drop(df.columns[[0]],axis=1,inplace = True) #Deleting the column 0 since there are no nnull values
        df_columns = df[0:3].fillna("") #Getting the first three original header
        df_data = df.drop(df.index[0:3],axis=0) #Getting only the data with no including the three header

        #---------- Merging the three header in just one header ---------
        for index,columns in enumerate(df_columns):
            list_string = ""
            for ind,columns_data in enumerate(df_columns[columns]):
                if columns_data != "":
                    if isinstance(columns_data, dt): 
                        columns_data = columns_data.strftime('%m-%d-%Y')
                    list_string += str(columns_data) + "_"
            list_string_long = len(list_string)
            columns_concat.append(list_string[:list_string_long - 1])
        #---------- ----------------------------------------- ---------

        df_data.columns = columns_concat #Replacing the columns in the original data with the merged columns

        """
        We will delete the GRP data due to these values are not necessary to be pivoted
        """
        df_data = df_data.loc[df_data['DATA'] == '€']

        #To validate the columns that contain values and they are going to be pivotting, it's necessary to separate them of the all header
        columns_to_pivot = [column_ok for column_ok in columns_concat if len(column_ok.split('_'))>1]

        """
        It's much better to pivot column by column because it takes a long time doing the pivotting process using all columns at the same time
        """
        for columnstomelt in columns_to_pivot:
            df_pivot_temp = pd.melt(df_data,id_vars=permanent_columns, value_vars=columnstomelt,var_name='Merged_Columns', value_name='Values')
            df_pivot_temp = df_pivot_temp.loc[df_pivot_temp['Values'] > 0] #Deleting the 0 values the data is much easier to be splitted
            #Creating the Date column and Media column using the merged columns based on its order 
            df_pivot_temp.loc[:,'Media'] = df_pivot_temp['Merged_Columns'].apply(lambda x:x.split('_')[0])
            df_pivot_temp.loc[:,'Date'] = df_pivot_temp['Merged_Columns'].apply(lambda x:x.split('_')[1])
            #Joining all interactions  in just one dataframe, this is because the local agency sometimes send us the data with more months than necessary
            df_pivot_final = df_pivot_final.append(df_pivot_temp,sort=False)

        return df_pivot_final
