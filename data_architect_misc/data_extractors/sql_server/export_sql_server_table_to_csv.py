"""
Author: Phyo Thiha
Description:
A simple Python script to download data as CSV files from SQL Server tables.
This script can be used to create back-up files of your SQL Server tables.
You can use Export option in SQL Server Management Studio, but
in practice, it can be slow.
"""
import argparse
import csv
import os
import pyodbc

from sql_server_account_info import server, database, username, password


tables_to_download = [
    # Provide a list of tables to back-up into CSV files
    'dbo.Fact_Media_Monthly_DEN',
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Script to download several SQL Server tables.",
        formatter_class=argparse.RawTextHelpFormatter,
        usage=argparse.SUPPRESS)
    parser.add_argument('-o', required=True, type=str,
                        help="Output folder path and name. E.g., './backup'")
    parser.add_argument('-d', required=False, type=str, default='|',
                        help="Delimiter to use for output CSV files. Default is pipe, '|', character.")
    parser.add_argument('-e', required=False, type=str, default='utf-8',
                        help="Encoding to use for CSV files. Default is 'utf-8'.")
    args = parser.parse_args()

    # 2. Make sure output folder exists; if not, create a folder there
    if not os.path.exists(args.o):
        print(f"Created output folder for CSV files: {args.o}")
        os.makedirs(args.o)

    # 3. Create database connection
    driver_name = "{SQL Server}"
    conn = pyodbc.connect(f"Driver={driver_name};Server={server};"
                          f"Database={database};UID={username};PWD={password};")
    cursor = conn.cursor()

    for table_name in tables_to_download:
        sql_query = "SELECT * FROM " + table_name

        cursor.execute(sql_query)

        headers = [[header[0] for header in cursor.description]]
        data = headers + [list(row) for row in cursor.fetchall()]

        # Write data to files
        file_path_and_name = f"{args.o}/{table_name}.csv"
        file_handle = open(file_path_and_name,
                           'w+',
                           newline='',
                           encoding=args.e)
        with file_handle:
            write = csv.writer(file_handle, delimiter=args.d)
            write.writerows(data)
            print("\n--> Downloaded data from: " + table_name)
            print("and wrote it to: " + file_path_and_name)

    cursor.close()
    conn.close()
