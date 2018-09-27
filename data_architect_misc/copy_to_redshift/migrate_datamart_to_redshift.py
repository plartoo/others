'''
Author: Hamza Ahmad
Desc:
'''

import os
import time
import multiprocessing
from .Connections import SQLConnection, RedshiftConnection
from .account_info import local_temp_folder, cred_sql, cred_rs
from FileUtilities import s2hms


def migrate(table_info):
    t = time.time()
    [_, table, row_count] = table_info

    # Export SQL table from Datamart into a tab-delimited text file in a temporary folder
    output_file = '{}.txt'.format(table.replace(' ', '_'))
    output_path = os.path.join(local_temp_folder, output_file)
    sql = SQLConnection(**cred_sql)
    sql.export_table(table=table, output_file=output_path, delimiter='\t')

    # Upload local file to S3 and COPY into Redshift
    rs = RedshiftConnection(**cred_rs)
    rs.file_to_redshift(file_path=output_path, table=table, replace_table=True, delimiter='\t')

    # Get row count of Redshift table
    cur = rs.exec_commit(query='select count(*) from {}'.format(table), commit=False, return_cursor=True)
    rs_row_count = cur.fetchone()[0]
    rs.close()

    if row_count == rs_row_count:
        os.remove(output_path)
        print('Transferred {:,} rows into [{}] in {}.'.format(row_count, table, s2hms(t)))
    else:
        print('\n\nERROR TRANSFERRING DATAMART TABLE: [{}]. #RowsInDataMart: {:,}\t#RowsInRedshift: {:,}'
              .format(table, row_count, rs_row_count))


if __name__ == '__main__':
    # Get a list of SQL tables that need to be migrated to Redshift
    sql = SQLConnection(**cred_sql)
    tables_to_transfer = sql.query("""SELECT DISTINCT [Schema] = s.[Name],
                                                      [Table] = t.[Name],
                                                      [RowCount] = p.[Rows]
                                      FROM sys.tables t
                                      INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
                                      INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                                      INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID
                                                                 AND i.index_id = p.index_id
                                      -- WHERE s.[Name] = 'dbo'
                                      ORDER BY p.[Rows]""")
    p = multiprocessing.Pool()
    p.map(migrate, tables_to_transfer.values.tolist())
    p.close()
