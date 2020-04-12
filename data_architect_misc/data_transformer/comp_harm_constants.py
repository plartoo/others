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

CURRENCIES = {
    # Standard currency names we support in competitive harmonization project
    'USD'
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
    "(?i)OUTDOOR.*": "OOH", "(?i)OOH.*": "OOH",
    "(?i)RADIO.*": "Radio", "(?i)RD.*": "Radio",
    "(?i)TV": "TV", "(?i)Television.*": "TV",
    "(?i)DIGITAL.*": "Digital", "(?i)INTERNET.*": "Digital", "(?i)ONLINE.*": "Digital"
}

COUNTRY_MAPPINGS = {
    # Mapping between raw country names in regular expression to standardized country names
    "(?i)BAHRAIN.*": "Bahrain",
    "(?i)KSA.*": "Saudi Arabia",
    "(?i)KUWAIT.*": "Kuwait",
    "(?i)MOROCCO.*": "Morocco",
    "(?i)MORROCO.*": "Morocco",
    "(?i)MORROCCO.*": "Morocco",
    "(?i)OMAN.*": "Oman",
    "(?i)PAN.*ARAB.*": "Pan Arab",
    "(?i)PAN.*ASIAN.*": "Pan Asian",
    "(?i)QATAR.*": "Qatar",
    "(?i)Russia.*": "Russia",
    "(?i)UNITED ARAB EMIRATES.*": "United Arab Emirates",
    "(?i)UAE.*": "United Arab Emirates"
}

ADVERTISER_MAPPINGS = {
    # Mapping between raw advertiser names in regular expression to standardized advertiser names
    # This list will grow to a big one and must be kept maintained/updated constantly.
    "(?i)BDF.*": "BEIERSDORF",
    "(?i)BEIERSDORF.*": "BEIERSDORF",
    "(?i)COLGATE.*": "COLGATE-PALMOLIVE",
    "(?i)^CP$": "COLGATE-PALMOLIVE",
    "(?i)GLAXO.*": "GSK",
    "(?i)^GSK": "GSK",
    "(?i)HENKEL.*": "HENKEL",
    "(?i)JOHNSON.*&.*JOHNSON.*": "JOHNSON & JOHNSON",
    "(?i)J.*&.*J.*": "JOHNSON & JOHNSON",
    "(?i)L'?OREAL.*": "LOREAL",
    "(?i)PROCTER.*&.*GAMBLE": "P&G",
    "(?i)P.*&.*G": "P&G",
    "(?i)RECKITT.*": "RECKITT BENCKISER",
    "(?i)^RB$": "RECKITT BENCKISER",
    "(?i).*CLOROX.*": "THE CLOROX COMPANY",
    "(?i).*UNILEVER.*": "UNILEVER"
}

CATEGORY_MAPPINGS = {
    "(?i)^HC$": "Home Care",
    "(?i)HOME.*CARE.*": "Home Care",
    "(?i)^OC$": "Oral Care",
    "(?i)ORAL.*CARE.*": "Oral Care",
    "(?i)^PC$": "Personal Care",
    "(?i).*PERSONAL.*CARE.*": "Personal Care",
    "(?i).*BABY.*CARE.*": "Personal Care",
    "(?i)HAIR.*CARE.*": "Personal Care",
    "(?i)OTHER.*": "Other",
    "(?i)ALL.*OTHER.*": "Other"
}
