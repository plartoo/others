PROCESSED_DATE_COLUMN = 'PROCESSED_DATE'
YEAR_COLUMN = 'HARMONIZED_YEAR'
MONTH_COLUMN = 'HARMONIZED_MONTH'
DATE_COLUMN = 'HARMONIZED_DATE'
REGION_COLUMN = 'HARMONIZED_REGION'
COUNTRY_COLUMN = 'HARMONIZED_COUNTRY'
ADVERTISER_COLUMN = 'HARMONIZED_ADVERTISER'
MEDIA_TYPE_COLUMN = 'HARMONIZED_MEDIA_TYPE'
CURRENCY_COLUMN = 'HARMONIZED_CURRENCY'
GROSS_SPEND_COLUMN = 'HARMONIZED_GROSS_SPEND'
CATEGORY_COLUMN = 'HARMONIZED_CATEGORY'
RAW_SUBCATEGORY_COLUMN = 'RAW_SUBCATEGORY'
RAW_BRAND_COLUMN = 'RAW_BRAND'
RAW_SUBBRAND_COLUMN = 'RAW_SUBBRAND'
RAW_PRODUCT_NAME_COLUMN = 'RAW_PRODUCT_NAME'
PRODUCT_NAME_COLUMN = 'HARMONIZED_PRODUCT_NAME'

# Below are the regions, countries, categories, media types
# and globally competing advertisers that we support as of April, 2020.
# Whenever we come across new data items for constants below, add them.
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
    'India', 'Indonesia', 'Ireland', 'Italy', 'Israel',
    'Kazakhstan', 'Kenya', 'Kuwait',
    'Latvia', 'Lithuania',
    'Malaysia', 'Mexico', 'Morocco',
    'Netherlands', 'New Zealand', 'Nicaragua', 'Norway',
    'Oman',
    'Pan Arab', 'Pan Asian', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico',
    'Qatar',
    'Romania', 'Russia',
    'Saudi Arabia', 'Singapore', 'Slovakia', 'South Africa', 'Spain', 'Sweden', 'Switzerland',
    'Taiwan', 'Thailand', 'Turkey',
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'USA',
    'Venezuela', 'Vietnam'
}

MEDIA_TYPES = {'Cinema', 'Digital', 'Door drops', 'In-store', 'OOH', 'Print', 'Radio', 'TV'}

