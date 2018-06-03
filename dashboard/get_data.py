import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

from collections import defaultdict

from flask import Flask, request
from flask_cors import CORS

import pandas as pd
import pyodbc

import account_info
import queries

ROOT_LEVEL = 'ROOT'
ROOT_NAME = 'ALL'
ANCHOR = 'Year'
METRICS = ['SumOfSpend','UniqBrandCount','UniqRegionCount','UniqCountryCount','UniqAdvertiserCount']

def build_data_block(row, level, hierarchy, metrics=METRICS, label=None):
    name = ROOT_NAME if level==ROOT_LEVEL else row[level]
    d = {
        'name': name,
        'level': level,
        'value': [row[m] for m in metrics],
    }
    # leaves of the tree do NOT have children TODO: test if ECharts allow empty list for leaves; if so, remove this code
    if hierarchy[-1] != level:
        d.setdefault('children',[])
    if label is not None:
        d.setdefault('label', label)
    return d
#
# def build_data_tree_by_year(dataframe, hierarchy):
#     assert ANCHOR in dataframe.columns, \
#         "'build_data_tree_by_year' expects the input dataframe to have '" + ANCHOR + "' column"
#     assert ANCHOR == hierarchy[0], \
#         "'build_data_tree_by_year' expects the first item in hierarchy as '" + ANCHOR + "'"
#     assert len(hierarchy) > 1, "hierarchy list should have at least two items"
#
#     # ['ALL','1 nonempty','2 nonempty','3 nonempty',...] #=> '1 nonempty' is where all data that have regional aggregate goes to etc.
#     #
#     # ['ALL','2013','2014','2015','2016']
#
#     temp = {} # {ROOT:[]}
#     i = 0
#     for index, row in dataframe.iterrows():
#         i += 1
#         # cur_row = [row[h] for h in hierarchy]
#         # nonempty_field_cnt = sum(x is not None for x in cur_row)
#         path = ['ROOT']+[l for l in [row[h] for h in hierarchy] if l is not None]
#         # ['ROOT','Year','Region']
#         # Given a path, walk down the dict and if no such node exists, create one
#         level = ROOT if len(path) == 0 else hierarchy[len(path)-1]
#         block = build_data_block(row, level)
#         if level == ROOT: # this is for Worldwide/global statistics
#             temp[ROOT] = block
#             # temp[ROOT].append(block)
#         elif level == ANCHOR:
#             yr = row[ANCHOR]
#             temp.setdefault(yr, [])
#             temp[yr].append(block)
#             pdb.set_trace()
#             print('ha')
#         else:
#             for h in ([ROOT] + hierarchy[:(nonempty_field_cnt-1)]):
#
#
#         print(r, ':', none_count)
#         if i > 14:
#             break

def run_sql(sql):
    conn = pyodbc.connect(account_info.DM_1219)
    # build_data_tree_by_year(pd.read_sql(sql, conn), ['Year', 'Region', 'Country', 'Advertiser', 'Brand'])
    # 'Year': ['Region', 'Country', 'Advertiser', 'Brand']
    # 'Year': ['Country', 'Advertiser', 'Brand']
    # -- if '' then replace with < hierarchy_name > +': ALL'
    # pdb.set_trace()

    # old school approach to return data
    # cursor = conn.cursor()
    # cursor.execute(sql)
    # return cursor.fetchall()
    return pd.read_sql(sql, conn)

QUERIES = {
    'full_data': queries.hierarchy_table,
    'spend_and_brand': queries.investment_and_brand,
}

app = Flask(__name__)
CORS(app) # REF: https://stackoverflow.com/a/32749344/1330974
@app.route('/get_data')
def get_data():
    # REF: https://stackoverflow.com/q/11774265/1330974
    # user = request.args.get('user') # how to get url query ?user=something
    # to get the whole query string, do: request.query_string
    qtype = request.args.get('qtype')
    df = run_sql(QUERIES[qtype])
    data = df.to_json(orient='records') # or use jsonify REF: https://stackoverflow.com/q/13081532/1330974
    # pdb.set_trace()
    return data

if __name__ == '__main__':
    app.debug = True
    app.run()
    # get_data()
