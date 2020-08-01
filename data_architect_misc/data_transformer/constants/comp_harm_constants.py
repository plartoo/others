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
SUBCATEGORY_COLUMN = 'HARMONIZED_SUBCATEGORY'
RAW_SUBCATEGORY_COLUMN = 'RAW_SUBCATEGORY'
RAW_BRAND_COLUMN = 'RAW_BRAND'
RAW_SUBBRAND_COLUMN = 'RAW_SUBBRAND'
RAW_PRODUCT_NAME_COLUMN = 'RAW_PRODUCT_NAME'
RAW_MEDIA_TYPE_COLUMN = 'RAW_MEDIA_TYPE'
PRODUCT_NAME_COLUMN = 'HARMONIZED_PRODUCT_NAME'

EXPECTED_COLUMNS = [
    # Standard column names we use in competitive harmonization project
    PROCESSED_DATE_COLUMN,
    YEAR_COLUMN,
    MONTH_COLUMN,
    DATE_COLUMN,
    REGION_COLUMN,
    COUNTRY_COLUMN,
    ADVERTISER_COLUMN,
    MEDIA_TYPE_COLUMN,
    CURRENCY_COLUMN,
    GROSS_SPEND_COLUMN,
    CATEGORY_COLUMN,
    RAW_SUBCATEGORY_COLUMN,
    RAW_BRAND_COLUMN,
    RAW_SUBBRAND_COLUMN,
    RAW_PRODUCT_NAME_COLUMN,
    SUBCATEGORY_COLUMN,
    PRODUCT_NAME_COLUMN
]

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

MEDIA_TYPE_MAPPINGS = {
    "(?i)CINEMA.*": "Cinema",
    "(?i)MAGAZINE.*": "Print", "(?i)NEWSPAPER.*": "Print", "(?i)PRINT.*": "Print", "(?i)PRESS.*": "Print",
    "(?i)OUTDOOR.*": "OOH", "(?i)OOH.*": "OOH", "(?i)OUT.*OF.*HOME.*": "OOH",
    "(?i)RADIO.*": "Radio", "(?i)RD.*": "Radio",
    "(?i)TV": "TV", "(?i)Television.*": "TV", "(?i)SPOTS": "TV", "FTA.*": "TV",
    "(?i)DIGITAL.*": "Digital", "(?i)INTERNET.*": "Digital", "(?i)ONLINE.*": "Digital", "(?i)MOBILE.*": "Digital",
}

COUNTRY_MAPPINGS = {
    # Mapping between raw country names in regular expression to standardized country names
    "(?i)BAHRAIN.*": "Bahrain",
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
    "(?i).*BIERSDORF.*": "BEIERSDORF",
    "(?i).*COLGATE.*": "COLGATE-PALMOLIVE",
    "(?i).*CLOROX.*": "THE CLOROX COMPANY",
    "(?i)^CP$": "COLGATE-PALMOLIVE",
    "(?i).*GLAXO.*": "GSK",  # also catches "\u200EGlaxoSmithKline"
    "(?i)^GSK.*": "GSK",
    "(?i).*HENKEL.*": "HENKEL",
    "(?i).*JOHNSON.*&.*JOHNSON.*": "JOHNSON & JOHNSON",
    "(?i)J.*&.*J.*": "JOHNSON & JOHNSON",
    "(?i).*L'?OREAL.*": "LOREAL",  # also catches 'LOREAL'
    "(?i).*PHILIPS.*": "PHILIPS",
    "(?i).*PROCTER.*&.*GAMBLE.*": "P&G",
    "(?i)P.*&.*G.*": "P&G",
    "(?i).*RECKITT.*": "RECKITT BENCKISER",
    "(?i)^RB\\s*?$": "RECKITT BENCKISER",
    "(?i)^RB\\sAG$": "RECKITT BENCKISER",
    "(?i)SANOFI.*": "SANOFI",
    "(?i)SC JOHNSON.*": "JOHNSON & JOHNSON",
    "(?i).*UNILEVER.*": "UNILEVER"
}

