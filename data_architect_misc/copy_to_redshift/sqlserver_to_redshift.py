'''
Author: Hamza Ahmad
Desc:
'''

import os
from time import time
import multiprocessing
from .Connections import SQLConnection, RedshiftConnection
from .account_info import cred_sql, cred_rs, local_temp_folder
from FileUtilities import s2hms


def main(input_val):
    rs_table_name = input_val[0]
    ss_table_name = input_val[1]
    t = time()
    file_name = f'{rs_table_name}.txt'
    file_path = os.path.join(local_temp_folder, file_name)
    delimiter = '\t'

    sql = SQLConnection(**cred_sql)
    sql.export_table(table=ss_table_name, output_file=file_path, delimiter=delimiter)

    rs = RedshiftConnection(**cred_rs)
    rs.file_to_redshift(file_path=file_path, table=rs_table_name, replace_table=True, delimiter=delimiter)

    os.remove(file_path)

    print(f'COMPLETED PUSHING {rs_table_name} TO REDSHIFT IN {s2hms(t)}.')
    return


if __name__ == '__main__':

    tasks = [
             ('ds027_externalfactors_holidays',
              '[DFID033618_Holiday until 2018_Transformed]'),
            ]

    p = multiprocessing.Pool()  # Use Pool(N) for N simultaneous threads
    p.map(main, tasks)
    p.close()
