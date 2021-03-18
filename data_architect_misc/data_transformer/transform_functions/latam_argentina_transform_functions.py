"""This is the subclass of Transform function for Argentina (LATAM division).

We will define transform functions specific to Argentina here.

Author: Maicol Contreras
Last Modified: Nov 30, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamArgentinaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    ARGENTINA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*PAÑO.*ABSORBENT.*": "Other",
        "(?i).*REHABILI.*": "Other",
        "(?i).*IND.*METAL.*": "Other",
        "(?i).*CLIN.*OFTALMO.*": "Other",
        "(?i).*ANTITRANS.*": "Other",
        "(?i).*LAB.*CLINICO.*": "Other",
        "(?i).*PEG.*PROT.*DEN.*": "Other",
        "(?i).*CTO.*ONCOLOGI.*": "Other",
        "(?i).*GREMIO.*ASOCIA.*": "Other",
        "(?i).*IND.*ELDOM.*ELE.*": "Other",
        "(?i).*IND.*CONS.*MASI.*": "Other",
        "(?i).*C.D.\\sSENSIBILIDAD.*": "Other",
        "(?i).*EPS.*": "Other",
        "(?i).*CLIN.*PSICOLOG.*": "Other",
        "(?i).*PESQUERA.*": "Other",
        "(?i).*REPELENTE.*": "Other",
        "(?i).*TRAPO.*": "Other",

        "(?i).*DETERG.*LAVADO.*": "Home Care",
        "(?i).*LEJIA.*": "Home Care",
        "(?i).*LIMPIAPISO.*": "Home Care",

        "(?i).*COLORACION.*": "Personal Care",
        "(?i).*CREM.*ESCALDA.*": "Personal Care",
        "(?i).*C.D.\\sMULTIBENE.*": "Personal Care",
        "(?i).*C.D.\\sBLANQUE.*": "Personal Care",
        "(?i).*ESMALTE.*UÑA.*": "Personal Care",
        "(?i).*HAIR.*STYLING.*": "Personal Care",
        "(?i).*PRODUCTO.*ANTICASPA.*": "Personal Care",
    }

    def __init__(self, config):
        self.config = config
        # Define self.category_mappings below if we want to use
        # specific category mapping for this country
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamArgentinaTransformFunctions.ARGENTINA_SPECIFIC_CATEGORY_MAPPINGS)
