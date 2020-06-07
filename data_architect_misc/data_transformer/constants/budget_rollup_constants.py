from constants.comp_harm_constants import CATEGORY_MAPPINGS

DIMENSION_COLUMNS = {
    'Region',
    'Market',
    'Year',
    'Category',
    'Segment Macro',
    'Brand',
    'Macro Channel',
    'Channel',
}
ESSENTIAL_COLUMNS = DIMENSION_COLUMNS.union({'Budget (USD)'})

# REGION column related constants
HILLS_REGION_NAME = 'HILLS'
RAW_REGION_COLUMN_NAME = 'Region'
HARMONIZED_REGION_COLUMN_NAME = 'Harmonized_Region'
RAW_TO_HARMONIZED_REGION_NAME_MAPPING = {
    'AED': 'AFRICA-EURASIA',
    'APAC': 'ASIA-PACIFIC',
    'EUROPE': 'EUROPE',
    'LATAM': 'LATIN AMERICA',
    'NA': 'NORTH AMERICA',
}
EXPECTED_REGION_COLUMN_VALUES = list(RAW_TO_HARMONIZED_REGION_NAME_MAPPING.keys())
EXPECTED_HARMONIZED_REGION_COLUMNS_VALUES = EXPECTED_REGION_COLUMN_VALUES + [HILLS_REGION_NAME]

# MARKET column related constants
RAW_MARKET_COLUMN_NAME = 'Market'
HARMONIZED_MARKET_COLUMN_NAME = 'Harmonized_Market'
HARMONIZED_COUNTRY_COLUMN_NAME = 'Harmonized_Country'
USA_COUNTRY_STANDARD_NAME = 'USA'
MARKET_MAPPING_TO_USA = {
        'USH': USA_COUNTRY_STANDARD_NAME,
        'AA': USA_COUNTRY_STANDARD_NAME,
        'US': USA_COUNTRY_STANDARD_NAME
}
PREFIX_FOR_MARKET_HILLS = 'Hills'
HARMONIZED_MARKET_TO_COMP_HARM_STANDARD_COUNTRY_NAME_MAPPINGS = {
    'Angola': 'Angola',
    'Argentina': 'Argentina',
    'Australia': 'Australia',
    'Austria': 'Austria',
    'Azerbaijan': 'Azerbaijan',
    'Belarus': 'Belarus',
    'Belgium': 'Belgium',
    'Benin': 'Benin',
    'Brazil': 'Brazil',
    'Burkina Faso': 'Burkina Faso',
    'Cambodia': 'Cambodia',
    'Cameroon': 'Cameroon',
    'Canada': 'Canada',
    'Caricom': 'Caricom',
    'Chad': 'Chad',
    'Chile': 'Chile',
    'China': 'China',
    'Colombia': 'Colombia',
    'Congo': 'Congo',
    'Costa Rica': 'Costa Rica',
    'Czech Republic': 'Czech Republic',
    'DRC': 'DRC',
    'Denmark': 'Denmark',
    'Dominican Republic': 'Dominican Republic',
    'Ecuador': 'Ecuador',
    'El Salvador': 'El Salvador',
    'Estonia': 'Estonia',
    'Ethiopia': 'Ethiopia',
    'Finland': 'Finland',
    'France': 'France',
    'French Overseas Territory': 'French Overseas Territory',
    'GCC': 'GCC', # Bahrain, Kuwait, Oman, Pan Asian, Pan Arab, Saudi Arabia, Qatar, United Arab Emirates
    'Gabon': 'Gabon',
    'Georgia': 'Georgia',
    'Germany': 'Germany',
    'Ghana': 'Ghana',
    'Greece': 'Greece',
    'Guatemala': 'Guatemala',
    'Guinea': 'Guinea',
    'Hills Australia': 'Hills Australia',
    'Hills Canada': 'Hills Canada',
    'Hills USA': 'Hills USA',
    'Honduras': 'Honduras',
    'Hong Kong': 'Hong Kong',
    'Hungary': 'Hungary',
    'India': 'India',
    'Indonesia': 'Indonesia',
    'Ireland': 'Ireland',
    'Israel': 'Israel',
    'Italy': 'Italy',
    'Ivory Coast': 'Ivory Coast',
    'Jordan': 'Jordan',
    'Kazakhstan': 'Kazakhstan',
    'Kenya': 'Kenya',
    'Kyrgyztan': 'Kyrgyztan',
    'Laos': 'Laos',
    'Latvia': 'Latvia',
    'Lebanon': 'Lebanon',
    'Lithuania': 'Lithuania',
    'Malawi': 'Malawi',
    'Malaysia': 'Malaysia',
    'Mali': 'Mali',
    'Mauritania': 'Mauritania',
    'Mexico': 'Mexico',
    'Mongolia': 'Mongolia',
    'Morocco': 'Morocco',
    'Mozambique': 'Mozambique',
    'Myanmar': 'Myanmar',
    'Netherlands': 'Netherlands',
    'New Zealand': 'New Zealand',
    'Nicaragua': 'Nicaragua',
    'Niger': 'Niger',
    'Nigeria': 'Nigeria',
    'Norway': 'Norway',
    'Pan Regional': 'Pan Regional',
    'Panama': 'Panama',
    'Paraguay': 'Paraguay',
    'Peru': 'Peru',
    'Philippines': 'Philippines',
    'Poland': 'Poland',
    'Portugal': 'Portugal',
    'Puerto Rico': 'Puerto Rico',
    'Romania': 'Romania',
    'Russia': 'Russia',
    'Rwanda': 'Rwanda',
    'Senegal': 'Senegal',
    'Singapore': 'Singapore',
    'Slovakia': 'Slovakia',
    'South Africa': 'South Africa',
    'Spain': 'Spain',
    'Sweden': 'Sweden',
    'Switzerland': 'Switzerland',
    'Taiwan': 'Taiwan',
    'Tanzania': 'Tanzania',
    'Thailand': 'Thailand',
    'Togo': 'Togo',
    'Tunisia': 'Tunisia',
    'Turkey': 'Turkey',
    'UK': 'United Kingdom',
    'USA': 'USA',
    'Uganda': 'Uganda',
    'Ukraine': 'Ukraine',
    'Uruguay': 'Uruguay',
    'Uzbekistan': 'Uzbekistan',
    'Venezuela': 'Venezuela',
    'Vietnam': 'Vietnam',
    'Zambia': 'Zambia',
    'Zimbabwe': 'Zimbabwe'
}

