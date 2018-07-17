import pdb
import csv
import json

import heuristic

SIGNALS = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
           'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME']
TARGET_CATEGORY = 'CP_SUBCATEGORY_NAME'
EXCLUDED_WORDS = {'N/A'}

query_name = 'mapped_items'
print('Loading data from remote database using query:', heuristic.QUERIES[query_name])
mapping_data = json.loads(heuristic.get_data_from_query(query_name))

word_lens = set()
uniq_chars = set()
input_output = {}

for row in mapping_data:
    cur_word = []
    for sig in SIGNALS:
        if row[sig] not in EXCLUDED_WORDS:
            cur_word.append(row[sig])
    cur_word_str = ' '.join(cur_word)
    tokenized_word = ' '.join(heuristic.tokenize(cur_word_str))
    word_lens.add(len(tokenized_word))
    input_output[tokenized_word] = row[TARGET_CATEGORY]

    for chr in tokenized_word:
        uniq_chars.add(chr)

max_word_len = max(word_lens)
encoded = []
# assign labels to unique characters found in the entire raw data set
# e.g., {'a': 0, 'b': 1, 'z': 26, ...}
char_map = {k: v for v,k in enumerate(sorted(list(uniq_chars)))}
char_cnt = len(char_map.keys())
row_cnt = 0

my_qa_file = open('raw_mappings_qa.csv', 'w')
qa_csv_writer = csv.writer(my_qa_file)

my_file = open('raw_mappings.csv', 'w')
csv_writer = csv.writer(my_file)

for input_words,output_category in input_output.items():
    row_cnt += 1
    print('Loading:', row_cnt)
    qa_csv_writer.writerow([input_words, output_category])

    cur_encoded = []
    cur_byte_arr = bytearray(char_cnt * max_word_len)
    # Note: approach#1 below does NOT fly because the sublists are mutable
    # approach#2 and #3 both ran out of memory (of course!)
    # cur_encoded = [([0] * char_cnt)]* max_word_len # approach#1
    # cur_encoded = [[0 for i in range(char_cnt)] for i in range(max_word_len)] # approach#2
    # cur_binary_encoded_csv = [0 for i in range(char_cnt) for i in range(max_word_len)] # approach#3
    cur_space_saving_encoded_csv = [0 for i in range(max_word_len)] # approach#4 space saving

    for i,chr in enumerate(input_words):
        # approach #1
        # cur_encoded[i][char_map[chr]] = 1 # set corresponding bits to '1' in the array

        # approach #2 and #3
        # idx = (i * char_cnt) + char_map[chr]
        # cur_byte_arr[idx] = 1
        # cur_binary_encoded_csv[idx] = 1  # set corresponding bits to '1' in the array

        cur_space_saving_encoded_csv[i] = char_map[chr]
    # approach #3
    # cur_binary_encoded_csv.append(output_category)
    # csv_writer.writerow(cur_binary_encoded_csv)

    # approach #4
    cur_space_saving_encoded_csv.append(output_category)
    csv_writer.writerow(cur_space_saving_encoded_csv)

    # cur_encoded.append(cur_byte_arr)
    # cur_encoded.append(output_category)
    # encoded.append(cur_encoded)

# pdb.set_trace()
my_qa_file.close()
my_file.close()

print('Finished')

# I ran into issue installing Tensorflow using pipenv, so I followed this recommendation
# https://stackoverflow.com/a/49908957
# pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.9.0-py3-none-any.whl

# TODO: https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
# https://www.tensorflow.org/versions/r1.1/install/install_windows
# after installing Python 3.5x, do this
# > pipenv --python 3.5
# > pip3 install --upgrade tensorflow
# > pipenv install pandas
# 