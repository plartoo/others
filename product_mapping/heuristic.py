import pdb
"""
Description:
This is a word-count-weighted approach similar to bag-of-words but without TFIDF.
To explain differently, this simple heuristic-based approach builds a dictionary
of word counts based on the raw data. Then given an input string, it chops it up
into unique words (thus, bag of words); find their association to each target mapping
in the aforementioned dictionary; add them up; and return the mapping with maximum
count.

For example, suppose the input string is 'Dial Kids : Hair & Body Wash'. 
This heuristic-based approach will look for ['dial', 'kids', 'hair', 'body', 'wash']
in the dictionary of word counts build on the raw (training) data. Suppose, the 
word count dictionary is as follows: 
{'dial' => {'body wash' => 10, 'shampoo' => 2}, 'kids' => {'baby accessories' => 5},
'hair' => {'shampoo' => 10, 'body wash' => 2}, 'body' => {'body wash' => 10},
'wash' => {'detergent' => 20, 'cleaners' => 5, 'body wash' => 4} }
 
Then after adding up the count of target mappings, we get {'body wash' => 26, 
'shampoo' => 12, 'baby accessories' => 5, 'detergent' => 20, 'cleaners' => 5}.
As a result, 'body wash' is assigned as the final target mapping for 
'Dial Kids : Hair & Body Wash'.

Note: this naive approach is NOT supposed to be used in production. I implemented
this to show that even a simple heuristic like this can get us to up to 60% accuracy.
"""

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
    'unmapped_items': queries.unmapped_items,
    'mapped_items': queries.mapped_items,
}
SIGNALS = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
           'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME']
TARGET_CATEGORY = 'CP_SUBCATEGORY_NAME'
EXCLUDED_WORDS = {'N/A'}

OUTPUT_DIR = 'local_cache'
WORD_COUNT_FILE = 'word_count_table.json'
THRESHOLD = 0.8
NOT_ENOUGH_WORDS = 'Not enough input words in raw data to predict reliably. Manual mapping needed.'
NO_SUGGESTIONS = 'No suggestion returned. Manual mapping needed.'
AMBIGUOUS = 'too many similar possibilities. Manual mapping needed.'\


def run_sql(sql):
    conn = pyodbc.connect(account_info.DM_1219)
    return pd.read_sql(sql, conn)


def get_dataframe_from_query(query_name):
    return run_sql(QUERIES[query_name])


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
    # 1. replace commas with spaces (must come first before step 2 below) for cases like 'ROLDA,GEL,(INT)'
    # 2. removes non-alphanumeric and double-or-more space characters;
    # and turn the str into lowercase
    # Note: alternatively, we can do simple thing like this r'\w+' instead
    return re.sub('[^0-9a-zA-Z\s]+', '', re.sub('[,]+', ' ', s)).lower().split()


# TODO: rename to 'build_total_word_cnt_table_from_json'
def build_total_word_cnt_table(data, fields):
    word_count = defaultdict(int)
    for row in data:
        sub_cat = row[TARGET_CATEGORY]
        if sub_cat is None:
            continue
        else:
            for f in fields:
                words = tokenize(row[f])
                for w in words:
                    if w in word_count:
                        if sub_cat in word_count[w]:
                            word_count[w][sub_cat] += 1
                        else:
                            word_count[w][sub_cat] = 1
                    else:
                        word_count[w] = {sub_cat: 1}
    return word_count


def combine_columns(pandas_row, col_names):
    combined_words = []
    for f in col_names:
        combined_words.append(pandas_row[f])
    return ' '.join(combined_words)


# TODO: refactor to combine this with the one above
def build_total_word_cnt_table_from_dataframe(data, fields):
    word_count = defaultdict(int)
    for i, row in data.iterrows():
        sub_cat = row[TARGET_CATEGORY]
        if sub_cat is None:
            continue
        else:
            words = tokenize(combine_columns(row, fields))
            for w in words:
                if w in word_count:
                    if sub_cat in word_count[w]:
                        word_count[w][sub_cat] += 1
                    else:
                        word_count[w][sub_cat] = 1
                else:
                    word_count[w] = {sub_cat: 1}
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


def get_enhanced_suggestion(word_cnt_tbl, words_in):
    suggestions = get_suggestions(word_cnt_tbl, words_in)
    if not suggestions:
        return {'label': NO_SUGGESTIONS, 'count': -1}

    if len(suggestions) > 2:
        hw = get_helpful_words(suggestions)
        if len(hw) > 0:
            # print("Getting enhanced suggestions...")
            suggestions = get_suggestions(word_cnt_tbl, ' '.join(hw))[0]
        else:
            return {'label': AMBIGUOUS, 'count': -1}

    return {'label': suggestions[0], 'count': suggestions[-1][0]}

    # try:
    #     test = {'label': suggestions[0], 'count': suggestions[-1][0]}
    # except:
    #     pdb.set_trace()
    #     return {'label': 'haha', 'count': 0}
    # return test


def have_same_count(suggestions):
    distinct_cnts = set([i[-1][0] for i in suggestions])
    if len(distinct_cnts) < 2:
        return True
    return False


def get_helpful_words(sorted_suggestions):
    """
    Only use this method for words that are longer than length = 2
    """
    helpful_words = [] # words that are not noise--for lack of better naming...
    if have_same_count(sorted_suggestions):
        return helpful_words

    noise_cnt_tbl = defaultdict(int)
    for s in sorted_suggestions:
        # count number of times this word appears in predicted subcats
        for word_cnt in s[-1][-1]: # {'total':25}
            key = list(word_cnt.keys())[0]
            noise_cnt_tbl[key] += 1

    total = len(sorted_suggestions)
    for w,c in noise_cnt_tbl.items():
        if (c/total) <= THRESHOLD:
            helpful_words.append(w)

    return helpful_words


if __name__ == '__main__':
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(cur_dir_path, OUTPUT_DIR)
    word_count_file = os.path.join(output_dir, WORD_COUNT_FILE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    desc = '''
    Guess mappings based on heuristic of previously mapped items and
    allow user to interactively try them out.
    To use reference table for mappping from the local cache file 
    (for faster speed), use '-l' flag.
    For more detail, please use '-h' flag to read the help/manual.
    '''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-l',
                        default=0,
                        type=int,
                        help="If '1', this will USE the LOCAL CACHE FILE  of the word count table named, '"
                             + WORD_COUNT_FILE
                             + "', which is expected to be placed in a local directory named, '"
                             + OUTPUT_DIR + ".'")

    args = parser.parse_args()
    if args.l:
        word_cnt_tbl = load_data_from_json(word_count_file) #json.loads(load_data_from_pickle(word_count_file))
    else:
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
        print("\n<-----Suggestions sorted by frequency----->")
        for s in suggestions:
            print(s[0],"",s[-1][0],"==>", s[-1][1])
        print("<--------------->\n\n\n\n\n\n")
        if len(suggestions) > 2:
            hw = get_helpful_words(suggestions)
            if len(hw) > 0:
                print("Getting enhanced suggestions...")
                suggestions = get_suggestions(word_cnt_tbl, ' '.join(hw))
            else:
                print("'", words_in, "' has ", AMBIGUOUS, "\n")
                continue

        print("<-----Enhanced suggestions sorted by frequency-----")
        for s in suggestions:
            print(s[0],"",s[-1][0],"==>", s[-1][1])
        print("----->\n")

    # 'CP_SUBCATEGORY_NAME' => 'CP_SUBCATEGORY_ID'
    # 'CP_VARIANT_NAME' => 'CP_VARIANT_ID_1PH'
