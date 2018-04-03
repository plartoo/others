import pdb
import sys
import pandas as pd

expected_column_headers = ['Date', 'Market', 'Station', 'Date',
                           'ADVERTISER_NAME', 'BRAND_DESC', 'PRODUCT_CATEGORY',
                           'Station', 'Start Time', 'Duration', 'Title',
                           'Title Top Level', 'Break Position', 'NO_SPOTS_CB',
                           'Commercial Position', 'Rat (%)', 'NoP', 'Rate',
                           'Cum. Rate', 'Cum. CPP', 'CumGRP (%)',
                           'CumNetRch (%) (C3+)', 'OTS', 'SoM', 'SoV (Rate)']

column_headers_needed = ['Date', 'ADVERTISER_NAME', 'BRAND_DESC', 'PRODUCT_CATEGORY',
                         'Title', 'Station', 'Title Top Level',
                         'Start Time', 'Duration', 'NO_SPOTS_CB', 'CumGRP (%)']

fname = "TRP_data.xlsx"
temp_fname = 'temp_'+fname+'.csv'
df1=pd.read_excel(fname)

# df1=df.drop(df.index[:3])
df1.to_csv(temp_fname, index=False)
df2 = pd.read_csv(temp_fname)
l2 = df2.values.tolist()
# pdb.set_trace()
potential_headers = []
last_header_row_index = 0
for row in df2.iterrows():
    index, data = row
    if len(set(expected_column_headers).intersection(set(data))) > 5:
        last_header_row_index = index
        potential_headers.append(data)

if len(potential_headers) == 2:
    # REF: https://stackoverflow.com/a/41693529
    column_headers_found = potential_headers[0].combine_first(potential_headers[1])
else:
    print(potential_headers)
    sys.exit('The header format probably has changed. Please review the code.')

if not set(column_headers_needed).issubset(set(column_headers_found)):
    print(potential_headers)
    print(column_headers_needed)
    sys.exit('Cannot find all headers needed in the raw data. Please review the code and raw data.')



df3 = df2[last_header_row_index+1:]
df3.columns = column_headers_found
df4 = df3.dropna(thresh=4) # REF: https://stackoverflow.com/a/22553757
df5 = df4.fillna(method='ffill')

if df5.columns[0] == df5.columns[3]:
    cols = df5.columns.tolist()
    cols[0] = 'To_Delete'
    df5.columns = cols
    df5 = df5.drop(['To_Delete'], axis=1)
    # df5 = df5.drop(df5.columns[0], axis=1)
else:
    sys.exit('There used to be two Date columns and we usually drop the first one. Now it has changed. '
             'Please inspect the raw data and the code.')

if df5.columns[1] == df5.columns[6]:
    cols = df5.columns.tolist()
    cols[1] = 'To_Delete'
    df5.columns = cols
    df5 = df5.drop(['To_Delete'], axis=1)
else:
    sys.exit('There used to be two Station columns and we usually drop the first one. Now it has changed. '
             'Please inspect the raw data and the code.')

columns_to_drop = list(set(df5.columns).difference(set(column_headers_needed)))
df5 = df5.drop(columns_to_drop, axis=1)
df5.to_csv('test_ffilled_2.csv', index=False)
# pdb.set_trace()

# columns = df2.columns
# for row in df2.iterrows():
#     pdb.set_trace()
#     print('')

print('finished')

# df3=pd.read_csv('test.csv')
# df4=df3.fillna(method='ffill')
# df4.to_csv('test_ffilled.csv')
# pd.to_datetime(df4.loc[4]['Report: Col Pal Monthly TV Data Reporting.rep'])