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
        "(?i).*AFORES.*": "Other",
        "(?i).*YOGHURTS.*": "Other",
        "(?i).*APARATO.*ACCESORIOS\sDE\sVIDEO.*": "Other",
        "(?i).*APARATO.*SORDERA.*": "Other",
        "(?i).*ACCESORIO.*ARTICULO.*PERSONAL.*": "Other",
        "(?i).*ACCESORIOS.*REFACCIONES\sVEHICULOS\sMOTOR.*": "Other",
        "(?i).*ARTE.*CUTURA.*": "Other",
        "(?i).*APARATOS\sPARA\sLA\sSALUD.*": "Other",
        "(?i).*BOTANAS.*": "Other",
        "(?i).*CAFES/TES/MODIFICADOR\sDE\sLECHE.*": "Other",
        "(?i).*CHOCOLATES/DULCES/GOLOSINAS.*": "Other",
        "(?i).*CONDIMENTOS/ADEREZOS.*": "Other",
        "(?i).*CAMPINGS/CAMPAMENTOS.*": "Other",
        "(?i).*COMBUSTIBLE.*LUBRICANTE.*": "Other",
        "(?i).*DISCOS\sCASSETTES\sDISCOS\sCOMPACTOS.*": "Other",
        "(?i).*EDITORAS\sDE\sLIBROS.*": "Other",
        "(?i).*GASTRONOMIA/CENTROS\sNOCTURNOS.*": "Other",
        "(?i).*GRANOS.*LEGUMINOSAS.*": "Other",
        "(?i).*INSTRUMENTOS.*ACCESORIOS\sMUSICALES.*": "Other",
        "(?i).*ILUMINACION/PILAS/FOCOS.*": "Other",
        "(?i).*JUEGOS\sY\sJUGUETES.*": "Other",
        "(?i).*MEDIOS\sDE\sCOMUNICACI.*": "Other",
        "(?i).*MATERIAL.*CONSTRUCCION.*": "Other",
        "(?i).*MAQUINA.*EQUIPO.*PARA\sESCUELA.*": "Other",
        "(?i).*MAQUINAS.*REFACCIONES.*": "Other",
        "(?i).*PRESTACION\sDE\sSERVICIO\sSOCIAL.*": "Other",
        "(?i).*PRODUCTOS\sGRASOS.*": "Other",
        "(?i).*PALETAS/HELADOS.*": "Other",
        "(?i).*PRODUCTO.*DOMESTICO.*DESECHABLE.*": "Other",
        "(?i).*RELOJ.*JOYA.*": "Other",
        "(?i).*TURISMO.*VIAJE.*": "Other",
        "(?i).*UTENSILLOS\sDOMESTICOS.*": "Other",
        "(?i).*CASSETTES/CDS/VIDEOLASER.*": "Other",
        "(?i).*GOTA.*OFTALMICA.*": "Other",
        "(?i).*WHISKIES.*": "Other",
        "(?i).*SERVICIO.*CELULAR.*": "Other",
        "(?i).*ESTAMBRES/HILOS/LISTONES*": "Other",
        "(?i).*RONES.*": "Other",
        "(?i).*ARTICULO.*PIEL.*GENERAL.*": "Other",
        "(?i).*FASCICULO.*": "Other",
        "(?i).*EQUIPO.*SONIDO.*": "Other",
        "(?i).*FRACCIONAMIENTO.*": "Other",
        "(?i).*ALIMENTO.*ANIMAL.*": "Other",
        "(?i).*OTRA.*SEMILLA.*": "Other",
        "(?i).*CAJETA.*": "Other",
        "(?i).*PROD\sP/ADELGAZAR/REDUCTORES/CELULIT.*": "Other",

        "(?i).*BLANCOS.*": "Home Care",
    }

    def __init__(self, config):
        self.config = config

    def apply_country_specific_category_mapping_to_HARMONIZED_CATEGORY_column(self,
                                                   df,
                                                   existing_category_col_name: str
                                                   ):
        """
        Helper function to invoke the common comp harm function that will help us apply
        country-specific mappings for HARMONIZED_CATEGORY column.
        """
        return self. add_HARMONIZED_CATEGORY_column_using_existing_category_column_with_country_specific_mappings(
            df,
            LatamMexicoTransformFunctions.MEXICO_SPECIFIC_CATEGORY_MAPPINGS,
            existing_category_col_name
        )
