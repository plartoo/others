"""This is the subclass of Transform function for Argentina (LATAM division).

We will define transform functions specific to Argentina here.

Author: Maicol Contreras
Last Modified: October 28, 2020
"""

import pandas as pd

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
        "(?i).*C.D.\sSENSIBILIDAD.*": "Other",
        "(?i).*EPS.*": "Other",
        "(?i).*CLIN.*PSICOLOG.*": "Other",
        "(?i).*PESQUERA.*": "Other",

        "(?i).*LEJIA.*": "Home Care",
        
        "(?i).*CREM.*ESCALDA.*": "Personal Care",
        "(?i).*C.D.\sMULTIBENE.*": "Personal Care",
        "(?i).*C.D.\sBLANQUE.*": "Personal Care",
    }

    def __init__(self, config):
        self.config = config
        
    def apply_country_specific_category_mapping_to_HARMONIZED_CATEGORY_column(self,
                                                   df,
                                                   existing_category_col_name: str,
                                                   leave_empty_if_no_match = False
                                                   ):
        """
        Helper function to invoke the common comp harm function that will help us apply
        country-specific mappings for HARMONIZED_CATEGORY column.
        """
        return self. add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            df,
            LatamArgentinaTransformFunctions.ARGENTINA_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name,
            leave_empty_if_no_match
        )