# YEAR column related constants
RAW_YEAR_COLUMN_NAME = 'Year'
HARMONIZED_YEAR_COLUMN_NAME = 'Harmonized_Year'
EXPECTED_MINIMUM_YEAR = 2012

# CATEGORY column related constants
RAW_CATEGORY_COLUMN_NAME = 'Category'
HARMONIZED_CATEGORY_COLUMN_NAME = 'Harmonized_Category'

# We will merge comp harm's standard category names
# with the additional category names found in Budget roll-up
RAW_TO_HARMONIZED_CATEGORY_NAME_MAPPING = CATEGORY_MAPPINGS.copy()
RAW_TO_HARMONIZED_CATEGORY_NAME_MAPPING.update({
    "(?i)^Baby$": 'Baby',
    "(?i)^Pet$": 'Pet'
})
EXPECTED_CATEGORY_COLUMN_VALUES = list(RAW_TO_HARMONIZED_CATEGORY_NAME_MAPPING.keys())

#SUBCATEGORY => SEGMENT MACRO colum related constants
RAW_SEGMENT_MACRO_COLUMN_NAME = 'Segment Macro'
HARMONIZED_SUBCATEGORY_COLUMN_NAME = 'Harmonized_Subcategory'

RAW_TO_HARMONIZED_SUBCATEGORY_NAME_MAPPING={
    "(?i)^PC$": 'PC Product Range',
    "(?i)^HC$": 'HC Product Range',
    "(?i)^home$": 'HC Product Range',
    "(?i)^personal$": 'HC Product Range',
    "(?i)^Toothpaste$":'Toothpaste',
    "(?i)^OC$":'OC',
    "(?i)^Female UAP$":'Female UAP',
    "(?i)^Toothbrush$":'Toothbrush',
    "(?i)^Dental Floss$":'Dental Floss',
    "(?i)^Mouthwash$":'Mouthwash',
    "(?i)^Dish Cleaners$":'Dish Cleaners',
    "(?i)^Anti-Bacterial Cleansers'$":'Anti-Bacterial Cleansers',
    "(?i)^Female Body Cleansers$":'Female Body Cleansers',
    "(?i)^Body Lotion$":'Body Lotion',
    "(?i)^Fabric Conditioners$":'Fabric Conditioners',
    "(?i)^Male UAP$":'Male UAP',
    "(?i)^Bar Soap$":'Bar Soap',
    "(?i)^Floor Cleaner$":'Floor Cleaner',
    "(?i)^Hair Care Shampoo$":'Hair Care Shampoo',
    "(?i)^Cleaners$":'Cleaners',
    "(?i)^Male Body Cleansers$":'Male Body Cleansers',
    "(?i)^Body Wash$":'Body Wash',
    "(?i)^Hair Care Conditioner$":'Hair Care Conditioner',
    "(?i)^Pet Food$":'Pet Food',
    "(?i)^Liquid Hand Soap$":'Liquid Hand Soap',
    "(?i)^Talcum Powder$":'Talcum Powder',
    "(?i)^Baby Care$":'Baby Care',
    "(?i)^Floor Cleaners$":'Floor Cleaners'
}
EXPECTED_SUBCATEGORY_COLUMN_VALUES = list(RAW_TO_HARMONIZED_SUBCATEGORY_NAME_MAPPING.keys())

