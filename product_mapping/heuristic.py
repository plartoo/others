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
THRESHOLD = 0.5
AMBIGUOUS = 'too many similar possibilities. Manual mapping needed.'\
    #('Too many similar possibilities. Manual mapping needed.', (None, None))

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
    print('Data loaded from file:', file)
    return data


def write_data_to_json(json_data, file):
    with open(file, 'w') as fo:
        json.dump(json_data, fo)
    print("JSON data written to:", file)


def load_data_from_json(file):
    with open(file, 'r') as fi:
        data = json.load(fi)
    print('Data loaded from file:', file)
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
    subcat_cnt_by_word = defaultdict(list)
    words = tokenize(words_in)
    for w in words:
        if w in word_cnt_t1:
            for cat,cnt in word_cnt_t1[w].items():
                subcat_cnt_by_word[cat].append({w: cnt})

    temp = {a: (sum(list(i.values())[0] for i in b), b) for a, b in subcat_cnt_by_word.items()}
    subcat_cnt_by_word = sorted(temp.items(), key=lambda x: x[-1][0], reverse=True)
    return subcat_cnt_by_word


def have_same_count(suggestions):
    distinct_cnts = set([i[-1][0] for i in suggestions])
    if len(distinct_cnts) < 2:
        return True
    return False


def get_helpful_words(sorted_suggestions):
    """
    Only use this method for words that are longer than length = 2
    """
    value_words = [] # words that are not noise--for lack of better naming...
    if have_same_count(sorted_suggestions):
        return value_words

    noise_cnt_tbl = defaultdict(int)
    for s in sorted_suggestions:
        # count number of times this word appears in predicted subcats
        for word_cnt in s[-1][-1]: # {'total':25}
            key = list(word_cnt.keys())[0]
            noise_cnt_tbl[key] += 1

    total = len(sorted_suggestions)
    for w,c in noise_cnt_tbl.items():
        if (c/total) <= THRESHOLD:
            value_words.append(w)

    return value_words



if __name__ == '__main__':
    OUTPUT_DIR = 'pickled_data'
    WORD_COUNT_FILE = 'word_count_table.json'

    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(cur_dir_path, OUTPUT_DIR)
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
    parser.add_argument('-l',
                        default=0,
                        type=int,
                        help="If '1', this will USE the local cache file of the word count table named, '"
                             + WORD_COUNT_FILE
                             + "', which is expected to be placed in a local directory named, '"
                             + OUTPUT_DIR + ".'")

    args = parser.parse_args()
    if args.l:
        word_cnt_tbl = load_data_from_json(word_count_file) #json.loads(load_data_from_pickle(word_count_file))
    else:
        SIGNALS = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
                   'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME']
        query_name = 'all_mappings'

        print('Loading data from remote database using query:', QUERIES[query_name])
        mapping_data = json.loads(get_data_from_query(query_name))
        word_cnt_tbl = build_total_word_cnt_table(mapping_data, SIGNALS)
        # word_cnt_tbl = build_column_specific_table(mapping_data, SIGNALS)
        write_data_to_json(word_cnt_tbl, word_count_file)

    print("Data loaded and ready to start predicting.\n")
    while True:
        words_in = input('Enter your input (or enter to exit): ')
        if len(words_in) == 0:
            print('Program finished.')
            break

        suggestions = get_suggestions(word_cnt_tbl, words_in)
        if len(suggestions) > 2:
            hw = get_helpful_words(suggestions)
            if len(hw) > 0:
                print("Getting enhanced suggestions...")
                suggestions = get_suggestions(word_cnt_tbl, ' '.join(hw))
            else:
                print("'", words_in, "' has ", AMBIGUOUS, "\n")
                continue

        print("<-----Suggestions sorted by frequency-----")
        for s in suggestions:
            print(s[0],"",s[-1][0],"==>", s[-1][1])
        print("----->\n")

    # 'CP_SUBCATEGORY_NAME' => 'CP_SUBCATEGORY_ID'
    # 'CP_VARIANT_NAME' => 'CP_VARIANT_ID_1PH'
