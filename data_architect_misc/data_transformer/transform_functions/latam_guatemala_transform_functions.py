"""This is the subclass of Transform function for Guatemala (LATAM division).

We will define transform functions specific to Guatemala here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamGuatemalaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    GUATEMALA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*HUEVO.*": "Other",
        "(?i).*SEDAN.*": "Other",
        "(?i).*ILUMINACION.*": "Other",
        "(?i).*EQUIPO.*": "Other",
        "(?i).*BANCA\\sONLINE.*": "Other",
        "(?i).*PROD\\sNATURALES.*": "Other",
        "(?i).*PICK-UPS.*": "Other",
        "(?i).*FUERZA.*ARMADA.*": "Other",
        "(?i).*OTRO.*PRODUCTO.*INFANTIL.*": "Other",
        "(?i).*PAQUETE.*FIJO.*HOGAR.*": "Other",
        "(?i).*EQUIPO.*INSTRUMENTO.*MEDICO.*": "Other",
        "(?i).*ELEARNING.*": "Other",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamGuatemalaTransformFunctions.GUATEMALA_SPECIFIC_CATEGORY_MAPPINGS)