# CHANNEl column related constants
RAW_CHANNEL_COLUMN_NAME = 'Channel'
HARMONIZED_CHANNEL_COLUMN_NAME = 'Harmonized_Channel '

RAW_TO_HARMONIZED_CHANNEL_NAME_MAPPING={
    "(?i)^GDN Display (non-programmatic)$": 'Display (Google)',
    "(?i)^GDN Video (non-programmatic)$": 'Display (Google)',
    "(?i)^GDN Display (programmatic)$": 'Display (Google)',
    "(?i)^GDN Video (programmatic)$": 'Display (Google)',
    "(?i)^YouTube$":'Online Video (Google)',
    "(?i)^Amazon$":'eCommerce (Amazon)',
    "(?i)^Facebook$":'Social (Facebook)',
    "(?i)^Programmatic$":'Programmatic',
    "(?i)^Paid Search$":'Search',
    "(?i)^SEO$":'Search',
    "(?i)^PR/Influencers$":'Other Digital',
    "(?i)^Online Partnership$":'Other Digital',
    "(?i)^Ecommerce$":'eCommerce (Other)',
    "(?i)^Online Display$":'Display (Other)',
    "(?i)^Mobile Display$":'Display (Other)',
    "(?i)^Mobile Video$":'Online Video (Other)',
    "(?i)^OLV/Preroll/VOD$":'Online Video (Other)',
    "(?i)^TV$":'TV',
    "(?i)^Print$":'Print',
    "(?i)^Other Digital$":'Other Digital',
    "(?i)^Other Social$":'Social (Other)',
    "(?i)^Other$":'Other Non-Digital',
    "(?i)^Google Preferred$":'Online Video (Google)',
    "(?i)^Desktop Video$":'Online Video (Other)',
    "(?i)^DV360 Video$":'Online Video (Other)',
    "(?i)^Desktop Display$":'Display (Other)',
    "(?i)^DV360 Display$":'Display (Other)',
    "(?i)^Audio$": 'Audio',
    "(?i)^GDN Video": 'Display (Google)',
    "(?i)^GDN Display": 'Display (Google)',
    "(?i)^YouTube/Trueview": 'Online Video (Google)',
}
EXPECTED_CHANNEL_COLUMN_VALUES = list(RAW_TO_HARMONIZED_CHANNEL_NAME_MAPPING.keys())




