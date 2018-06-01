# TODO: implement a clearer version here

import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

from itertools import takewhile

HIERARCHY = ['Year', 'Region', 'Country', 'Advertiser', 'Brand']

def get_level(row):
    level = []
    for h in HIERARCHY:
        if row[h] is not None:
            level.append(h)
    if level:
        return level[-1]
    else:
        return 'ALL'

def get_node(ld, path):
    temp = ld.copy()
    for k in path:
        if isinstance(temp, list):
            try:
                temp = [d for d in temp if k in d][0]
            except IndexError:
                print('index error')
                return
        try:
            temp = temp[k]
        except KeyError:
            print('key error')
            return # an empty list?
    return temp

def build_node(row, row_level, hierarchy):
    # print('row:', str(row), '\tlevel:', level)
    n = {
        'name': str(row[row_level]),
        'level': row_level,
        'value': row['Value'],
    }
    if hierarchy[-1] != row_level:
        n.setdefault('children',[])
    return n

def main():
    rows = [
        {'Year': None,'Region': None,'Country': None,'Advertiser':None,'Brand':None,'Value': 25},
        {'Year': 2013, 'Region': None, 'Country': None, 'Advertiser':None, 'Brand':None, 'Value': 25},
        {'Year': 2013, 'Region': 'LTM', 'Country': None, 'Advertiser':None, 'Brand':None, 'Value': 25}, # Colombia and Chile combined
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser':None, 'Brand':None, 'Value': 10}, # M1, M2 and M3 combined
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M1', 'Brand': None, 'Value': 1},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M1', 'Brand': 'B1', 'Value': 1},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M2', 'Brand': None, 'Value': 5},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M2', 'Brand': 'B2', 'Value': 2},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M2', 'Brand': 'B3', 'Value': 3},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M3', 'Brand': None, 'Value': 4},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M3', 'Brand': 'B4', 'Value': 4},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser':None, 'Brand':None, 'Value': 15}, # M1, M2 and M4 combined
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M1', 'Brand': None, 'Value': 6},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M1', 'Brand': 'B1', 'Value': 1},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M1', 'Brand': 'B5', 'Value': 5},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M2', 'Brand': None, 'Value': 3},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M2', 'Brand': 'B3', 'Value': 3},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M4', 'Brand': None, 'Value': 6},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M4', 'Brand': 'B6', 'Value': 6},
    ]

    hierarchy = ['Year', 'Advertiser', 'Brand']
    collecion = []
    for r in rows:
        row_level = get_level(r)
        if row_level not in hierarchy: # row_level not in hierarchy, then skip this row
            continue
        else:
            path = list(takewhile(lambda x: x != row_level, (item for item in hierarchy))) + [row_level]
            print(r)
            print(row_level, '=>', path)
            cd = get_node(collecion, hierarchy)
            if cd is None: # create a node for this level and add to colleccion
                nd = build_node(r, row_level, hierarchy)

                print(nd)

            pdb.set_trace()
            print('h')

        # TODO: ignore all None row or handle it specially


    # pdb.set_trace()
    print('hah')

if __name__ == '__main__':
    main()

    # hierarchy = ['Year', 'Region', 'Country', 'Advertiser', 'Brand']
    #
    # hierarchy = ['Year', 'Region', 'Country', 'Advertiser'] # brand removed
    #
    # hierarchy = ['Year', 'Region', 'Country', 'Brand'] # manufacturer removed
    # hierarchy = ['Year', 'Region', 'Country']
    #
    # hierarchy = ['Year', 'Region', 'Advertiser', 'Brand'] # country removed
    # hierarchy = ['Year', 'Region', 'Advertiser']
    # hierarchy = ['Year', 'Region', 'Brand']
    #
    # hierarchy = ['Year', 'Country', 'Advertiser', 'Brand'] # region removed
    # hierarchy = ['Year', 'Country', 'Advertiser']
    # hierarchy = ['Year', 'Country', 'Brand']
#     rows = [
#         {'Year':None,'Region':None,'Country':None,'Advertiser':None,'Brand':None,'Value':1},
# k   Y   x{'Year':2013, 'Region':None, 'Country':None, 'Advertiser':None, 'Brand':None, 'Value':2},
#         {'Year':2013, 'Region':'LTM', 'Country':None, 'Advertiser':None, 'Brand':None, 'Value':3},
# k   Y,C x{'Year':2013, 'Region':'LTM', 'Country':'Colombia', 'Advertiser':None, 'Brand':None, 'Value':4},
# k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M1', 'Brand': None, 'Value': 5},
#         {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M1', 'Brand': 'B1', 'Value': 6},
# k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M2', 'Brand': None, 'Value': 7},
#         {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M2', 'Brand': 'B2', 'Value': 8},
#         {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M2', 'Brand': 'B3', 'Value': 9},
# k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M3', 'Brand': None, 'Value': 10},
#         {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M3', 'Brand': 'B4', 'Value': 11},
# k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M4', 'Brand': None, 'Value': 12},
#         {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M4', 'Brand': 'B5', 'Value': 13},
# k   Y   x{'Year': 2014, 'Region': None, 'Country': None, 'Advertiser': None, 'Brand': None, 'Value': 14},
#         {'Year': 2014, 'Region': 'LTM', 'Country': None, 'Advertiser': None, 'Brand': None, 'Value': 15},
# k   Y,C x{'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': None, 'Brand': None, 'Value': 16},
# k   Y,C,M x{'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M1', 'Brand': None, 'Value': 17},
#         {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': 'M1', 'Brand': None, 'Value': 18},
#         {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Advertiser': None, 'Brand': None, 'Value': 19},
#         {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M1', 'Brand': 'B1', 'Value': 20},
#         {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Advertiser': 'M1', 'Brand': 'B6', 'Value': 21},
#     ]
