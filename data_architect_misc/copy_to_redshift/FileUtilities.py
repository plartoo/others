'''
Author: Hamza Ahmad
Desc:
'''

import pandas as pd
from pandas.api.types import infer_dtype
import filecmp


def get_headers(file_path, delimiter=','):
    data = pd.read_csv(file_path, sep=delimiter, nrows=0, low_memory=False)
    return data.columns.tolist()


def get_redshift_dtype(values):
    dtype = infer_dtype(values)
    if dtype in ['int64', 'integer']:
        return 'bigint'
    elif dtype in ['float64', 'floating', 'mixed-integer-float', 'decimal']:
        return 'float'
    elif dtype in ['datetime64', 'datetime', 'date']:
        return 'date'
    elif dtype in ['boolean']:
        return 'boolean'
    elif dtype in ['object', 'string', 'mixed-integer', 'mixed']:
        return 'varchar(4000)'
    else:
        return 'varchar(4000)'


def get_columns_and_redshift_dtypes(file_path, delimiter=','):
    columns = get_headers(file_path=file_path, delimiter=delimiter)
    dtypes = []
    for column in columns:
        values = pd.DataFrame()
        reader = pd.read_csv(file_path, sep=delimiter, chunksize=10000, usecols=[column], infer_datetime_format=True, low_memory=False)
        for chunk in reader:
            chunk.dropna(axis=0, inplace=True)
            values = pd.concat([values, chunk], ignore_index=True)
            values.drop_duplicates(inplace=True)
        dtypes.extend([get_redshift_dtype(values[column])])
    return columns, dtypes


def compare_files(file1, file2, compare_bytes=False):
    if compare_bytes:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            if f1.read() == f2.read():
                return True
            else:
                return False
    else:
        return filecmp.cmp(file1, file2, shallow=False)

from time import time

def s2hms(t):
    sec = int(round(time() - t, 0))
    hrs, mins, sec = sec // 3600, (sec % 3600) // 60, (sec % 3600) % 60
    if hrs > 0:
        return str('{:01}:{:02}:{:02}'.format(hrs, mins, sec) + ' hrs')
    elif mins > 0:
        return str('{:01}:{:02}'.format(mins, sec) + ' mins')
    else:
        return str('{:01}'.format(sec) + ' secs')
