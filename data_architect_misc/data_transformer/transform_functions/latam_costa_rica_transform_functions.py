"""This is the subclass of Transform function for Costa_Rica (LATAM division).

We will define transform functions specific to Costa_Rica here.

Author: Maicol Contreras
Last Modified: October 15, 2020
"""
from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamCostaRicaTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    COSTA_RICA_SPECIFIC_CATEGORY_MAPPINGS = {
        "(?i).*AUTOLAVADO.*": "Other",
        "(?i).*FUMIGADOR.*": "Other",
        "(?i).*ESCOLAR.*": "Other",
        "(?i).*PARASICOLOGIA.*": "Other",
        "(?i).*ANCIANO.*": "Other",
        "(?i).*PROGRAMACION.*": "Other",
        "(?i).*HIGIENE\\sINSTITUCIO.*": "Other",
        "(?i).*ESTRENIMIENTO.*": "Other",
        "(?i).*OPERADORES\\sMOV\\sFUL.*": "Other",
        "(?i).*PARAGUERIAS.*": "Other",
        "(?i).*VARIOS.*": "Other",
        "(?i).*(\b)?MASA(\b)?.*": "Other",
        "(?i).*(\b)?MENTA(\b)?.*": "Other",
        "(?i).*CONTRADROGA.*": "Other",
        "(?i).*DISCOMOVILES.*": "Other",
        "(?i).*COURIER.*": "Other",
        "(?i).*BEBE.*GENERICO.*": "Other",
        "(?i).*CENTRO.*COM.*OTROS.*": "Other",
    }

    def __init__(self, config):
        self.config = config
        self.category_mappings = dict(
            comp_harm_constants.SPANISH_CATEGORY_MAPPINGS,
            **LatamCostaRicaTransformFunctions.COSTA_RICA_SPECIFIC_CATEGORY_MAPPINGS)
