import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb
from collections import defaultdict

def build_tree(rows, hierarchy):
    if not hierarchy:
        return []
    h0, *hierarchy = hierarchy
    node = defaultdict(list)
    for row in rows:
        v0 = row[h0]
        if v0 is not None:  # filter out null values??
            node[v0].append(row)
    return [{
        'name': key,
        'value': None, # what is value??
        'children': build_tree(subrows, hierarchy)} for key, subrows in node.items()]


def main():
    tree = []
    nodes = []
    # hierarchy = ['Year', 'Region']
    hierarchy = ['Year', 'Region', 'Country']
    # hierarchy = ['Year', 'Country', 'Manufacturer']

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
    t = build_tree(rows, hierarchy)
    # pdb.set_trace()
    pp.pprint(t)

if __name__ == '__main__':
    main()


# import itertools
# rows = [{'Year': None, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 1}, {'Year': 2013, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 2}, {'Year': 2013, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 3}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 4}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 5}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 6}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': None, 'Value': 7}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B2', 'Value': 8}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B3', 'Value': 9}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': None, 'Value': 10}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': 'B4', 'Value': 11}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': None, 'Value': 12}, {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': 'B5', 'Value': 13}, {'Year': 2014, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 14}, {'Year': 2014, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15}, {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': None, 'Brand': None, 'Value': 16}, {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': None, 'Value': 17}, {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 18}, {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 19}, {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 20}, {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B6', 'Value': 21}]
# def __lt__(_rows, key, current):
#   new_rows = list(filter(None, [i[current] for i in _rows]))
#   return {'int':0, 'str':''}.get(type(new_rows[0]).__name__) if key is None else key
#
# def group_data(d, hierarchy=['Year','Country','Manufacturer']):
#   start, *_h = hierarchy
#   first = [[a, list(b)] for a, b in itertools.groupby(sorted(d, key=lambda x:__lt__(rows, x[start], start)), key=lambda x:__lt__(rows, x[start], start))]
#   return [{'name':a, 'value':min(b, key=lambda x:x['Value'])['Value'], 'children':[] if not _h else group_data(b, _h)} for a, b in first if a]