DATABASE = "[WM_RF_DB_Colgate].[VIZ]"

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
  FROM {}.[Phyo_Custom_Dashboard_Data_Hierarchy_20190709_Do_Not_Delete_Without_Permission]
  ORDER BY 1,2,3,4,5
""".format(DATABASE)

spend_by_country_advertiser = """
SELECT [Year]
      ,[Region]
      ,[Country]
      ,[Advertiser]
      ,[SumOfSpend]
      ,[UniqBrandCount]
  FROM {}.[Phyo_Custom_Dashboard_Data_Hierarchy_20190709_Do_Not_Delete_Without_Permission]
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

spend_by_country_advertiser_subbrand = """
SELECT [Period]
      ,[Region]
      ,[Country]
      ,[Advertiser]
      ,[Subbrand] AS [Brand]
      ,[SumOfSpend]
  FROM {}.[DFID065658_SampleDataForDashboard_Spend_By_Subbrand]
""".format(DATABASE)
