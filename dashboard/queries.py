DATABASE = "[DM_1219_ColgateGlobal].[dbo]"

hierarchy_table = """
SELECT [Year]
      ,[Region]
      ,[Country]
      ,[Advertiser]
	  ,[Brand]
      ,[SumOfSpend]
      ,[UniqBrandCount]
      ,[UniqRegionCount]
      ,[UniqCountryCount]
      ,[UniqAdvertiserCount]
  FROM {}.[DFID065658_SampleDataForDashboard_Hierarchy]
  ORDER BY 1,2,3,4,5
""".format(DATABASE)

spend_by_country_advertiser = """
SELECT [Year]
      ,[Region]
      ,[Country]
      ,[Advertiser]
      ,[SumOfSpend]
      ,[UniqBrandCount]
  FROM {}.[DFID065658_SampleDataForDashboard_Hierarchy]
  WHERE
  [YEAR] IS NOT NULL
  AND
  [REGION] IS NOT NULL
  AND
  [COUNTRY] IS NOT NULL
  AND
  [ADVERTISER] IS NOT NULL
  AND
  [BRAND] IS NULL
""".format(DATABASE)

spend_by_country_advertiser_brand = """
SELECT [Period]
      ,[Region]
      ,[Country]
      ,[Advertiser]
      ,[Brand]
      ,[SumOfSpend]
  FROM {}.[DFID065658_SampleDataForDashboard_Spend_By_Brand]
""".format(DATABASE)