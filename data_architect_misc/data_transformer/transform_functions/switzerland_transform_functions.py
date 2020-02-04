"""This is the subclass of Transform function for Switzerland.

We will define transform functions specific to Switzerland here.

Author: Phyo Thiha
Last Modified: Jan 30, 2020
"""


from transform_functions.transform_functions import TransformFunctions


# class SwitzerlandTransformFunctions(TransformFunctions):
class CountrySpecificTransformFunctions(TransformFunctions):

    """
    All transform functions **SPECIFIC to individual country** must be
    defined as part of this class.
    """

    def __init__(self):

        """Always include __init__ function to make object instantiation easier."""
        pass


    # def mark_categories_as_compete(self):
    #     pass


    def call_swiss(self):
        print("Swiss!")

