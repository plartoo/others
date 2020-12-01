"""This is the subclass of Transform function for El Salvador (LATAM division).

We will define transform functions specific to El Salvador here.

Author: Maicol Contreras
Last Modified: August 3, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamElSalvadorTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    EL_SALVADOR_SPECIFIC_CATEGORY_MAPPINGS = {
            "(?i).*CREMAS\\sPARA\sLA\\sPIEL.*": "Personal Care",
            "(?i).*HIGIENE\\sINTIMA\\sFEMENINA.*": "Personal Care",
            "(?i).*HIGIENE\\sPRODUCTOS\\sINFANTILES.*": "Personal Care",
        }
    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamElSalvadorTransformFunctions.EL_SALVADOR_SPECIFIC_CATEGORY_MAPPINGS)
