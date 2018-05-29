# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# import pdb
#
# def find_dict(ld, key):
#     # we can assume that 'ld' has dicts each of which has unique key
#     for d in ld:
#         # pp.pprint(d)
#         # print(key)
#         if key not in d:
#             continue
#         # else:
#         #     # print('returned from find_dict')
#         #     # pp.pprint(d)
#         return d
#
# def walk_dict(d,path): # this is iterative, a bit more naive approach
#     temp = None
#     # pp.pprint(d)
#     for i,n in enumerate(path):
#         if i == 0:
#             temp = d.get(n)
#             # print(i,n)
#             # pp.pprint(temp)
#         elif i < (len(path)-1):
#             temp = find_dict(temp, n)
#             temp = temp.get(n)
#             # print(i,n)
#             # pp.pprint(temp)
#         else: # last item
#             temp = find_dict(temp, n)
#             print('Found it!')
#             print(i,n)
#             print(temp.get(n))
#             return temp.get(n)
#

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

def main():
    d = {'A': [{'B': [{'C': [{'D1':['values of D1']}, {'D2': "I'm D2"}]}]}]}
    a = ['A', 'B', 'C', 'D1']
    print(walk_dict(d, a))
    a = ['A', 'B', 'C', 'D2']
    print(walk_dict(d, a))
    a = ['A', 'B', 'C', 'D3']
    print(walk_dict(d, a))
    a = ['A', 'B1', 'C', 'D3']
    print(walk_dict(d, a))

if __name__ == '__main__':
    main()
