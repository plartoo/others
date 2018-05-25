import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

from collections import defaultdict

from flask import Flask, jsonify, request
import pandas as pd
import pyodbc

import account_info
import queries

ROOT = 'ALL'
ANCHOR = 'Year'
METRICS = ['SumOfSpend','UniqBrandCount','UniqRegionCount','UniqCountryCount','UniqAdvertiserCount']

def build_data_block(row, level, label=None):
    # print(row)
    # pdb.set_trace()
    # print(row)
    # print(level)
    name = ROOT if level == ROOT else row[level]
    return {
        'name': name,
        'value': [row[m] for m in METRICS],
        'label': label
    }

def build_data_tree_by_year(dataframe, hierarchy):
    assert ANCHOR in dataframe.columns, \
        "'build_data_tree_by_year' expects the input dataframe to have '" + ANCHOR + "' column"
    assert len(hierarchy) > 1, "hierarchy list should have at least two items"

    # ['ALL','1 nonempty','2 nonempty','3 nonempty',...] #=> '1 nonempty' is where all data that have regional aggregate goes to etc.
    #
    # ['ALL','2013','2014','2015','2016']

    hierarchy = [ROOT] + hierarchy
    # dataframe[[ANCHOR]] = dataframe[[ANCHOR]].fillna(value=0)#.astype(int).astype(str)
    years = [x if x else ROOT for x in dataframe.Year.unique()]
    tree = {y: [] for y in years}
    temp = {y: {h: [] for h in hierarchy} for y in years}
    i = 0
    for index, row in dataframe.iterrows():
        i += 1
        for prev,cur in zip(hierarchy, hierarchy[1:]):
            print(prev,cur)
            if row[cur] is not None:
                continue
            else:
                k = ROOT if row[ANCHOR] is None else row[ANCHOR]
                temp[k][prev].append(build_data_block(row, prev))
                break

        if i == 13:
            pp.pprint(temp['2013'])
            pdb.set_trace()
            print('halo')

    pdb.set_trace()
    print('ha')



def run_sql(sql):
    conn = pyodbc.connect(account_info.DM_1219)
    build_data_tree_by_year(pd.read_sql(sql, conn), ['Year', 'Region', 'Country', 'Advertiser', 'Brand'])
    # 'Year': ['Region', 'Country', 'Advertiser', 'Brand']
    # 'Year': ['Country', 'Advertiser', 'Brand']
    # -- if '' then replace with < hierarchy_name > +': ALL'
    # pdb.set_trace()
    print('hello')

app = Flask(__name__)
@app.route('/get_data')
def get_data():
    # REF: https://stackoverflow.com/q/11774265/1330974
    # user = request.args.get('user') # how to get url query ?user=something
    # to get the whole query string, do: request.query_string

    run_sql(queries.hierarchy_table)
    # return json:: jsonify(d) REF: https://stackoverflow.com/q/13081532/1330974
    return "Hello World"

if __name__ == '__main__':
    # app.debug = True
    # app.run()
    get_data()