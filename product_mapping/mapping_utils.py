import re

import pandas as pd
import pyodbc

import account_info


def run_sql(sql):
    conn = pyodbc.connect(account_info.DM_1219)
    return pd.read_sql(sql, conn)


def get_dataframe_from_query(query):
    return run_sql(query)


def tokenize(s):
    # 1. replace commas and forward slashes with spaces
    # (this step must come first before step 2 below) for cases like 'ROLDA,GEL,(INT)'
    # 2. removes non-alphanumeric and double-or-more space characters;
    # and turn the str into lowercase
    # Note: alternatively, we can do simple thing like this r'\w+' instead
    return re.sub('[^0-9a-zA-Z\s]+', '', re.sub('[,//]+', ' ', s)).lower().split()
