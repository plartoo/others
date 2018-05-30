# TODO: implement a clearer version here

import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

def build_node(row, level, hierarchy):
    # print('row:', str(row), '\tlevel:', level)
    n = {
        'name': 'ALL' if level=='ROOT' else row[level],
        'level': level,
        'value': row['Value'],
    }
    if hierarchy[-1] != level:
        n.setdefault('children',[])
    return n

def main():
    tree = []
    nodes = []
    # hierarchy = ['Year', 'Region']
    hierarchy = ['Year', 'Region', 'Country']
    hierarchy = ['Year', 'Country', 'Manufacturer']

    rows = [
        {'Year':None,'Region':None,'Country':None,'Manufacturer':None,'Brand':None,'Value':1},
        {'Year':2013, 'Region':None, 'Country':None, 'Manufacturer':None, 'Brand':None, 'Value':2},
        {'Year':2013, 'Region':'LTM', 'Country':None, 'Manufacturer':None, 'Brand':None, 'Value':3},
        {'Year':2013, 'Region':'LTM', 'Country':'Colombia', 'Manufacturer':None, 'Brand':None, 'Value':4},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 5},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 6},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': None, 'Value': 7},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B2', 'Value': 8},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B3', 'Value': 9},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': None, 'Value': 10},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': 'B4', 'Value': 11},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': None, 'Value': 12},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': 'B5', 'Value': 13},
        ...
    ]

    rows = [
        {'Year':None,'Region':None,'Country':None,'Manufacturer':None,'Brand':None,'Value':1},
k   Y   x{'Year':2013, 'Region':None, 'Country':None, 'Manufacturer':None, 'Brand':None, 'Value':2},
        {'Year':2013, 'Region':'LTM', 'Country':None, 'Manufacturer':None, 'Brand':None, 'Value':3},
k   Y,C x{'Year':2013, 'Region':'LTM', 'Country':'Colombia', 'Manufacturer':None, 'Brand':None, 'Value':4},
k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 5},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 6},
k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': None, 'Value': 7},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B2', 'Value': 8},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B3', 'Value': 9},
k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': None, 'Value': 10},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': 'B4', 'Value': 11},
k   Y,C,M x{'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': None, 'Value': 12},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': 'B5', 'Value': 13},
k   Y   x{'Year': 2014, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 14},
        {'Year': 2014, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15},
k   Y,C x{'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': None, 'Brand': None, 'Value': 16},
k   Y,C,M x{'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': None, 'Value': 17},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 18},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 19},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 20},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B6', 'Value': 21},

        # more data...
    ]

    rows = [
        {'Year': None, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 1},
        {'Year': 2013, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 2},
        {'Year': 2013, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 3},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 4},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 5},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 6},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': None, 'Value': 7},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B2', 'Value': 8},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B3', 'Value': 9},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': None, 'Value': 10},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': 'B4', 'Value': 11},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': None, 'Value': 12},
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': 'B5', 'Value': 13},
        {'Year': 2014, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 14},
        {'Year': 2014, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': None, 'Brand': None, 'Value': 16},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': None, 'Value': 17},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 18},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 19},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 20},
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B6', 'Value': 21},
        # more data...
    ]
    for row in rows:
        if
    # for row in rows:
    #     row_levels = [k for k, v in row.items() if v is not None]
    #     print(row_levels)
    #     if set(hierarchy) == set(row_levels):
    #         pdb.set_trace()
    #         nodes.append(build_node(row, hierarchy[-1], hierarchy))

        # row_content = [i for i in [row[l] for l in hierarchy] if i is not None]
        # row_levels = [l for l in hierarchy if row[l] is not None]
        # row_level = 'ROOT' if not row_levels else row_levels[-1]
        # if len(row_levels) ==

    pp.pprint(nodes)
    pdb.set_trace()
    pp.pprint(tree)

if __name__ == '__main__':
    main()
