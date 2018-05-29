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

def r_retrieve(lst, key):


def retrieve(dict, path, key='children'):

    for k in path:
        if key in dict:




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
    ele = walk_dict(d,a)

    print(walk_dict(d, a))
    a = ['A', 'B', 'C', 'D2']
    print(walk_dict(d, a))
    a = ['A', 'B', 'C', 'D3']
    print(walk_dict(d, a))
    a = ['A', 'B1', 'C', 'D3']
    print(walk_dict(d, a))

if __name__ == '__main__':
    main()
