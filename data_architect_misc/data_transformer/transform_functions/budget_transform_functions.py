"""This is the subclass of Transform function for Switzerland.

We will define transform functions specific to Switzerland here.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""

import pandas as pd

from transform_functions.common_transform_functions import CommonTransformFunctions


class CustomFunctions(CommonTransformFunctions):
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


    def capitalize_market_name_if_they_are_the_same_as_region_name(self,
                                                                   df) -> pd.DataFrame:
        """
        Neel decided that in Tableau dashboard market filters, we want to show
        'Division' values with capitalized letters so that users can select them
        to see the total division value (although there's already 'All' option
        to choose in market filter).

        This method make sure that the region values that are copied to market
        columns are capitalized.
        """
        df.loc[df.Region == df.Market, 'Market'] = df['Market'].apply(lambda x: x.upper())

        return df

