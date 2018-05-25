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