GLOBAL_COMPETE_ADVERTISERS = {
    # This list is used only as a reference for new team members
    # It is not used in the code.
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

CATEGORIES = {'Home Care', 'Oral Care', 'Other', 'Personal Care', 'Pet Nutrition'}

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

MEDIA_TYPE_MAPPINGS = {
    "(?i)CINEMA.*": "Cinema",
    "(?i)MAGAZINE.*": "Print", "(?i)NEWSPAPER.*": "Print", "(?i)PRINT.*": "Print", "(?i)PRESS.*": "Print",
    "(?i)OUTDOOR.*": "OOH", "(?i)OOH.*": "OOH", "(?i)OUT.*OF.*HOME.*": "OOH",
    "(?i)RADIO.*": "Radio", "(?i)RD.*": "Radio",
    "(?i)TV": "TV", "(?i)Television.*": "TV",
    "(?i)DIGITAL.*": "Digital", "(?i)INTERNET.*": "Digital", "(?i)ONLINE.*": "Digital",
}

COUNTRY_MAPPINGS = {
    # Mapping between raw country names in regular expression to standardized country names
    "(?i)BAHRAIN.*": "Bahrain",
    "(?i)KENYA.*": "Kenya",
    "(?i)KAZAK.*": "Kazakhstan",
    "(?i)KAZAKHSTAN.*": "Kazakhstan",
    "(?i)KENYA.*": "Kenya",
    "(?i)KUWAIT.*": "Kuwait",
    "(?i)KSA.*": "Saudi Arabia",
    "(?i)MOROCCO.*": "Morocco",
    "(?i)MORROCO.*": "Morocco",
    "(?i)MORROCCO.*": "Morocco",
    "(?i)OMAN.*": "Oman",
    "(?i)PAN.*ARAB.*": "Pan Arab",
    "(?i)PAN.*ASIAN.*": "Pan Asian",
    "(?i)QATAR.*": "Qatar",
    "(?i)RUSSIA.*": "Russia",
    "(?i)SOUTH.*AFRICA.*": "South Africa",
    "(?i)TURKEY.*": "Turkey",
    "(?i)UKRAINE.*": "Ukraine",
    "(?i)UNITED ARAB EMIRATES.*": "United Arab Emirates",
    "(?i)UAE.*": "United Arab Emirates"
}

ADVERTISER_MAPPINGS = {
    # Mapping between raw advertiser names in regular expression to standardized advertiser names
    # This list will grow to a big one and must be kept maintained/updated constantly.
    "(?i)BDF.*": "BEIERSDORF",
    "(?i).*BEIERSDORF.*": "BEIERSDORF",
    "(?i).*COLGATE.*": "COLGATE-PALMOLIVE",
    "(?i).*CLOROX.*": "THE CLOROX COMPANY",
    "(?i)^CP$": "COLGATE-PALMOLIVE",
    "(?i).*GLAXO.*": "GSK", # also catches "\u200EGlaxoSmithKline"
    "(?i)^GSK": "GSK",
    "(?i).*HENKEL.*": "HENKEL",
    "(?i).*JOHNSON.*&.*JOHNSON.*": "JOHNSON & JOHNSON",
    "(?i)J.*&.*J.*": "JOHNSON & JOHNSON",
    "(?i).*L'?OREAL.*": "LOREAL", # also catches 'LOREAL'
    "(?i).*PHILIPS.*": "PHILIPS",
    "(?i).*PROCTER.*&.*GAMBLE": "P&G",
    "(?i)P.*&.*G": "P&G",
    "(?i).*RECKITT.*": "RECKITT BENCKISER",
    "(?i)^RB\s*?$": "RECKITT BENCKISER",
    "(?i)^RB\sAG$": "RECKITT BENCKISER",
    "(?i)SANOFI.*": "SANOFI",
    "(?i)SC JOHNSON.*": "JOHNSON & JOHNSON",
    "(?i).*UNILEVER.*": "UNILEVER"
}

CATEGORY_MAPPINGS = {
    "(?i)^HC$": "Home Care",
    "(?i)HOME.*": "Home Care",
    "(?i).*HOME.*CARE.*": "Home Care",
    "(?i).*HOUSEHOLD.*CARE.*": "Home Care",
    "(?i)^OC$": "Oral Care",
    "(?i).*ORAL.*": "Oral Care",
    "(?i).*ORAL.*CARE.*": "Oral Care",
    "(?i)^PC$": "Personal Care",
    "(?i).*PERSONAL.*CARE.*": "Personal Care",
    "(?i).*BABY.*CARE.*": "Personal Care",
    "(?i).*HAIR.*CARE.*": "Personal Care",
    "(?i)OTHER.*": "Other",
    "(?i)ALL.*OTHER.*": "Other",

    "(?i).*AIR.*FRESHENER.*RANGE.*": "Home Care",
    "(?i).*BABY NAPKINS.*": "Personal Care",
    "(?i).*BABY.*BATH-SHOWER-SOAP.*": "Personal Care",
    "(?i).*BABY.*CARE.*PRODUCTS.*": "Personal Care",
    "(?i).*BODY.*CARE.*LINES.*": "Personal Care",
    "(?i).*COSMETIC.*PRODUCT.*RANGE.*": "Personal Care",
    "(?i).*COSMETICS.*CORPORATE.*": "Personal Care",
    "(?i).*DELI.*HANDWASH.*LIQUID.*": "Personal Care",
    "(?i).*DEODORANTS.*": "Personal Care",
    "(?i).*DISHWASHER.*PRODUCTS.*": "Home Care",
    "(?i).*FABRIC.*SOFTENER/FRESHENER.*": "Home Care",
    "(?i).*FACE CREAM.*MOITURIZERS.*": "Personal Care",
    "(?i).*FACE.*CLEANSERS.*": "Personal Care",
    "(?i).*FACE.*SCRUB.*ANTI.*ACNE.*": "Personal Care",
    "(?i).*FEMININE.*HYGIENE.*": "Personal Care",
    "(?i).*FLOOR.*CLEANERS.*": "Home Care",
    "(?i).*FOUNDATION.*": "Other",
    "(?i).*HAIR.*CARE.*RANGES.*": "Personal Care",
    "(?i).*HYGIENE.*CORPORATE.*": "Personal Care",
    "(?i).*LIPSTICKS.*": "Personal Care",
    "(?i).*MAKE-UP.*LINES.*": "Personal Care",
    "(?i).*MAKE-UP.*REMOVERS.*": "Personal Care",
    "(?i).*MASK.*": "Personal Care",
    "(?i).*MEN'S.*FACIAL.*CARE.*LINE.*": "Personal Care",
    "(?i).*MENS.*MANUAL.*RAZORS.*BLADES.*": "Other",
    "(?i).*MEN'S.*SHAMPOO.*": "Personal Care",
    "(?i).*MOUTH.*WASHES.*": "Oral Care",
    "(?i).*NAIL.*VARNISH.*DECORATION.*": "Personal Care",
    "(?i).*NAPIES.*": "Other",
    "(?i).*PERSONAL.*HYGIENE.*RANGE.*": "Personal Care",
    "(?i).*SHAMPOO.*": "Personal Care",
    "(?i).*SHOWER.*PRODUCTS.*": "Personal Care",
    "(?i).*SUN.*AFTER-SUN CARE.*": "Personal Care",
    "(?i).*TOOTHPASTE.*": "Oral Care",
    "(?i).*WASHING.*LIQUID.*": "Personal Care",
    "(?i).*WASHING.*POWDER.*": "Home Care",
    "(?i).*WASHING-UP.*PRODUCTS.*": "Home Care",
    "(?i).*WATER-CLOSET.*CLEANERS.*": "Home Care",
    "(?i).*WHITENING.*ESSENCE.*": "Personal Care",
    "(?i).*WOMEN'S.*FRAGRANCES.*": "Personal Care",
}

