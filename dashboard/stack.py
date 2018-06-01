import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb
import json
import itertools

def __lt__(_rows, key, current):
    new_rows = list(filter(None, [i[current] for i in _rows]))
    return {'int':0, 'str':''}.get(type(new_rows[0]).__name__) if key is None else key


rows = [
    {'Year': None, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 25},
    # row 1 => SUM of (row 2 and row 14) = 15+25 = 40; this row represents, for example, all of the sales made so far (the ultimate total, if you will call it as such)
    {'Year': 2013, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15},
    # row 2 => SUM of values from (row 3) = 15; this row represents, for example, the total of sales in 2013 from all regions, all countries, all manufacturers and all brands
    {'Year': 2013, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15},
    # row 3 => SUM of values from (row 4) = 15; this row represents, for example, the total of sales in LTM region for 2013
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 15},
    # row 4 => SUM of values from (row 5+row 7+row 10+row12) = 1+5+4+5 = 15; this row represents, for example, the total of Sales in Colombia for 2013
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 1},
    # row 5 => SUM of value sfrom (row 6) = 1
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 1},
    # row 6 => Nothing to sum here because this is the lowest hierarchy
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': None, 'Value': 5},
    # row 7 => SUM of value sfrom (row 8 and row 9) = 2+3 = 5
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B2', 'Value': 2},
    # row 8 => Nothing to sum here
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B3', 'Value': 3},
    # row 9 => Nothing to sum here
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': None, 'Value': 4},
    # row 10 => SUM of values from (row 11) = 4
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': 'B4', 'Value': 4},
    # row 11 => Nothing to sum here
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': None, 'Value': 5},
    # row 12 => SUM of values from (row 13) = 5
    {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': 'B5', 'Value': 5},
    # row 13 => Nothing to sum here

    {'Year': 2014, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 25},
    # row 14 => SUM of values from (row 15) = 25; represents total sales in 2014 from all regions, all countries, all manufacturers and all brands
    {'Year': 2014, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 25},
    # row 15 => SUM of values from (row 16+row 18) = 15+10 = 25; represents total sales in 2014 from Chile and Colombia combined
    {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': None, 'Brand': None, 'Value': 15},
    # ** TRICKY: row 16 => SUM of values from (row 17+row 20+row 21) =  0+5+10 = 15; total sales in 2014 for Chile
    {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': None, 'Value': 15},  # row 17
    {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 10},
    # row 18 => SUM of values from (row 19) = 10; total sales in 2014 for Colombia
    {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 10},  # row 19
    {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 5},  # row 20
    {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B6', 'Value': 10},  # row 21

]

def build_tree(d, hierarchy=['Year', 'Region', 'Country', 'Brand']):
    start, *_h = hierarchy
    first = [
        [a, list(b)] for a, b in itertools.groupby(sorted(d, key=lambda x:__lt__(rows, x[start], start)),
                                                   key=lambda x:__lt__(rows, x[start], start))
        ]
    return [{'name':a,
             'value':min(b, key=lambda x:x['Value'])['Value'],
             'children':[] if not _h else build_tree(b, _h)} for a, b in first if a]

# c = 0
# def build_tree(rows, hierarchy):
#     from collections import defaultdict
#     # This code is only partially working; it fails to take into account the Values...
#     global c
#     if not hierarchy:
#         print(c)
#         return []
#     h0, *hierarchy = hierarchy
#     node = defaultdict(list)
#     for row in rows:
#         v0 = row[h0]
#         if v0 is not None:  # filter out null values??
#             c += 1
#             print(v0)
#             node[v0].append(row)#(row,row['Value']))
#             pp.pprint(node)
#     return [{
#         'name': key,
#         'value': sum([r['Value'] for r in subrows]),#None, # what is value??
#         'children': build_tree(subrows, hierarchy)} for key, subrows in node.items()]

def main():
    tree = []
    nodes = []
    # hierarchy = ['Year', 'Region']
    hierarchy = ['Year', 'Region', 'Country']
    # hierarchy = ['Year', 'Region', 'Country', 'Brand']

    rows = [
        {'Year': None, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 25}, # row 1 => SUM of (row 2 and row 14) = 15+25 = 40; this row represents, for example, all of the sales made so far (the ultimate total, if you will call it as such)
        {'Year': 2013, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15}, # row 2 => SUM of values from (row 3) = 15; this row represents, for example, the total of sales in 2013 from all regions, all countries, all manufacturers and all brands
        {'Year': 2013, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15}, #row 3 => SUM of values from (row 4) = 15; this row represents, for example, the total of sales in LTM region for 2013
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 15}, # row 4 => SUM of values from (row 5+row 7+row 10+row12) = 1+5+4+5 = 15; this row represents, for example, the total of Sales in Colombia for 2013
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 1}, # row 5 => SUM of value sfrom (row 6) = 1
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 1}, # row 6 => Nothing to sum here because this is the lowest hierarchy
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': None, 'Value': 5}, # row 7 => SUM of value sfrom (row 8 and row 9) = 2+3 = 5
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B2', 'Value': 2}, # row 8 => Nothing to sum here
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B3', 'Value': 3}, # row 9 => Nothing to sum here
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': None, 'Value': 4}, # row 10 => SUM of values from (row 11) = 4
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': 'B4', 'Value': 4}, # row 11 => Nothing to sum here
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': None, 'Value': 5}, # row 12 => SUM of values from (row 13) = 5
        {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': 'B5', 'Value': 5}, # row 13 => Nothing to sum here

        {'Year': 2014, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 25}, # row 14 => SUM of values from (row 15) = 25; represents total sales in 2014 from all regions, all countries, all manufacturers and all brands
        {'Year': 2014, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 25}, # row 15 => SUM of values from (row 16+row 18) = 15+10 = 25; represents total sales in 2014 from Chile and Colombia combined
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': None, 'Brand': None, 'Value': 15}, # ** TRICKY: row 16 => SUM of values from (row 17+row 20+row 21) =  0+5+10 = 15; total sales in 2014 for Chile
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': None, 'Value': 0}, # row 17
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 10}, # row 18 => SUM of values from (row 19) = 10; total sales in 2014 for Colombia
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 10}, # row 19
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 5}, # row 20
        {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B6', 'Value': 10}, # row 21

        # {'Year': None, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 1},
        # {'Year': 2013, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 2},
        # {'Year': 2013, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 3},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 4},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 5},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 6},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': None, 'Value': 7},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B2', 'Value': 8},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M2', 'Brand': 'B3', 'Value': 9},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': None, 'Value': 10},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M3', 'Brand': 'B4', 'Value': 11},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': None, 'Value': 12},
        # {'Year': 2013, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M4', 'Brand': 'B5', 'Value': 13},
        # {'Year': 2014, 'Region': None, 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 14},
        # {'Year': 2014, 'Region': 'LTM', 'Country': None, 'Manufacturer': None, 'Brand': None, 'Value': 15},
        # {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': None, 'Brand': None, 'Value': 16},
        # {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': None, 'Value': 17},
        # {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': 'M1', 'Brand': None, 'Value': 18},
        # {'Year': 2014, 'Region': 'LTM', 'Country': 'Colombia', 'Manufacturer': None, 'Brand': None, 'Value': 19},
        # {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B1', 'Value': 20},
        # {'Year': 2014, 'Region': 'LTM', 'Country': 'Chile', 'Manufacturer': 'M1', 'Brand': 'B6', 'Value': 21},
        # more data...
    ]
    t = build_tree(rows, hierarchy)
    # pdb.set_trace()
    pp.pprint(t)


if __name__ == '__main__':
    main()


