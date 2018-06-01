import json
# # archived as of 6/1/2018 3AM
# def get_node(ld, path):
#     temp = ld.copy()
#     for k in path:
#         if isinstance(temp, list):
#             try:
#                 temp = [d for d in temp if k in d][0]
#             except IndexError:
#                 print('index error')
#                 return
#         try:
#             temp = temp[k]
#         except KeyError:
#             print('key error')
#             return # an empty list?
#     return temp

def walk_dict(ld, path):
    temp = ld.copy()
    for k in path:
        if isinstance(temp, list):
            try:
                temp = [d for d in temp if k in d][0]
            except IndexError:
                return
        try:
            temp = temp[k]
        except KeyError:
            return
    return temp

def retrieve(dict, path, key='children'):
    for k in path:
        if isinstance(temp, list):
            try:
                temp = [d for d in temp if k in d][0]
            except IndexError:
                return
        try:
            temp = temp[k]
        except KeyError:
            return
    return temp
import pdb
#TODO: we need a function to build a path like this: [('Year', '2014'), ('Advertiser','A5'), ('Brand', 'B5')]
def get_node(ld, path):
    temp = ld.copy()
    try:
        temp = [d for d in temp if (path[0][1] == d[path[0][0]])][0]
    except IndexError:
        # means that there is no hash with equivalent value yet in this bucket; need to add a new node to this bucket, and keep adding more
        print('index error')
        return ld
    try:
        # if we get here, we found an existing hash in the bucket, so we need to keep going down if more path trail remains
        if len(path) > 1: # here, path should not include the last level in hierarchy; we don't go that far
            get_node(temp['children'], path[1:])
        else:
            # this means we reached the leaf level
            return temp # return the hash; in that case, we don't need to add a new node, possibly update the value?
    except KeyError:
        # means this is the leaf (the last hierarchy), we should never get here...
        print('key error')
        return  # an empty list?

# say, I want to add ('Brand', 'B5'), we go up to 'Advertiser' level and get its children list/bucket
[('Year', '2014'), ('Advertiser','A5'), ('Brand', 'B5')]
# to add A6 and B7, we need to go to 'Year' level, get its bucket, not found
[('Year', '2014'), ('Advertiser','A6'), ('Brand', 'B7')]

def main():
    d = [
        {
            'Year': '2013',
            'level': 'Year',
            'children': [
                {
                    'Advertiser': 'A1',
                    'level': 'Advertiser',
                    'children': [
                        {
                            'Brand': 'B1',
                            'level': 'Brand',
                            'children': []
                        },
                    ]
                },
                {
                    'Advertiser': 'A2',
                    'level': 'Advertiser',
                    'children': [
                        {
                            'Brand': 'B2',
                            'level': 'Brand',
                            'children': []
                        },
                    ]
                }
            ],
        },
        {
            'Year': '2014',
            'level': 'Year',
            'children': [
                {
                    'Advertiser': 'A4',
                    'level': 'Advertiser',
                    'children': [
                        {
                            'Brand': 'B4',
                            'level': 'Brand',
                            'children': []
                        },
                    ]
                },
                {
                    'Advertiser': 'A5',
                    'level': 'Advertiser',
                    'children': [
                        {
                            'Brand': 'B5',
                            'level': 'Brand',
                            'children': []
                        },
                        {
                            'Brand': 'B6',
                            'level': 'Brand',
                            'children': []
                        },
                    ]
                }
            ],
        }
    ]
    p = [('Year', '2014'), ('Advertiser','A5'), ('Brand', 'B5')]
    print(json.dumps(get_node(d,p), indent=4))
    # # archived as of 6/1/2018 3AM
    # def get_node(ld, path):
    #     temp = ld.copy()
    #     for k in path:
    #         if isinstance(temp, list):
    #             try:
    #                 temp = [d for d in temp if k in d][0]
    #             except IndexError:
    #                 print('index error')
    #                 return
    #         try:
    #             temp = temp[k]
    #         except KeyError:
    #             print('key error')
    #             return # an empty list?
    #     return temp

    # below works
    # d = {'A': [{'B': [{'C': [{'D1':['values of D1']}, {'D2': "I'm D2"}]}]}]}
    # a = ['A', 'B', 'C', 'D1']
    # ele = walk_dict(d,a)
    #
    # print(walk_dict(d, a))
    # a = ['A', 'B', 'C', 'D2']
    # print(walk_dict(d, a))
    # a = ['A', 'B', 'C', 'D3']
    # print(walk_dict(d, a))
    # a = ['A', 'B1', 'C', 'D3']
    # print(walk_dict(d, a))

if __name__ == '__main__':
    main()

#
# def add_node(nd, path):
#     # write add node function here
#     pass
#
# def build_node(row, row_level, hierarchy):
#     # print('row:', str(row), '\tlevel:', level)
#     n = {
#         'name': str(row[row_level]),
#         'level': row_level,
#         'value': row['Value'],
#     }
#     if hierarchy[-1] != row_level:
#         n.setdefault('children',[])
#     return n









