__author__ = 'lacheephyo'

"""
Python script to count ASCII characters in files spanning
from "1.txt", "2.txt", ..., "104.txt".
"""

import pprint
char_count = {}

#for i in range(0,1):
for i in range(0,105):
    fin_name = str(i) + ".txt"

    fin = open(fin_name)
    line = ''.join(fin.readlines()) # all lines in the file combined
    fin.close()
    #print line
    for char in line:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count.setdefault(char, 1)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(char_count)
