"""This is the subclass of Transform function for Mexico (LATAM division).

We will define transform functions specific to Mexico here.

Author: Maicol Contreras
Last Modified: September 9, 2020
"""

import pandas as pd

from constants import comp_harm_constants
from transform_functions.common_comp_harm_transform_functions import CommonCompHarmTransformFunctions


class LatamMexicoTransformFunctions(CommonCompHarmTransformFunctions):
    """
    All custom (uncommon) transform functions **SPECIFIC to
    individual processing task** must be defined as part
    of this class.
    """
    MEXICO_SPECIFIC_CATEGORY_MAPPINGS = {
            "(?i).*APARATOS\sDOMESTICOS.*": "Other",
            "(?i).*APARATOS.*ACCESORIOS\sDE\sVIDEO.*": "Other",
            "(?i).*ALIMENTOS.*ARTICULOS.*": "Other",
            "(?i).*ALIMENTOS.*INFANTILES.*": "Other",
            "(?i).*ACCESORIO.*ARTICULO.*PERSONAL.*": "Other",
            "(?i).*ACCESORIOS.*REFACCIONES\sVEHICULOS\sMOTOR.*": "Other",
            "(?i).*ALIMENTOS.*ENLATADO.*INSTANTANE.*": "Other",
            "(?i).*ARTE.*CUTURA.*": "Other",
            "(?i).*AGRICULTURA.*": "Other",
            "(?i).*APARATOS\sPARA\sLA\sSALUD.*": "Other",
            "(?i).*BOTANAS.*": "Other",
            "(?i).*BLANCOS.*": "Home Care",
            "(?i).*CAFES/TES/MODIFICADOR\sDE\sLECHE.*": "Other",
            "(?i).*COMPUTACION.*": "Other",
            "(?i).*CHOCOLATES/DULCES/GOLOSINAS.*": "Other",
            "(?i).*CONDIMENTOS/ADEREZOS.*": "Other",
            "(?i).*CAMPINGS/CAMPAMENTOS.*": "Other",
            "(?i).*COMBUSTIBLE.*LUBRICANTE.*": "Other",
            "(?i).*DISCOS\sCASSETTES\sDISCOS\sCOMPACTOS.*": "Other",
            "(?i).*EDUCACION.*": "Other",
            "(?i).*EDITORAS\sDE\sLIBROS.*": "Other",
            "(?i).*GASTRONOMIA/CENTROS\sNOCTURNOS.*": "Other",
            "(?i).*GRANOS.*LEGUMINOSAS.*": "Other",
            "(?i).*INSTRUMENTOS.*ACCESORIOS\sMUSICALES.*": "Other",
            "(?i).*INSTITUCIONAL.*": "Other",
            "(?i).*INMOBILIARIAS.*": "Other",
            "(?i).*ILUMINACION/PILAS/FOCOS.*": "Other",
            "(?i).*JUEGOS\sY\sJUGUETES.*": "Other",
            "(?i).*MEDIOS\sDE\sCOMUNICACI.*": "Other",
            "(?i).*MATERIAL.*CONSTRUCCION.*": "Other",
            "(?i).*MAQUINA.*EQUIPO.*PARA\sESCUELA.*": "Other",
            "(?i).*MAQUINAS.*REFACCIONES.*": "Other",
            "(?i).*MENUDEO.*": "Other",
            "(?i).*MOTOCICLETA.*": "Other",
            "(?i).*NO\sDISPONIBLE.*": "Other",
            "(?i).*PUBLICIDAD\sCOMPARTIDA.*": "Other",
            "(?i).*PANIFICACION.*": "Other",
            "(?i).*PRESTACION\sDE\sSERVICIO\sSOCIAL.*": "Other",
            "(?i).*PRODUCTOS\sGRASOS.*": "Other",
            "(?i).*PALETAS/HELADOS.*": "Other",
            "(?i).*PRODUCTO.*DOMESTICO.*DESECHABLE.*": "Other",
            "(?i).*RELOJ.*JOYA.*": "Other",
            "(?i).*ROPA.*": "Other",
            "(?i).*SEGURO.*": "Other",
            "(?i).*TELEMERCADEO.*": "Other",
            "(?i).*TURISMO.*VIAJE.*": "Other",
            "(?i).*UTENSILLOS\sDOMESTICOS.*": "Other",
            
    }

    def __init__(self, config):
        self.config = config

    def add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            self,
            df,
            existing_category_col_name: str):
        """
        We have some Nicaragua-specific category mappings, so we will
        wrap the common comp. harm. transform function with this one.
        """
        # REF: https://stackoverflow.com/a/1784128/1330974
        category_mappings = dict(comp_harm_constants.CATEGORY_MAPPINGS,
                                 **LatamMexicoTransformFunctions.MEXICO_SPECIFIC_CATEGORY_MAPPINGS)

        return self.add_new_column_with_values_based_on_another_column_values_using_regex_match \
            (df,
             existing_category_col_name,
             comp_harm_constants.CATEGORY_COLUMN,
             category_mappings
             )