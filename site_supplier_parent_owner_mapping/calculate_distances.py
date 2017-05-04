import argparse

from word_similarity import *
from mapper_utils import *


def main():
    parser = argparse.ArgumentParser(description='Calculate and build the distance table out of the words in the input file.')
    parser.add_argument('-i','--input', required=True, help='Input file with all possible words in the domain')
    args = parser.parse_args()
    import pdb
    pdb.set_trace()
    print(args)

if __name__ == "__main__":
    main()
