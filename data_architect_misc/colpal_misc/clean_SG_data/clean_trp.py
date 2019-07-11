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

fname = "TRP_data.xlsx" # raw data file name
outfile = "cleaned_TRP_data.csv"

df1=pd.read_excel(fname)
l2 = df1.values.tolist()

# 1. Verify if expected headers show up
potential_headers = []
last_header_row_index = 0
for row in df1.iterrows():
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


# 2. Drop some columns that we don't need
df2 = df1[last_header_row_index + 1:]
df2.columns = column_headers_found

df3 = df2
if df3.columns[0] == df3.columns[3]:
    cols = df3.columns.tolist()
    cols[0] = 'To_Delete'
    df3.columns = cols
    df3 = df3.drop(['To_Delete'], axis=1)
else:
    sys.exit('There used to be two Date columns and we usually drop the first one. Now it has changed. '
             'Please inspect the raw data and the code.')

if df3.columns[1] == df3.columns[6]:
    cols = df3.columns.tolist()
    cols[1] = 'To_Delete'
    df3.columns = cols
    df3 = df3.drop(['To_Delete'], axis=1)
else:
    sys.exit('There used to be two Station columns and we usually drop the first one. Now it has changed. '
             'Please inspect the raw data and the code.')

columns_to_drop = list(set(df3.columns).difference(set(column_headers_needed)))
df3 = df3.drop(columns_to_drop, axis=1)

# 3. Drop rows that have too many holes (arbitrary but safe threshold for blank cells per row to delete=4)
df3 = df3.dropna(thresh=4) # REF: https://stackoverflow.com/a/22553757

# 4. Forward fill some cells below using the data from above (most adjacent) cells
df3 = df3.fillna(method='ffill')

# 5. Write to output file
df3.to_csv(outfile, index=False)

print('Cleaned TRP file. Output written to:', outfile)