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

    def add_sum_of_budget_rows_for_each_region_year_and_macro_channel_pair(self,
                                                                           df,
                                                                           list_of_col_names_to_group_by,
                                                                           col_name_to_sum
                                                                           )  -> pd.DataFrame:
        """
        For each unique pair of region, year and macro channel, add a total line
        item for Budget (USD) in the dataframe.
        This is needed to create total Division-wide displays in the dashboard.
        REF: https://stackoverflow.com/q/58276169/1330974
        """
        df_grouped_and_summed = df.groupby(list_of_col_names_to_group_by)[col_name_to_sum]\
            .sum().reset_index()
        df = pd.concat([df, df_grouped_and_summed], sort=False).fillna('Total')\
            .sort_values(by=list_of_col_names_to_group_by).reset_index(drop=True)

        return df


    def add_char_in_front_of_region_names_in_total_rows(self,
                                                        df,
                                                        char_to_add_in_front):
        """
        In Tableau, the filters are sorted by alphabetical order.
        In order to make sure Division filters appear on top of the filter
        options, we need to append space character in front of Division
        total rows under 'Region' column.
        REF1: https://stackoverflow.com/a/49995329/1330974
        E.g., df.loc[df.Hub == 'Total', 'Region'] = df['Region'].apply(lambda x: f" {x}")
        REF2: https://stackoverflow.com/a/45651450/1330974
        E.g., df.loc[df.Hub == 'Total','Region'] = '*' + df[df.Hub == 'Total']['Region']
        """
        df.loc[df.Hub == 'Total', 'Region'] = df['Region'].apply(lambda x: f" {x}")

        return df


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
        return df


    # def return_int(self, df)  -> bool:
    #     # Testing if enforcing pandas dataframe as return type is successful. Pass!
    #     return 1
    #     # return pd.DataFrame(data={"a": [1, 2, 3], "b": [4, 5, 6]})
