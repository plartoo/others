# Below are the regions, countries, categories, media types
# and globally competing advertisers that we support as of April, 2020.
# Whenever we come across new data items for constants below, add them.

COUNTRIES_IN_FX_FILE = {"TODO"}

REGIONS = {'Africa-Eurasia', 'Asia Pacific', 'Europe', 'Latin America', 'North America'}

COUNTRIES = {
    'Argentina', 'Australia', 'Austria',
    'Bahrain', 'Belgium', 'Brazil',
    'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Czech Republic',
    'Denmark', 'Dominican Republic',
    'Ecuador', 'El Salvador', 'Estonia',
    'Finland', 'France',
    'Germany', 'Greece', 'Guatemala',
    'Honduras', 'Hong Kong', 'Hungary',
    'India', 'Indonesia', 'Ireland', 'Italy', "Israel",
    'Kuwait',
    'Latvia', 'Lithuania',
    'Malaysia', 'Mexico', 'Morocco',
    'Netherlands', 'New Zealand', 'Nicaragua', 'Norway',
    'Oman',
    'Pan Arab', 'Pan Asia', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
    'Qatar',
    'Romania', 'Russia',
    'Saudi Arabia', 'Singapore', 'Slovakia', 'Spain', 'Sweden', 'Switzerland',
    'Taiwan', 'Thailand', 'Turkey',
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'USA',
    'Venezuela', 'Vietnam'
}

CATEGORIES = {'Home Care', 'Oral Care', 'Other', 'Personal Care', 'Pet Nutrition'}

MEDIA_TYPES = {'Cinema', 'Digital', 'Door drops', 'In-store', 'OOH', 'Print', 'Radio', 'TV'}

GLOBAL_COMPETE_ADVERTISERS = {
    'BEIERSDORF',
    'CHURCH & DWIGHT',
    'COLGATE-PALMOLIVE',
    'GENOMMA LAB',
    'GSK',
    'HENKEL',
    'JOHNSON & JOHNSON',
    'LOREAL',
    'P&G',
    'PHILIPS',
    'RECKITT BENCKISER',
    'SANOFI',
    'S.C. JOHNSON',
    'THE CLOROX COMPANY',
    'UNILEVER'
}

# Minimum set of output columns expected after data transformation
EXPECTED_STANDARD_OUTPUT_COLUMNS = {
    "YEAR",
    "MONTH",
    "DATE",
    "PROCESSED_DATE",
    "HARMONIZED_REGION",
    "HARMONIZED_COUNTRY",
    "HARMONIZED_ADVERTISER",
    "HARMONIZED_MEDIA_TYPE",
    "CURRENCY",
    "GROSS_SPEND_IN_LOCAL_CURRENCY",
    "HARMONIZED_CATEGORY",
    "RAW_SUBCATEGORY",
    "RAW_BRAND",
    "RAW_SUBBRAND",
    "RAW_PRODUCT_NAME"
}
