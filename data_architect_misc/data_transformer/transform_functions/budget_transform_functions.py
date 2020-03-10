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
    def set_originally_null_region_to_values_when_market_is_one_of_the_matching_values(
            self,
            df,
            region_value_to_set,
            list_of_matching_market_values
    )  -> pd.DataFrame:
        """
        In Budget roll-up data, there are lines with region as NULL.
        We must set 'Region' for these lines to something specific if
        their corresponding 'Market' values are one in
        list_of_matching_market_values.
        For example, in Budget roll-up file, some of the "Region" values
        are NULL. For them, if the "Market" value is one of the followings:
        ["AA", "Canada", "US"], we set the "Region" value to "North America"
        REF: https://stackoverflow.com/q/51787247

        Args:
            df: Raw dataframe to transform.
            region_value_to_set: Region value that must be set if corresponding
            values in 'Market' column is met AND the original 'Region' value is NULL.
            list_of_matching_market_values: If the current row consists of one of
            these market values in the list AND if the row's "Region" value is NULL,
            we set the value of "Region" to region_value_to_set.

            E.g., if we want 'Amazon' and 'Ecommerce' to be mapped to 'E-Commerce'
            we should provide {"Amazon": "E-Commerce", "Ecommerce": "E-Commerce"}

        Returns:
            Dataframe with Region value set to something (not NULL).
        """
        print("map_macrochannel_to_ecommerce")
        #TODO: fix this so that we check value in Channel and change value in another column
        return df


    def create_new_column_based_on_another_column_values(self,
                                                         df,
                                                         new_col_name,
                                                         existing_col_name,
                                                         mappings):
        df[new_col_name] = mappings[df[existing_col_name]]
        import pdb
        pdb.set_trace()

    # def return_int(self, df)  -> bool:
    #     # Testing if enforcing pandas dataframe as return type is successful. Pass!
    #     return 1
    #     # return pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
