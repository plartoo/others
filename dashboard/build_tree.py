import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

def build_node(row, level, hierarchy):
    n = {
        'name': 'ALL' if level=='ROOT' else row[level],
        'level': level,
        'value': row['Metric'],
    }
    if hierarchy[-1] != level:
        n.setdefault('children',[])
    return n


def add_node_to_tree(tree, levels, row): # path=['ROOT','Year','Region']
    if len(levels) == 1:  # last level => leaves
        return build_node(row, levels[0], levels)
    else:
        for level in levels:
            if not tree: # empty list
                tree.append(build_node(row, level, levels))
                # print(levels)
                add_node_to_tree(tree[0]['children'], levels[1:], row)
            else:
                # search for relevant node and call add_node_to_tree on its children
                if level == 'ROOT':
                    pdb.set_trace()
                    print('ha')
                node = [n for n in tree if (n['level']==level) and (n['name']==row[level])]
                print(levels)
                if not node:
                    add_node_to_tree(node, levels[1:], row)
                else:
                    add_node_to_tree(node[0]['children'], levels[1:], row)

def main():
    tree = []
    levels = ['ROOT', 'Year', 'Region']
    row = [
        {'Year':None,'Region':None,'Country':None,'Advertiser':None,'Brand':None,'Metric':1},
        {'Year':2013, 'Region':None, 'Country':None, 'Advertiser':None, 'Brand':None, 'Metric':2},
        {'Year':2013, 'Region':'Latin', 'Country':None, 'Advertiser':None, 'Brand':None, 'Metric':3},
        {'Year':2013, 'Region':'Latin', 'Country':'Colombia', 'Advertiser':None, 'Brand':None, 'Metric':4},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'AZUL', 'Brand': None, 'Metric': 5},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'AZUL', 'Brand': 'Carey', 'Metric': 6},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'BEIERSDORF', 'Brand': None, 'Metric': 7},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'BEIERSDORF', 'Brand': 'Eucerin', 'Metric': 8},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'BEIERSDORF', 'Brand': 'Nivea', 'Metric': 9},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'BEISBOL', 'Brand': None, 'Metric': 10},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'BEISBOL', 'Brand': 'Beisbol', 'Metric': 11},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'BELLEZA EXPRESS SA', 'Brand': None, 'Metric': 12},
        {'Year': 2013, 'Region': 'Latin', 'Country': 'Colombia', 'Advertiser': 'BELLEZA EXPRESS SA', 'Brand': 'Aromasense', 'Metric': 13},
    ]
    for r in row:
        add_node_to_tree(tree, levels, r)

    pp.pprint(tree)

if __name__ == '__main__':
    main()
