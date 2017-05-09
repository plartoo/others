import os
import time
import schedule
import pandas as pd
import pypyodbc

from account_info import *

def main():
    print("\nCategorization code started at:", time.ctime(), "\n")
    connection = pypyodbc.connect(CONNECTION_INFO)
    cursor= connection.cursor()
    sql_cmd = ("select * from [DM_1305_GroupMBenchmarkingUS].[dbo].[Analytics_Final_Base_Workload_Categorization_Step4]")
    df = pd.read_sql(sql_cmd, connection)
    columns = df.columns

    df2 = pd.DataFrame(columns=df.columns)

    for name, gp in df.groupby('campaignname'):
        sorted_gp = gp.groupby(['campaignname','category_type_final']).sum().sort_values(['allocated_plannedamount'], ascending=False)
        cur_row = [sorted_gp.iloc[0].name[0], sorted_gp.iloc[0].name[1], sorted_gp.iloc[0].values.tolist()[0]]

        if (len(sorted_gp) > 1) and (len(set(sorted_gp.allocated_plannedamount.apply(lambda x: '{0:.2f}'.format(x)))) == 1):
            cur_category = 'Other Category'
            cur_row[1] = cur_category

        d = dict(zip(columns, cur_row))
        df2 = df2.append(d, ignore_index=True)


    truncate_sql = """
        USE [DM_1305_GroupMBenchmarkingUS];
        IF OBJECT_ID('Analytics_Final_Base_Workload_Categorization_Step5') IS NOT NULL
        DROP TABLE [DM_1305_GroupMBenchmarkingUS].[dbo].[Analytics_Final_Base_Workload_Categorization_Step5];
        CREATE TABLE [DM_1305_GroupMBenchmarkingUS].[dbo].[Analytics_Final_Base_Workload_Categorization_Step5]
           (
           CampaignName VARCHAR(MAX),
            category_type_Final VARCHAR(MAX),
            Allocated_PlannedAmount FLOAT
            );

       COMMIT;
    """
    cursor.execute(truncate_sql)

    df2 = df2.fillna(0)
    for index, row in df2[['campaignname','category_type_final','allocated_plannedamount']].iterrows():
        insert_sql = "INSERT INTO [DM_1305_GroupMBenchmarkingUS].[dbo].[Analytics_Final_Base_Workload_Categorization_Step5] " + \
                     "([CampaignName], [category_type_Final], [Allocated_PlannedAmount]) VALUES (?, ?, ?)"
        cursor.execute(insert_sql,
                       (row['campaignname'], row['category_type_final'], row['allocated_plannedamount']))
        cursor.commit()

    cursor.close()
    connection.close()
    print("\nCategorization code finished at:", time.ctime(), "\n")


if __name__ == "__main__":
    print("\n\n*****DO NOT KILL this program::", os.path.basename(__file__) ,"*****\n")
    print("If you accidentally or intentionally killed this program, please rerun it")
    print("This program runs processes every: friday at 6:00am EST")

    schedule.every().friday.at("6:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(30)
