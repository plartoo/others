import sys
import csv
import getopt
import re

#usage: python suggest_sites.py -i sspo.csv -o results -a 0 -b 3

from levenshtein import Similarity


class MapperUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def transform_word(w):
        w = w.lower()
        w = re.sub(r'\s|"|\'|-|,|;|:', '', w)   # remove space, double+single quote, dash, comma, semi colon, colon
        w = re.sub(r'(www\.)|\.(com|net|org|int|edu|gov|mil)|\/$', '', w) # remove '.com', '.net', trailing '/' etc.
        w = re.sub(r'https?:\/\/', '', w)

        # r'^xaxis' is one word that we can remove
        return w


class Mapper(object):
    def __init__(self):
        pass


def main(argv):
    verbose = True
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:a:b:",["ifile=","ofile=","col1=", "col2="])
    except getopt.GetoptError:
        print('Usage: map_words.py -i <input file> -o <output file> -a <col 1> -b <col2>')
        sys.exit(2)

    if len(argv) == 0:
        print('Usage: map_words.py -i <input file> -o <output file>  -a <column 1> -b <column 2>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: map_words.py -i <inputfile> -o <outputfile> -a <column 1> -b <column 2>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-a", "--col1"):
            col_idx1 = int(arg)
        elif opt in ("-b", "--col2"):
            col_idx2 = int(arg)

    """
        Load raw data; clean/transform it.
    """
    if verbose: print("Working hard (hardly working) on: ", input_file)
    if verbose: print("Loading data from:", input_file)

    sites = []
    updated_sites = []

    sites_map_updated_sites = {} # sites_deduped is sites_map_updated_sites.keys()
    updated_sites_map_sites = {}
    sites_transformed_dict = {}
    updated_sites_transformed_dict = {}

    with open(input_file, 'r') as infile:
        file_reader = csv.reader(infile, delimiter=',', quotechar='"')

        for row in file_reader:
            site = row[col_idx1]
            updated_site = row[col_idx2]

            sites.append(site)
            updated_sites.append(updated_site)
            sites_map_updated_sites[site] = updated_site # NOTE: assumes that site => updated_site mapping is one-to-one
            updated_sites_map_sites[updated_site] = site

            site_transformed = MapperUtils.transform_word(site)
            updated_site_transformed = MapperUtils.transform_word(updated_site)
            sites_transformed_dict[site_transformed] = 'site'
            updated_sites_transformed_dict[updated_site_transformed] = 'updated site'

        # print("sites: ", len(sites))
        # print("updated_sites: ", len(updated_sites))
        # print("sites map updated sites: ", len(sites_map_updated_sites))
        # print("updated sites map sites: ", len(updated_sites_map_sites))
        # print("sites transformed dict: ", len(sites_transformed_dict))
        # print("updated sites transformed dict: ", len(updated_sites_transformed_dict))

    """
        Build similarity score tables
    """
    if verbose: print("Constructing similarity score tables...")

    jaro_table = {}
    leven_table = {}
    lcs_table = {}
    jaccard_table = {}

    for w1 in sites_map_updated_sites.keys(): # take from unique_sites_transformed to save computation
        for w2 in updated_sites_map_sites.keys():

            wt1 = MapperUtils.transform_word(w1)
            wt2 = MapperUtils.transform_word(w2)

            if not w1 in jaro_table:
                jaro_table[w1] = {}
            jaro_table[w1][w2] = Similarity.jaro_score(wt1, wt2)

            if not w1 in leven_table:
                leven_table[w1] = {}
            leven_table[w1][w2] = Similarity.levenshtein_normalized_score(wt1, wt2)

            if not w1 in lcs_table:
                lcs_table[w1] = {}
            lcs_table[w1][w2] = Similarity.lcs_score(wt1, wt2)

            if not w1 in jaccard_table:
                jaccard_table[w1] = {}
            jaccard_table[w1][w2] = Similarity.jaccard_similarity(wt1, wt2)

    """
        Sort the scores in the table
    """
    if verbose: print("Sorting similarity score tables...")

    jaro_sorted = {}
    leven_sorted = {}
    lcs_sorted = {}
    jaccard_sorted = {}
    for w1, score_table in jaro_table.items():
        jaro_sorted[w1] = sorted(score_table.items(), key=lambda x: -x[1])
    for w1, score_table in leven_table.items():
        leven_sorted[w1] = sorted(score_table.items(), key=lambda x: -x[1])
    for w1, score_table in lcs_table.items():
        lcs_sorted[w1] = sorted(score_table.items(), key=lambda x: -x[1])
    for w1, score_table in jaccard_table.items():
        jaccard_sorted[w1] = sorted(score_table.items(), key=lambda x: -x[1])

    """
        Get the suggestions
    """
    if verbose: print("Preparing output data...")

    # if cannot predict, write 'NULL'
    output_table = [[
        'source', 'truth',
        'jaro suggested 1', 'score of jaro suggested 1', 'jaro suggested 1 correct', # 1 for True; 0 for False
        'equalOrabove jaro threshold 1', # 1 or 0 indicating if the suggested label passes our arbitrary threshold
        'jaro suggested 2', 'score of jaro suggested 2', 'jaro suggested 2 correct', 'equalOrabove jaro threshold 2',
        'jaro suggested 3', 'score of jaro suggested 3', 'jaro suggested 3 correct', 'equalOrabove jaro threshold 3',

        'leven suggested 1', 'score of leven suggested 1', 'leven suggested 1 correct',
        'equalOrabove leven threshold 1',
        'leven suggested 2', 'score of leven suggested 2', 'leven suggested 2 correct', 'equalOrabove leven threshold 2',
        'leven suggested 3', 'score of leven suggested 3', 'leven suggested 3 correct', 'equalOrabove leven threshold 3',

        'lcs suggested 1', 'score of lcs suggested 1', 'lcs suggested 1 correct',
        'equalOrabove lcs threshold 1',
        'lcs suggested 2', 'score of lcs suggested 2', 'lcs suggested 2 correct', 'equalOrabove lcs threshold 2',
        'lcs suggested 3', 'score of lcs suggested 3', 'lcs suggested 3 correct', 'equalOrabove lcs threshold 3',

        'jaccard suggested 1', 'score of jaccard suggested 1', 'jaccard suggested 1 correct',
        'equalOrabove jaccard threshold 1',
        'jaccard suggested 2', 'score of jaccard suggested 2', 'jaccard suggested 2 correct', 'equalOrabove jaccard threshold 2',
        'jaccard suggested 3', 'score of jaccard suggested 3', 'jaccard suggested 3 correct', 'equalOrabove jaccard threshold 3',
    ]]

    jaro_threshold = 0.95 # empirical value from score3.xlsx which is the output of process_sites.py
    jaccard_threshold = 0.88
    leven_threshold = 0.85
    lcs_threshold = 0.85

    for i, site in enumerate(sites):
        truth = updated_sites[i]
        out_row = [site, truth]

        sorted_score_tables = [jaro_sorted, leven_sorted, lcs_sorted, jaccard_sorted]
        for k, score_table in enumerate(sorted_score_tables):
            thresholds = [jaro_threshold, leven_threshold, lcs_threshold, jaccard_threshold]

            for j in range(0,len(sorted_score_tables)):
                suggested_word = score_table[site][j][0]
                suggested_word_score = score_table[site][j][1]

                out_row.append(suggested_word)
                out_row.append(suggested_word_score)

                out_row.append(1 if suggested_word == truth else 0)
                out_row.append(1 if suggested_word_score >= thresholds[k] else 0)

        output_table.append(out_row)

    with open(output_file+'.csv', 'w') as csvfile:
        if verbose: print("Results written to:", output_file + ".csv")
        csv_writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        csv_writer.writerows(output_table)

if __name__ == "__main__":
    main(sys.argv[1:])
