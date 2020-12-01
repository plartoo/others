"""This is the subclass of Transform function for Peru (LATAM division).

We will define transform functions specific to Peru here.

Author: Maicol Contreras
Last Modified: October 21, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamPeruTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    PERU_SPECIFIC_CATEGORY_MAPPINGS = {
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

        "(?i).*LEJIA.*": "Home Care",
        
        "(?i).*CREM.*ESCALDA.*": "Personal Care",
        "(?i).*C.D.\\sMULTIBENE.*": "Personal Care",
        "(?i).*C.D.\\sBLANQUE.*": "Personal Care",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamPeruTransformFunctions.PERU_SPECIFIC_CATEGORY_MAPPINGS)
