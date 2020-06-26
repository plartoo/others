from constants.comp_harm_constants import COUNTRIES

FX_COUNTRY_NAME_TO_HARMONIZED_COUNTRY_NAME_MAPPINGS = {
    'ARGENTINA': 'Argentina'
    , 'AUSTRALIA': 'Australia'
    , 'BRAZIL': 'Brazil'
    , 'CANADA': 'Canada'
    , 'CHILE': 'Chile'
    , 'CHINA': 'China'
    , 'COLOMBIA': 'Colombia'
    , 'COSTA RICA': 'Costa Rica'
    , 'CZECH REPUBLIC': 'Czech Republic'
    , 'DENMARK': 'Denmark'
    , 'DOM. REP.': 'Dominican Republic'
    , 'ECUADOR': 'Ecuador'
    , 'EL SALVADOR': 'El Salvador'
    , 'ESTONIA': 'Estonia'
    , 'EURO': 'Euro'
    , 'GUATEMALA': 'Guatemala'
    , 'HONDURAS': 'Honduras'
    , 'HONG KONG': 'Hong Kong'
    , 'HUNGARY': 'Hungary'
    , 'INDIA': 'India'
    , 'INDONESIA': 'Indonesia'
    , 'ISRAEL': 'Israel'
    , 'KAZAKHSTAN': 'Kazakhstan'
    , 'KENYA': 'Kenya'
    , 'LATVIA': 'Latvia'
    , 'LITHUANIA': 'Lithuania'
    , 'MALAYSIA': 'Malaysia'
    , 'MEXICO': 'Mexico'
    , 'MOROCCO': 'Morocco'
    , 'NEW ZEALAND': 'New Zealand'
    , 'NICARAGUA': 'Nicaragua'
    , 'NORWAY': 'Norway'
    , 'PANAMA': 'Panama'
    , 'PARAGUAY': 'Paraguay'
    , 'PERU': 'Peru'
    , 'PHILIPPINES': 'Philippines'
    , 'POLAND': 'Poland'
    , 'ROMANIA': 'Romania'
    , 'RUSSIA': 'Russia'
    , 'SINGAPORE': 'Singapore'
    , 'SO. AFRICA': 'South Africa'
    , 'SWEDEN': 'Sweden'
    , 'SWITZERLAND': 'Switzerland'
    , 'TAIWAN': 'Taiwan'
    , 'THAILAND': 'Thailand'
    , 'TURKEY': 'Turkey'
    , 'U.K.': 'United Kingdom'
    , 'UKRAINE': 'Ukraine'
    , 'URUGUAY': 'Uruguay'
    , 'VENEZUELA': 'Venezuela'
    , 'VIETNAM': 'Vietnam'
    # In 2012 raw FX file, they have asterik next to Vietnam
    , 'VIETNAM*': 'Vietnam'
}

DATE_COLUMN = 'DATE'
FX_RATES_COLUMN = 'FX_RATES'
YEAR_COLUMN = 'YEAR'
RAW_COUNTRY_COLUMN = 'COUNTRY'
HARMONIZED_COUNTRY_COLUMN = 'HARMONIZED_COUNTRY'
CONSTANT_DOLLAR_COLUMN_SUFFIX = '_CONSTANT_DOLLAR_RATIO'

USD_FX_Rate = 1.0
EURO_CURRENCY_NAME = 'Euro'

COUNTRIES_THAT_USE_USD = {
    'Bahrain', 'Kuwait', 'Oman', 'Pan Arab', 'Pan Asian', 'Puerto Rico',
    'Qatar', 'Saudi Arabia', 'United Arab Emirates', 'USA'
}

COUNTRIES_THAT_USE_EURO = {
    'Austria', 'Belgium', 'Finland', 'France', 'Germany', 'Greece',
    'Ireland', 'Italy', 'Netherlands', 'Portugal', 'Slovakia', 'Spain'
}
