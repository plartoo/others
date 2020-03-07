"""This is the subclass of Transform function for Switzerland.

We will define transform functions specific to Switzerland here.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import pandas as pd

from transform_functions.transform_functions import CommonTransformFunctions


class CustomTransformFunctions(CommonTransformFunctions):

    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """

    # def __init__(self):
    #
    #     """Always include __init__ function to make object instantiation easier."""
    #     """Always include __init__ function to make object instantiation easier."""
    #     pass


    def map_macrochannel_to_ecommerce(self, df, dictionary_of_mappings)  -> pd.DataFrame:
        """
        In Budget roll-up data, if we see Channel values like 'Amazon'
        and 'Ecommerce', we should set Macro Channel values to 'E-Commerce'.

        Args:
            df: Raw dataframe to transform.
            dictionary_of_mappings: Dictionary of keys representing original
            values and values representing desired values.
            E.g., if we want 'Amazon' and 'Ecommerce' to be mapped to 'E-Commerce'
            we should provide {"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}

        Returns:
            Dataframe with 'E-Commerce' name in Channel column standardized.
        """
        # https://stackoverflow.com/a/20250996
        # import pdb
        # pdb.set_trace()
        print("map_macrochannel_to_ecommerce")
        df['Channel'] = df['Channel'].map(dictionary_of_mappings).fillna(df['Channel'])
        #TODO: fix this so that we check value in Channel and change value in another column
        return df


    # def return_int(self, df)  -> bool:
    #     # Testing if enforcing pandas dataframe as return type is successful. Pass!
    #     return 1
    #     # return pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
