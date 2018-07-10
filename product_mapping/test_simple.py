import pdb
"""
Description: 
A quick script to test the accuracy of (simple word-count-based) heuristic approach.
"""
import random

from sklearn.model_selection import train_test_split

import heuristic

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
EXCLUDED_WORDS = {'N/A'}
INPUT_CATEGORIES = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
                 'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME']
TARGET_CATEGORY = 'CP_SUBCATEGORY_NAME'
TEST_ITERATIONS = 100

def is_correct(word_cnt_tbl, input_words, row):
    predicted = heuristic.get_enhanced_suggestion(word_cnt_tbl, input_words)['label']
    actual = row.CP_SUBCATEGORY_NAME
    return predicted == actual

if __name__ == '__main__':
    query_name = 'mapped_items'
    print('Loading data from remote database using query:', heuristic.QUERIES[query_name])
    df = heuristic.get_dataframe_from_query(query_name)

    total_cnt = 0
    hit_cnt = 0
    miss_cnt = 0
    all_signal_hit_cnt = 0
    all_signal_miss_cnt = 0
    for i in range(TEST_ITERATIONS):
        input_cols = INPUT_CATEGORIES + [TARGET_CATEGORY]
        x_train, x_test, y_train, y_test = train_test_split(df[input_cols],
                                                            df[TARGET_CATEGORY],
                                                            test_size=0.2,
                                                            random_state=random.randint(0,10*TEST_ITERATIONS))

        word_cnt_tbl = heuristic.build_total_word_cnt_table_from_dataframe(x_train, INPUT_CATEGORIES)
        for i, row in x_test.iterrows():
            total_cnt += 1

            # use just product_name as input signal
            if is_correct(word_cnt_tbl, row.GM_PRODUCT_NAME, row):
                hit_cnt += 1
            else:
                miss_cnt += 1

            # now let's try to use all signals as input
            input_words = heuristic.combine_columns(row, INPUT_CATEGORIES)
            if is_correct(word_cnt_tbl, input_words, row):
                all_signal_hit_cnt += 1
            else:
                all_signal_miss_cnt += 1

        print("\n====\ntotal:",total_cnt)
        print("\thit_cnt:",hit_cnt,"\tmiss_cnt:",miss_cnt)
        print("\tall_signal_hit_cnt:", all_signal_hit_cnt, "\tall_signal_miss_cnt:", all_signal_miss_cnt)