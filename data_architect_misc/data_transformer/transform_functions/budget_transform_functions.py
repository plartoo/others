"""This is the subclass of Transform function for Switzerland.

We will define transform functions specific to Switzerland here.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""


from transform_functions.transform_functions import TransformFunctions


# class SwitzerlandTransformFunctions(TransformFunctions):
class TaskSpecificTransformFunctions(TransformFunctions):

    """
    All transform functions **SPECIFIC to individual country** must be
    defined as part of this class.
    """

    def __init__(self):

        """Always include __init__ function to make object instantiation easier."""
        """Always include __init__ function to make object instantiation easier."""
        pass


    def map_to_ecommerce(self, df, list_of_strs_to_map_to_ecommerce):
        """
        In Budget roll-up data, we need to map raw Channel names
        like 'Amazon' and 'Ecommerce' to 'E-Commerce'.

        Args:
            df: Raw dataframe to transform.
            list_of_strs_to_map_to_ecommerce: List of strings that must
            be mapped to 'E-Commerce'. E.g., ["Amazon", "Ecommerce"]

        Returns:
            Dataframe with 'E-Commerce' name in Channel column standardized.
        """
        # https://stackoverflow.com/a/20250996
        import pdb
        pdb.set_trace()
        print("map_to_ecommerce")


    def call_swiss(self):
        print("Swiss!")

