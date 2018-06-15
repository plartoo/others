import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

import pandas as pd
import pyodbc

import account_info
import queries


def run_sql(sql):
    conn = pyodbc.connect(account_info.DM_1219)
    return pd.read_sql(sql, conn)

QUERIES = {
    'all_mappings': queries.all_mappings,
}

def get_data(query_name):
    df = run_sql(QUERIES[query_name])
    data = df.to_json(orient='records') # or use jsonify REF: https://stackoverflow.com/q/13081532/1330974
    pdb.set_trace()
    return data

if __name__ == '__main__':
    get_data('all_mappings')
