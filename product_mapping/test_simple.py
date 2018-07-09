import pdb

import json
import os
import random
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

import heuristic

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
EXCLUDED_WORDS = {'N/A'}
INPUT_CATEGORIES = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
                 'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME']
TARGET_CATEGORY = 'CP_SUBCATEGORY_NAME'
TEST_ITERATIONS = 100

if __name__ == '__main__':
    query_name = 'mapped_items'
    print('Loading data from remote database using query:', heuristic.QUERIES[query_name])
    df = heuristic.get_dataframe_from_query(query_name)

    for i in range(TEST_ITERATIONS):
        input_cols = INPUT_CATEGORIES + [TARGET_CATEGORY]
        x_train, x_test, y_train, y_test = train_test_split(df[input_cols],
                                                            df[TARGET_CATEGORY],
                                                            test_size=0.2,
                                                            random_state=random.randint(0,10*TEST_ITERATIONS))

        word_cnt_tbl = heuristic.build_total_word_cnt_table_from_dataframe(x_train, INPUT_CATEGORIES)
        print(heuristic.get_enhanced_suggestion(word_cnt_tbl, 'Dry Idea : Solid Antiperspirant'))
        print(heuristic.get_enhanced_suggestion(word_cnt_tbl, 'Henkel : Misc Merchandise'))
        print(heuristic.get_enhanced_suggestion(word_cnt_tbl, 'Renuzit Aromatherapy Collection Air Freshener & Renuzit Farm Fresh Air Freshener : Combo'))
        print(heuristic.get_enhanced_suggestion(word_cnt_tbl, 'Schwarzkopf : General Promotion - Hair Care Products'))
        print(heuristic.get_enhanced_suggestion(word_cnt_tbl, 'Dial For Men Odor Armor : Body Wash & Bar Soap'))
        print(heuristic.get_enhanced_suggestion(word_cnt_tbl, 'Purex Crystals : Fabric Softener Crystals'))
        print(heuristic.get_enhanced_suggestion(word_cnt_tbl, 'Got 2B Glued : Hair Spray'))

        pdb.set_trace()
        print(x_train.iloc[0])
        print(y_train.iloc[0])

    # mapping_data = json.loads(heuristic.get_data_from_query(query_name))

    # if args.f:
    #     input_file = os.path.join(input_dir, args.f)
    #     filename, file_extension = os.path.splitext(args.f)
    #     if file_extension == '.csv':
    #         output_file = os.path.join(output_dir, (args.f + '-' + cur_date + '.csv'))
    #         output_in_csv = True
    #         df = pd.read_csv(input_file, index_col=False)
    #     elif file_extension == '.xlsx':
    #         output_file = os.path.join(output_dir, (args.f + '-' + cur_date + '.xlsx'))
    #         df = pd.read_excel(input_file, index_col=False)
    #     else:
    #         print("The file format (extension) is not supported. Only CSV and XLSX as input file will work.")
    #         sys.exit()
    #     input_data = df.to_json(orient='records')
    # elif args.d:
    #     output_file = os.path.join(output_dir, ('database_pull' + '-' + cur_date + '.xlsx'))
    #     query_name = 'unmapped_items'
    #     print('Pulling input data from remote database using query:', heuristic.QUERIES[query_name])
    #     input_data = heuristic.get_data_from_query(query_name)
    # else:
    #     pass
    #
    # input_data = json.loads(input_data)
    # output_data = []
    # for input_row in input_data:
    #     print("\n------------")
    #     print("Current row:")
    #     print(input_row)
    #     uniq_input_words = set()
    #     for sig in INPUT_SIGNALS:
    #         if input_row[sig] is not None:
    #             uniq_input_words.add(input_row[sig])
    #
    #     uniq_input_words = list(uniq_input_words - EXCLUDED_WORDS)
    #     if len(uniq_input_words) == 0:
    #         input_row['CP_SUBCATEGORY_NAME'] = heuristic.NOT_ENOUGH_WORDS
    #     else:
    #         suggestions = heuristic.get_suggestions(word_cnt_tbl, ' '.join(uniq_input_words))
    #         if len(suggestions) > 2:
    #             # if a lot of suggestions were returned originally, try to filter out noisy words
    #             helpful_words = heuristic.get_helpful_words(suggestions)
    #             if len(helpful_words) > 0:
    #                 print("\nGot enhanced suggestions:")
    #                 suggestions = heuristic.get_suggestions(word_cnt_tbl, ' '.join(helpful_words))
    #             else:
    #                 suggestions = [(heuristic.AMBIGUOUS,)]
    #
    #         print(suggestions)
    #         print("------------\n")
    #         input_row['CP_SUBCATEGORY_NAME'] = suggestions[0][0] if len(suggestions) > 0 else heuristic.NO_SUGGESTIONS
    #
    #     output_data.append(input_row)
    #
    # cols = list(output_data[0].keys())
    # df = pd.DataFrame.from_dict(output_data)
    # if output_in_csv:
    #     df.to_csv(output_file, index=False, columns=cols)
    # else:
    #     df.to_excel(output_file, index=False, columns=cols)
    # print("Output written in:", output_file)
    # print("Program successfully finished.\n")
