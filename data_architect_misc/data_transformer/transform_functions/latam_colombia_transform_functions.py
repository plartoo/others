"""This is the subclass of Transform function for Colombia (LATAM division).

We will define transform functions specific to Colombia here.

Author: Maicol Contreras
Last Modified: October 16, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamColombiaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    COLOMBIA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*MULTIPRODUCTO.*": "Other",
        "(?i).*ASEO.*PERSONAL.*": "Other",
        "(?i).*ILUMINACION.*": "Other",
        "(?i).*EQUIPO.*": "Other",
        "(?i).*BANCA\\s?ONLINE.*": "Other",
        "(?i).*PROD\\s?NATURALES.*": "Other",
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
            **LatamColombiaTransformFunctions.COLOMBIA_SPECIFIC_CATEGORY_MAPPINGS)
