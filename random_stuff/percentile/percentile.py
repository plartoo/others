"""
Author: Phyo Thiha
Last Modified Date: October 7, 2019
Description: Script to calculate percentiles for Budget Roll-up data visualization
in WorldView Tableau.
"""

import pandas as pd

# TODO: Tell Jholman about removing 'Global' line because it can be taken care of by the code
# For Jholman: read about percentiles/quantiles
# https://www.dummies.com/education/math/statistics/how-to-calculate-percentiles-in-statistics/
# Based on what Jholman asked, we are configuring Tableau filters like this:
# Year				Region			Country					Category
# 2018 (no All)		(no All)		All is available		All available
# Other notes:
# percentile rank: http://www.datasciencemadesimple.com/percentile-rank-column-pandas-python-2/
# df1['Percentile_rank']=df1.Mathematics_score.rank(pct=True)

PERCENTILE_SPLIT = 0.2 # We are interested in 80-20 split
FILE_NAME = 'Budget Roll Up Data.xlsx'
OUTPUT_FILE_NAME = 'BudgetRollUpData_Percentile_programmatic_output.csv'
SPEND_COL_NAME = 'Budget'
USE_COLUMNS = ['Year', 'Region', 'Market', 'Category', 'Segment Macro', 'Brand', 'Budget (USD)']
REORDERED_FINAL_COLUMNS = ['Year','Region','Country','Category','Subcategory','Brand','Budget']
RENAME_COLUMNS = {'Market': 'Country',
                  'Segment Macro': 'Subcategory',
                  'Budget (USD)': 'Budget'}
GROUP_BYS = [['Year'], ['Year', 'Region'], ['Year', 'Region', 'Country'],
             ['Year', 'Region', 'Country', 'Category'], ['Year', 'Region', 'Country', 'Category', 'Subcategory']]

# The following block is only used for testing toy example
# FILE_NAME = 'example_input.xlsx'
# OUTPUT_FILE_NAME = 'example_qa_output.csv'
# SPEND_COL_NAME = 'Spend'
# USE_COLUMNS = ['Year', 'Region', 'Country', 'Category', 'Spend']
# REORDERED_FINAL_COLUMNS = ['Year','Region','Country','Category','Spend']
# RENAME_COLUMNS = {'Year': 'Year'}
# GROUP_BYS = [['Year'], ['Year', 'Region'], ['Year', 'Region', 'Country']]

df = pd.read_excel(FILE_NAME, usecols = USE_COLUMNS)
df = df.rename(columns=RENAME_COLUMNS)
df = df[REORDERED_FINAL_COLUMNS]

for gb in GROUP_BYS:
    new_percentile_col_name = ''.join(['20P_'] + gb)
    # REF: https://stackoverflow.com/questions/36944884/calculating-percentile-for-specific-groups
    df[new_percentile_col_name] = df.groupby(gb)[SPEND_COL_NAME].transform(lambda x: x.quantile(PERCENTILE_SPLIT))
    # We need the line below because Jholman had 'Global' line already calculated in the raw file
    df[REORDERED_FINAL_COLUMNS] = df[REORDERED_FINAL_COLUMNS].fillna('All')

# dfs = []
# for gb in GROUP_BYS[:-1]:
#     # Tried this, but didn't get quite the output we desired (compacted the df too much)
#     # REF: https://stackoverflow.com/a/58280720/1330974
#     dfs.append(df.groupby(gb)[SPEND_COL_NAME].sum().reset_index())
# df = pd.concat(dfs, ignore_index=True, sort=False) # .fillna('All').sort_values(by=GROUP_BYS[-1])

for gb in GROUP_BYS[:-1]:
    # REF: https://stackoverflow.com/questions/39922986/pandas-group-by-and-sum
    df = df.append(df.groupby(gb)[SPEND_COL_NAME].sum().to_frame().reset_index(),
                   ignore_index=True, sort=False)

# Fill 'Nan' in label columns with 'All' (for summary rows)
df[REORDERED_FINAL_COLUMNS] = df[REORDERED_FINAL_COLUMNS].fillna('All')

# Forward fill values in percentile value columns
df = df.ffill()
df = df.sort_values(by=GROUP_BYS[-1])
df.to_csv(OUTPUT_FILE_NAME, index=False)
print("Done calculating percentiles and wrote the output as:", OUTPUT_FILE_NAME)
