country_metadata = """
SELECT *
FROM [DM_1219_ColgateGlobal].[dbo].[CP_DIM_COUNTRY]
"""

demographic ="""
SELECT 
    [Demographics], [TA Dim Text], [Dim Type], [Dim Type Text], 
    [Is Gbl TA? Key], [Is Gbl TA? Text], [Global Name], 
    [Global Name Text], [Sort Number] 
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_DEMO_DM]
"""

geography = """
SELECT 
    [Geography Dim], [Geo Dim Text], [Dim Type], [Dim Type Text], 
    [Division], [Subdivision], [Hub], [Country], [Region], 
    [Region Text], [SubRegion], [SubRegion Text], [Province], 
    [ProvinceText], [CityTier], [CityTier Text], [City], [City Text] 
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_GEO_DM]
"""

product = """
SELECT 
    [Product Dim], [Product Dim Text], [Dim Type], [Dim Type Text], 
    [6L Category], [6L Subcategory], [6L Brand], [6L Subbrand], 
    [6L Variant], [1PH Category], [1PH Subcategory], [1PH ProductCategory], 
    [1PH Brand], [1PH Subbrand], [1PH Variant] 
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_PROD_DM]
"""

media = """
SELECT 
    [Media Dim], [Media Dim Text], [Dim Type], [Dim Type Text], 
    [Media lvl 1], [Media lvl 1 text], [Media lvl 2], [Media lvl 2 text], 
    [Media lvl 3], [Media lvl 3 text], [Spot Length], [Spot  Bucket Length] 
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_MEDIA_DM]
"""

creative = """
SELECT 
    [Creative Dim], [Creative Dim text], [Dim Type], [Dim Type Text], 
    [Global Name], [Global Name Text] 
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_CREA_DM]
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
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_BRAND_MANF]
"""

# TODO: Fix incorrect format for country_id and subcat_key columns in our db
market_subcat = """
SELECT 
    CAST([Country ID] AS INT) AS [Country ID], 
    CAST([Subcategory Key] AS INT) AS [Subcategory Key],
    [C/NC Flag],
    [C/NC Text]
FROM [DM_1219_ColgateGlobal].[dbo].[V_MED_MARKET_SUBCAT]
"""

# TODO:
channel = """
Jholman will reate this view later 
"""

dim_queries = [
    {'query': demographic, 'output_file_basename': 'MED_DEMO_DM_ALL'},
    {'query': geography, 'output_file_basename': 'MED_GEO_DM_ALL'},
    {'query': product, 'output_file_basename': 'MED_PROD_DM_ALL'},
    {'query': media, 'output_file_basename': 'MED_MEDIA_DM_ALL'},
    {'query': creative, 'output_file_basename': 'MED_CREA_DM_ALL'},
    {'query': network, 'output_file_basename': 'MED_NETWORK_DM_ALL'},
    {'query': daypart, 'output_file_basename': 'MED_DAYPART_DM_ALL'},
    {'query': brand, 'output_file_basename': 'MED_BRAND_MANUF_ALL'},
    {'query': market_subcat, 'output_file_basename': 'MED_MARKET_SUBCAT_ALL'},
    # {'MED_CHANNEL_DM_ALL':, 'split_file': False}, # TODO: add after Jholman created channel view
]


def get_fact_query(country_metadata):
    # TODO: we have type mismatch between APAC tables and rest-of-the-world tables
    fact_query_non_APAC = """
    SELECT	[Geography Dim], [Product Dim], [Media Dim], [Demographic Dim], [Creative Dim],
        [Daypart Dim], [Network Dim], [Month Year], [Country ID], [Local Currency], 
        [Spend Local], [Spend USD], [TRP], [Normalized TRP], [Insertions], [Impressions] 
    FROM [DM_1219_ColgateGlobal].[dbo].[V_Transaction_Data] 
    WHERE [COUNTRY ID] = @CP_COUNTRY_ID
    """

    # fact_query_APAC = """
    # SELECT	[Geography Dim], [Product Dim], [Media Dim], [Demographic Dim], [Creative Dim],
    #     [Daypart Dim], [Network Dim], [Month/Year] AS [Month Year], [Country] AS [Country ID],
    #     [Local Currency], [Spend Local], [Spend USD], [TRP], [Normalized TRP], [Insertions],[Impressions]
    # FROM [DM_1035_ColgateAPACCompetitive].[dbo].[MED_KF_@MERGED_COUNTRY_KEY]
    # """
    fact_query_APAC = """
    SELECT	[Geography Dim], [Product Dim], [Media Dim], [Demographic Dim], [Creative Dim],
        [Daypart Dim], [Network Dim], [Month/Year] AS [Month Year], [Country] AS [Country ID], 
        [Local Currency], 
        CAST([Spend Local] AS DECIMAL(18,2)) AS [Spend Local], 
        CAST([Spend USD] AS INT) AS [Spend USD], 
        CAST([TRP] AS DECIMAL(38,2)) AS [TRP], 
        CAST([Normalized TRP] AS DECIMAL(38,2)) AS [Normalized TRP], 
        CAST([Insertions] AS INT) AS [Insertions], 
        CAST([Impressions]  AS DECIMAL(38,2)) AS [Impressions] 
    FROM [DM_1035_ColgateAPACCompetitive].[dbo].[MED_KF_@MERGED_COUNTRY_KEY]    
    """

    output_file = 'MED_KF_'
    if country_metadata['division_text'] == 'Asia':
        query = fact_query_APAC.replace('@MERGED_COUNTRY_KEY', str(country_metadata['merged_country_key']))
        output_file += str(country_metadata['merged_country_key'])
    else:
        query = fact_query_non_APAC.replace('@CP_COUNTRY_ID', str(country_metadata['cp_country_id']))
        output_file += str(country_metadata['country_key'])

    return {'query': query, 'output_file_basename': output_file}
