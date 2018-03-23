country_metadata = """
SELECT 
    [CP_COUNTRY_ID],[COUNTRY_KEY],[COUNTRY_NAME],[GM_COUNTRY_ID],
    [HUB_ID],[HUB_KEY],[HUB_TEXT],[SUBDIVISION_ID],[SUBDIVISION_KEY],
    [SUBDIVISION_TEXT],[DIVISION_ID],[DIVISION_KEY],[DIVISION_TEXT],
    [ADD_DATE] 
FROM [DM_1219_ColgateGlobal].[dbo].[CP_DIM_COUNTRY]
"""

demographic ="""
SELECT 
    [Demographics], [TA Dim Text], [Dim Type], [Dim Type Text], 
    [Is Gbl TA? Key], [Is Gbl TA? Text], [Global Name], 
    [Global Name Text], [Sort Number] 
FROM [dbo].[V_MED_DEMO_DM]
"""

geography = """
SELECT 
    [Geography Dim], [Geo Dim Text], [Dim Type], [Dim Type Text], 
    [Division], [Subdivision], [Hub], [Country], [Region], 
    [Region Text], [SubRegion], [SubRegion Text], [Province], 
    [ProvinceText], [CityTier], [CityTier Text], [City], [City Text] 
FROM [dbo].[V_MED_GEO_DM]
"""

product = """
SELECT 
    [Product Dim], [Product Dim Text], [Dim Type], [Dim Type Text], 
    [6L Category], [6L Subcategory], [6L Brand], [6L Subbrand], 
    [6L Variant], [1PH Category], [1PH Subcategory], [1PH ProductCategory], 
    [1PH Brand], [1PH Subbrand], [1PH Variant] 
FROM [dbo].[V_MED_PROD_DM]
"""

media = """
SELECT 
    [Media Dim], [Media Dim Text], [Dim Type], [Dim Type Text], 
    [Media lvl 1], [Media lvl 1 text], [Media lvl 2], [Media lvl 2 text], 
    [Media lvl 3], [Media lvl 3 text], [Spot Length], [Spot  Bucket Length] 
FROM [dbo].[V_MED_MEDIA_DM]
"""

creative = """
SELECT 
    [Creative Dim], [Creative Dim text], [Dim Type], [Dim Type Text], 
    [Global Name], [Global Name Text] 
FROM [dbo].[V_MED_CREA_DM]
"""

network = """
SELECT 
    [Network Dim],[Network Dim Text] 
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_NETWORK_DM] 
"""

daypart = """
SELECT 
    [Daypart Dim],[Daypart Dim Text] 
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_DAYPART_DM]
"""

brand = """
SELECT 
    [Country ID], [CountryName], [BrandID], [BrandName], 
    [LocalManuf], [GlobalManuf], [StartDate] 
FROM [dbo].[V_MED_BRAND_MANF]
"""

market_subcat = """
SELECT 
    [Country ID], [Subcategory Key], [C/NC Flag], [C/NC Text] 
FROM [dbo].[V_MED_MARKET_SUBCAT]
"""

# TODO:
channel = """
Jholman will reate this view later 
"""

dim_queries = [
    {'MED_DEMO_DM_ALL': demographic, 'split_file': False},
    {'MED_GEO_DM_ALL': geography, 'split_file': False},
    {'MED_PROD_DM_ALL': product, 'split_file': False},
    {'MED_MEDIA_DM_ALL': media, 'split_file': False},
    {'MED_CREA_DM_ALL': creative, 'split_file': False},
    {'MED_NETWORK_DM_ALL': network, 'split_file': False},
    {'MED_DAYPART_DM_ALL': daypart, 'split_file': False},
    {'MED_BRAND_MANUF_ALL': brand, 'split_file': False},
    {'MED_MARKET_SUBCAT_ALL': market_subcat, 'split_file': False},
    # {'MED_CHANNEL_DM_ALL':, 'split_file': False}, # TODO: add after Jholman created channel view
]

def get_fact_query(country_metadata):
    fact_query_non_APAC = """
    SELECT	[Geography Dim], [Product Dim], [Media Dim], [Demographic Dim], [Creative Dim], 
    		[Daypart Dim], [Network Dim], [Month Year], [Country ID], [Local Currency], 
    		[Spend Local], [Spend USD], [TRP], [Normalized TRP], [Insertions], [Impressions] 
    FROM [dbo].[V_Transaction_Data] 
    WHERE [COUNTRY ID] = @CP_COUNTRY_ID 
    """

    fact_query_APAC = """
    SELECT	[Geography Dim], [Product Dim], [Media Dim], [Demographic Dim], [Creative Dim], 
    		[Daypart Dim], [Network Dim], [Month/Year] AS [Month Year], [Country] AS [Country ID], 
    		[Local Currency], [Spend Local], [Spend USD], [TRP], [Normalized TRP], [Insertions],[Impressions]  
    FROM [dbo].[MED_KF_@MERGED_COUNTRY_KEY] 
    """

    query = None
    if country_metadata['DIVISION_TEXT'] == 'Asia':
        query = fact_query_APAC.replace('@MERGED_COUNTRY_KEY', country_metadata['MERGED_COUNTRY_KEY'])
    else:
        query = fact_query_non_APAC.replace('@CP_COUNTRY_ID', country_metadata['CP_COUNTRY_ID'])

    return {'MED_KF_': query, 'split_file': True, 'by_row_count': {}