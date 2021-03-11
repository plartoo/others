"""
Script to demo Komal that we can quickly extract
a good chunk of data from SQL Server and use that
to filter out the already-mapped data.

Created On: March 1, 2021
"""

import pdb
import sys
import time

import pandas as pd
import pyodbc

from queries import mapped_data_for_country
from sql_server_account_info import server, database, username, password


def load_unmapped_data(file_name, sep='|'):
    return pd.read_csv(file_name, sep=sep)


def get_country_name(df):
    country = df['HARMONIZED_COUNTRY'].unique()
    if len(country) > 1:
        sys.exit(f"Found more than one country in the unmapped data file.")
    return country[0].strip()


def get_query_to_fetch_mapped_data(df, country_name):
    return ''.join([mapped_data_for_country, country_name, "'"])


def main():
    # Columns we will use to determine if a row is already mapped
    key_cols = ['HARMONIZED_COUNTRY', 'HARMONIZED_ADVERTISER',
                'RAW_CATEGORY', 'RAW_SUBCATEGORY', 'RAW_BRAND',
                'RAW_SUBBRAND', 'RAW_PRODUCT_NAME']

    # Get unmapped data from the transformed file
    unmapped_df = load_unmapped_data('Transformed_India_20210101_20210131__rows_0_72559_20210301_153304.csv', '|')
    # unmapped_df = load_unmapped_data('Test_Transformed_Data.csv', ',')

    country_name = get_country_name(unmapped_df)
    query = get_query_to_fetch_mapped_data(unmapped_df, country_name)
    print(f"\n=>Query to run:{query}\n")

    start_t = time.perf_counter()
    # REF: https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15
    connection = pyodbc.connect(
        ''.join([
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=', server,
            ';DATABASE=', database,
            ';UID=', username,
            ';PWD=', password
        ]))
    # REF: https://github.com/mkleehammer/pyodbc/wiki/Cursor
    cursor = connection.cursor()
    cursor.execute(query)
    col_headers = [header[0] for header in cursor.description]
    data = [list(row) for row in cursor.fetchall()]
    mapped_df = pd.DataFrame(data, columns=col_headers)
    cursor.commit()
    cursor.close()
    connection.close()
    stop_t = time.perf_counter()
    print(f"\n=>Time taken to extract mapped data for {country_name} to dataframe (secs): {stop_t - start_t}")

    # Drop the duplicate rows in the unmapped df to reduce computation, and convert all cols to str type for left join
    # VERY IMPORTANT: we need to call fillna('N/A') because pandas and pyodbc reads NULL values differently
    # If we don't call fillna('N/A') here, the left join below will not return correct results
    unmapped_unique_df = unmapped_df[key_cols].drop_duplicates().fillna('N/A').astype(str)
    mapped_unique_df = mapped_df[key_cols].drop_duplicates().fillna('N/A').astype(str)

    # REF: https://kanoki.org/2019/07/04/pandas-difference-between-two-dataframes/
    truly_unmapped_df = unmapped_unique_df.merge(mapped_unique_df, how='outer', indicator=True).loc[
        lambda x: x['_merge'] == 'left_only']
    print(f"\n=>List of never-mapped row(s):")
    print(truly_unmapped_df[truly_unmapped_df['_merge'] == 'left_only'])


if __name__ == '__main__':
    main()

# Related REF about how we can leverage executemany if we ever need to insert many rows at once to SQL SERVER DB
# REF: https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
