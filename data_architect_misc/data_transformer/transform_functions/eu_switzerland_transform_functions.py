"""This is the subclass of Transform function for Switzerland (EU division).

We will define transform functions specific to Switzerland here.

Author: Maicol Contreras
Last Modified: December 21, 2020
"""
from constants import comp_harm_constants
import pandas as pd
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class EuSwitzerlandTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    SWITZERLAND_SPECIFIC_CATEGORY_MAPPINGS = {
        # Add any Switzerland-specific mappings that cannot be used for other EU countries here.
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.ENGLISH_CATEGORY_MAPPINGS,
            **comp_harm_constants.GERMAN_CATEGORY_MAPPINGS,
            **EuSwitzerlandTransformFunctions.SWITZERLAND_SPECIFIC_CATEGORY_MAPPINGS)

    def unpivot_month_columns_with_spend_values(self,df):
        columns_to_use = ['Branche','Produktgruppe','Produktsegment','Produkt','Marke','Firma','Werbungtreibender',
        'Mediengruppe','Verlag/Vermarkter','Sprachgebiet']
        final_df = pd.DataFrame()

        #Merging the headers
        df.columns = [str(x) if str(y)=='CHF' else  str(y) for x, y in df[0:1].squeeze().iteritems()]
        df = df.iloc[1:]
        
        #Delete the grand total columns or columns year
        column_year = [column_type for column_type in df.columns.tolist() if column_type.isdigit()]
        df = df.drop(columns=column_year,axis=1)

        ##Melt or unpivot dataframe table
        final_df = pd.melt(df, id_vars = columns_to_use, var_name = 'Date', value_name = 'Local_Spend')

        return final_df