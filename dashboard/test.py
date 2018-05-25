import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

def find_dict(ld, key):
    # we can assume that 'ld' has dicts each of which has unique key
    for d in ld:
        # pp.pprint(d)
        # print(key)
        if key not in d:
            continue
        # else:
        #     # print('returned from find_dict')
        #     # pp.pprint(d)
        return d

def walk_dict(d,path):
    temp = None
    # pp.pprint(d)
    for i,n in enumerate(path):
        if i == 0:
            temp = d.get(n)
            # print(i,n)
            # pp.pprint(temp)
        elif i < (len(path)-1):
            temp = find_dict(temp, n)
            temp = temp.get(n)
            # print(i,n)
            # pp.pprint(temp)
        else: # last item
            temp = find_dict(temp, n)
            print('Found it!')
            print(i,n)
            print(temp.get(n))
            return temp.get(n)

d = {'A': [{'B': [{'C': [{'D1':[]}, {'D2': []}]}]}]}
l = ['A','B','C','D1'] # here, I'd like to retrieve the value of 'D1'
walk_dict(d,l)
l = ['A','B','C','D2'] # here, I'd like to retrieve the value of 'D2'
walk_dict(d,l)
l = ['A','B','C','D3'] # get NoneType error as expected because 'D3' does not exist
walk_dict(d,l)
