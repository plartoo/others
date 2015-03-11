__author__ = 'lacheephyo'

"""
Python script to generate ASCII characters
of random size (MIN < size < MAX) and write them in
files labeled sequentially as
"1.txt", "2.txt", ..., "100.txt"
"""

import random
import string

MAX = 9000
MIN = 500
NUM_OF_FILES = 100

file_counter = 1

while (file_counter <= NUM_OF_FILES):
    fout_name = str(file_counter) + ".txt"
    fout = open(fout_name, 'w')

    # generate random sized ASCII chars and write them
    random_str =  ''.join(random.choice(string.printable)
                          for _ in range(random.randint(MIN,MAX)))

    fout.write(random_str)

    file_counter += 1
    fout.close()