CATEGORY_MAPPINGS = {
    "(?i)^HC$": "Home Care",
    "(?i)HOME.*": "Home Care",
    "(?i).*HOME.*CARE.*": "Home Care",
    "(?i).*HOUSEHOLD.*": "Home Care",
    "(?i).*Laundry.*": "Home Care",
    "(?i).*Toiletries.*": "Home Care",
    "(?i)Cleaning.*agent.*": "Home Care",
    "(?i).*Detergent.*": "Home Care",

    "(?i)^OC$": "Oral Care",
    "(?i).*ORAL.*": "Oral Care",
    "(?i).*ORAL.*CARE.*": "Oral Care",
    "(?i).*Dental.*": "Oral Care",
    "(?i).*Dentifrices.*": "Oral Care",

    "(?i).*BEAUTY.*": "Personal Care",
    "(?i).*BODY.*CARE.*": "Personal Care",
    "(?i).*Cosmetics.*": "Personal Care",
    "(?i).*Deodorant.*": "Personal Care",
    "(?i).*Eye.*Care.*": "Personal Care",
    "(?i)Face.*Care.*": "Personal Care",
    "(?i).*Facial.*": "Personal Care",
    "(?i)Feminine.*Care.*": "Personal Care",
    "(?i)Hair.*Care.*": "Personal Care",
    "(?i)Hair.*Colour.*": "Personal Care",
    "(?i)Hair.*Shampoo.*": "Personal Care",
    "(?i).*Hair.*Removal.*": "Personal Care",
    "(?i)Hair.*Styl.*": "Personal Care",
    "(?i)Hair.*Treatment.*": "Personal Care",
    "(?i)Hand.*Wash.*": "Personal Care",
    "(?i)Shampoo.*Conditioner": "Personal Care",
    "(?i).*HYGIENE.*": "Personal Care",
    "(?i)^PC$": "Personal Care",
    "(?i).*PERSONAL.*CARE.*": "Personal Care",
    "(?i).*BABY.*CARE.*": "Personal Care",
    "(?i)Bath.*Shower.*": "Personal Care",
    "(?i).*Moisturizer.*": "Personal Care",
    "(?i).*Sun.*Products.*": "Personal Care",

    "(?i)OTHER.*": "Other",
    "(?i).*Accessories.*": "Other",
    "(?i).*Agriculture.*": "Other",
    "(?i).*Alcohol.*": "Other",
    "(?i)ALL.*OTHER.*": "Other",
    "(?i).*Automation.*": "Other",
    "(?i).*Automotive.*": "Other",
    "(?i).*Banking.*": "Other",
    "(?i).*Beverage.*": "Other",
    "(?i).*Building.*": "Other",
    "(?i).*Cough.*": "Other",
    "(?i).*Clothing.*": "Other",
    "(?i).*Computers.*": "Other",
    "(?i).*Conglomerate.*": "Other",
    "(?i).*Corporate.*": "Other",
    "(?i).*Dairy.*": "Other",
    "(?i).*Dermatology.*": "Other",
    "(?i).*Drinks.*": "Other",
    "(?i).*Durables.*": "Other",
    "(?i).*Education.*": "Other",
    "(?i).*Equipments.*": "Other",
    "(?i).*Electrical.*": "Other",
    "(?i).*Event.*": "Other",
    "(?i).*Finance.*": "Other",
    "(?i).*Foundation.*": "Other",
    "(?i).*FOOD.*": "Other",
    "(?i).*Fuel.*": "Other",
    "(?i).*Internet.*": "Other",
    "(?i).*Investment.*": "Other",
    "(?i).*Land.*": "Other",
    "(?i).*Materials.*": "Other",
    "(?i).*Medicated.*": "Other",
    "(?i).*Medicine.*": "Other",
    "(?i).*Miscellaneous.*": "Other",
    "(?i).*Muscle.*": "Other",
    "(?i).*Office.*": "Other",
    "(?i).*Petroleum.*": "Other",
    "(?i)Pesticide.*": "Other",
    "(?i).*Pharmaceutical.*": "Other",
    "(?i).*Pharmacy.*": "Other",
    "(?i).*Retail.*": "Other",
    "(?i).*Telecom.*": "Other",
    "(?i).*Textiles.*": "Other",
    "(?i).*Tobacco.*": "Other",
    "(?i).*Tourism.*": "Other",
    "(?i).*Transport.*": "Other",
    "(?i).*Vitamin.*": "Other",

    "(?i)Pet\\s.*": "Pet Nutrition"
}
