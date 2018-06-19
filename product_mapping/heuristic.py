import pprint
pp = pprint.PrettyPrinter(indent=4)
import pdb

import argparse
import json
import os
import pickle
import re
from collections import defaultdict

import pandas as pd
import pyodbc

import account_info
import queries


QUERIES = {
    'all_mappings': queries.all_mappings,
}


def run_sql(sql):
    conn = pyodbc.connect(account_info.DM_1219)
    return pd.read_sql(sql, conn)


def get_data_from_query(query_name):
    df = run_sql(QUERIES[query_name])
    data_str = df.to_json(orient='records')
    return data_str


def write_data_to_pickle(data, file):
    with open(file, 'wb') as fo:
        pickle.dump(data, fo)
    print("Serialized data written to:", file)


def load_data_from_pickle(file):
    with open(file, 'rb') as fi:
        data = pickle.load(fi)
    return data


def tokenize(s):
    # removes non-alphanumeric and space characters; and turn the str into lowercase
    # Or we can do simple thing like this r'\w+' instead
    return re.sub('[^0-9a-zA-Z\s]+', '', s).lower().split()


def build_total_word_cnt_table(data, fields):
    word_count = defaultdict(int)
    for r in data:
        sub_cat = r['CP_SUBCATEGORY_NAME'] #TODO: refactor
        if sub_cat is None:
            continue
        else:
            for f in fields:
                words = tokenize(r[f])
                for w in words:
                    if w in word_count:
                        if sub_cat in word_count[w]:
                            word_count[w][sub_cat] += 1
                        else:
                            word_count[w][sub_cat] = 1
                    else:
                        word_count[w] = {sub_cat: 1}
    return word_count


def build_column_specific_table(data, fields):
    word_count = defaultdict(int)
    for r in data:
        sub_cat = r['CP_SUBCATEGORY_NAME'] #TODO: refactor
        if sub_cat is None:
            continue
        else:
            for f in fields:
                words = tokenize(r[f])
                for w in words:
                    if w in word_count:
                        if f in word_count[w]:
                            if sub_cat in word_count[w][f]:
                                word_count[w][f][sub_cat] += 1
                            else:
                                word_count[w][f][sub_cat] = 1
                        else:
                            word_count[w][f] = {sub_cat: 1}
                    else:
                        word_count[w] = {f: {sub_cat: 1}}
    return word_count


def get_suggestions(word_cnt_t1, words_in):
    subcat_cnt = defaultdict(int)
    words = tokenize(words_in)
    for w in words:
        if w in word_cnt_t1:
            for k,v in word_cnt_t1[w].items():
                subcat_cnt[k] += v
    return subcat_cnt

if __name__ == '__main__':
    MAPPING_FILE = 'mapping_table.p'
    WORD_COUNT_FILE = 'word_count_table.p'
    OUTPUT_DIR = 'pickled_data'

    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(cur_dir_path, OUTPUT_DIR)
    mapping_file = os.path.join(output_dir, MAPPING_FILE)
    word_count_file = os.path.join(output_dir, WORD_COUNT_FILE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # REF: https://stackoverflow.com/a/30493366
    desc = '''
    Guess mappings based on heuristic of previously mapped items.
    To generate serialized mapping data in a local folder (for faster load),
    please use '-s' as flag.  
    To load data from local file (faster) approach, set '-l' flag.
    For more detail, please use '-h' flag to read the help/manual.
    '''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-sm',
                        default=0,
                        type=int,
                        help="If '1', this will generate a serialized file, named '"
                             + MAPPING_FILE
                             + "' of existing mapping data in a local directory named, '"
                             + OUTPUT_DIR + ".'")
    parser.add_argument('-lm',
                        default=0,
                        type=int,
                        help="If '1', this will try to load mappings from a file named '"
                             + MAPPING_FILE
                             + "'in a directory called '" + OUTPUT_DIR
                             + "'. Else, it'll load directly from the remote database table.")
    parser.add_argument('-st',
                        default=0,
                        type=int,
                        help="If '1', this will generate a serialized file, named '"
                             + WORD_COUNT_FILE
                             + "' of word count table in a local directory named, '"
                             + OUTPUT_DIR + ".'")

    args = parser.parse_args()
    if args.sm:
        write_data_to_pickle(get_data_from_query('all_mappings'), mapping_file)
    else:
        if args.lm:
            print("Loading data from file:", mapping_file)
            data = json.loads(load_data_from_pickle(mapping_file))
        else:
            query_name = 'all_mappings'
            print("Loading data from remote database using query:", QUERIES[query_name])
            data = json.loads(get_data_from_query(query_name))

        SIGNALS = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
                   'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME']
        word_cnt_t1 = build_total_word_cnt_table(data, SIGNALS)
        # word_cnt_t2 = build_column_specific_table(data, SIGNALS)
        if args.st:
            write_data_to_pickle(word_cnt_t1, word_count_file)

        while True:
            words_in = input('Enter your input (or enter to exit): ')
            if len(words_in) == 0:
                print
                "goodbye"
                break
            print
            suggestions = get_suggestions(word_cnt_t1, words_in)
            print(suggestions)
            '-----'
            for w in suggestions:
                print(w)
            '-----'
            print
            " "
        print("Data loaded")
        # 'CP_SUBCATEGORY_NAME' => 'CP_SUBCATEGORY_ID'
        # 'CP_VARIANT_NAME' => 'CP_VARIANT_ID_1PH'
