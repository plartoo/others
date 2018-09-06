import os
import time
import argparse

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from mapping_utils import get_dataframe_from_query, tokenize
from queries import mapped_subcategories_q, unmapped_subcategories_q

DESC = '''
This program guesses subcategory column based on multinomial naive bayes approach. 
To find out how to run, use '-h' flag. Usage example: 
>> python map_subcategories.py -c \"UNITED STATES\"
'''
OUTPUT_DIR = 'output'
OUTPUT_FILE = ''.join(['mapped_subcategories_', str(int(time.time())), '.csv'])
FEATURE_COLUMNS = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
                   'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME']
TARGET_NAME_COLUMN = 'CP_SUBCATEGORY_NAME'
TARGET_ID_COLUMN = 'CP_SUBCATEGORY_ID'

EXCLUDED_WORDS = {'N/A', 'na', 'N', 'A', 'n', 'a'}

# TODO: extend this list; then remove this when we have migrated all APAC countries into main database
APAC_COUNTRIES = ['INDIA', 'SINGAPORE', 'THAILAND']
COLUMNS_FOR_APAC = {
       'Included': 'Included'# if SOS_PRODUCT = 0, then 1; if SOS_PRODUCT = 1, then 2
      ,'CategoryType': 'CategoryType' # leave blank
      ,'GM_SECTOR_NAME': 'Local_Section'
      ,'GM_CATEGORY_NAME': 'Local_Category'
      ,'GM_ADVERTISER_NAME': 'Local_Advertiser'
      ,'GM_BRAND_NAME': 'Local_Brand'
      ,'GM_PRODUCT_NAME': 'Local_Product'
      ,'Comments': 'Comments' # leave blank
      ,'Global_Category ID': 'Global_Category ID' # leave blank
      ,'Global_Category Name': 'Global_Category Name' # leave blank
      ,'Global_ProductCategory ID': 'Global_ProductCategory ID' # leave blank
      ,'Global_ProductCategory Name': 'Global_ProductCategory Name'  # leave blank
      ,'Global_Subcategory ID': 'Global_Subcategory ID' # leave blank
      ,'Global_Subcategory Name': 'Global_Subcategory Name' # leave blank
      ,'Global_Brand ID': 'Global_Brand ID'  # leave blank
      ,'Global_Brand Name': 'Global_Brand Name'  # leave blank
      ,'Global_Subbrand ID': 'Global_Subbrand ID' # leave blank
      ,'Global_Subbrand Name': 'Global_Subbrand Name'  # leave blank
      ,'Global_Variant ID': 'Global_Variant ID' # leave blank
      ,'Global_Variant Name': 'Global_Variant Name' # leave blank
      ,'ExceptionStatus': 'ExceptionStatus' # = 'New'
      ,'GM_COUNTRY_ID': 'GM_COUNTRY_ID'
      ,'GM_COUNTRY_NAME': 'GM_COUNTRY_NAME'
}
COLUMNS_FOR_ALL_OTHERS = {
    'MAPPING_PROCESS_TYPE': 'MAPPING_PROCESS_TYPE'  # 'New_Product_Mapping'
    , 'GM_GLOBAL_PRODUCT_ID': 'GM_GLOBAL_PRODUCT_ID'
    , 'GM_COUNTRY_ID': 'GM_COUNTRY_ID'
    , 'GM_COUNTRY_NAME': 'GM_COUNTRY_NAME'
    , 'GM_ADVERTISER_NAME': 'GM_ADVERTISER_NAME'
    , 'GM_SECTOR_NAME': 'GM_SECTOR_NAME'
    , 'GM_SUBSECTOR_NAME': 'GM_SUBSECTOR_NAME'
    , 'GM_CATEGORY_NAME': 'GM_CATEGORY_NAME'
    , 'GM_BRAND_NAME': 'GM_BRAND_NAME'
    , 'GM_PRODUCT_NAME': 'GM_PRODUCT_NAME'
    , 'SOS_PRODUCT': 'SOS_PRODUCT'
    , 'CP_SUBCATEGORY_ID': 'CP_SUBCATEGORY_ID'
    , 'CP_SUBCATEGORY_NAME': 'CP_SUBCATEGORY_NAME'
    , 'CP_VARIANT_ID_1PH': 'CP_VARIANT_ID_1PH'
    , 'CP_BRAND_ID': 'CP_BRAND_ID'  # leave empty
    , 'CP_BRAND_NAME': 'CP_BRAND_NAME'  # leave empty
    , 'IS_BRAND_MAPPING_EXCEPTION': 'IS_BRAND_MAPPING_EXCEPTION' # leave empty
    , 'IS_QUESTIONABLE_MAPPING': 'IS_QUESTIONABLE_MAPPING' # leave empty
    , 'IS_BRAND_FILTER_EXCEPTION': 'IS_BRAND_FILTER_EXCEPTION' # leave empty
    , 'MAPPING_COMMENTS': 'MAPPING_COMMENTS' # leave empty
    , 'LAST_MAPPED_BY': 'LAST_MAPPED_BY' # 'Multinomial Naive Bayes algorithm'
}


def predict_using_svc(str, model, vectorizer, id_to_name_dict):
    vectorized_str = vectorizer.transform([str])
    predicted_cat_id = model.predict(vectorized_str)[0]
    return id_to_name_dict[predicted_cat_id]


def combine_feature_columns_to_one_long_str(row_from_df):
    combined_str_tokens = tokenize(' '.join(row_from_df[f] for f in FEATURE_COLUMNS))
    return ' '.join([t for t in combined_str_tokens if t not in EXCLUDED_WORDS])


if __name__ == '__main__':
    apac_country = False
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-c',
                        required=True,
                        type=str,
                        help="(Required) Enter the FULL name of the country as seen under [GM_COUNTRY_NAME] column in "
                             "the GM_CP_MASTER_PRODUCT_MAPPING table. E.g., python map_subcategories.py -c \"UNITED STATES\"")
    args = parser.parse_args()
    if args.c in APAC_COUNTRIES: # TODO: remove this when we have migrated all APAC countries into main database
        apac_country = True

    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(cur_dir_path, OUTPUT_DIR)
    output_file = os.path.join(output_dir, OUTPUT_FILE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    unmapped_subcategories_q += " AND GM_COUNTRY_NAME='" + args.c + "'"
    print('Loading mapped subcategories from remote database using query:', mapped_subcategories_q)
    # mapped_subcats_df = get_dataframe_from_query(mapped_subcategories_q) # TODO: uncomment this
    # if you want to save the existing mappings locally (on your computer, uncomment this line and comment out the line above
    mapped_subcats_df = pd.read_csv('mapped_subcats.csv', dtype=str, sep='\t')
    print('Loading unmapped subcategories for', args.c, 'from remote database using query:', unmapped_subcategories_q)
    unmapped_subcats_df = get_dataframe_from_query(unmapped_subcategories_q)

    tfidf_vectorizer = TfidfVectorizer(
        sublinear_tf=True,  # TODO: we can remove this if log scale doesn't work out
        min_df=1,
        norm='l2', # L2 norm
        encoding='utf-8',
        ngram_range=(1, 2),
        stop_words='english'
    )
    print('concat starts', time.asctime())
    # TODO: creating df_x could become a computational bottleneck; need to find a more efficient way to do it like
    # what I used to do below?
    df_x = (mapped_subcats_df['GM_ADVERTISER_NAME'].astype('str').apply(tokenize)
            + mapped_subcats_df['GM_SECTOR_NAME'].astype('str').apply(tokenize)
            + mapped_subcats_df['GM_SUBSECTOR_NAME'].astype('str').apply(tokenize)
            + mapped_subcats_df['GM_CATEGORY_NAME'].astype('str').apply(tokenize)
            + mapped_subcats_df['GM_BRAND_NAME'].astype('str').apply(tokenize)
            + mapped_subcats_df['GM_PRODUCT_NAME'].astype('str').apply(tokenize))\
        .apply(' '.join)
    # The line below works similar to above, but it is a bit slower because we need to make sure
    # each column is converted to str(). The upside of this approach is that it is more aligned with
    # functional style programming.
    # df_x = pd.DataFrame(mapped_subcats_df[FEATURE_COLUMNS].apply(lambda x:  ' '.join(str(x)), axis=1).apply(tokenize), columns=['Col'])
    print('concat ends', time.asctime())

    df_y = pd.DataFrame(mapped_subcats_df, columns=[TARGET_NAME_COLUMN])
    features = tfidf_vectorizer.fit_transform(df_x)
    df_y[TARGET_ID_COLUMN] = df_y[TARGET_NAME_COLUMN].factorize()[0] # assign id labels
    subcat_name_to_id_df = df_y[[TARGET_NAME_COLUMN, TARGET_ID_COLUMN]].drop_duplicates().sort_values(TARGET_ID_COLUMN)
    subcat_name_to_id_ref_table = dict(subcat_name_to_id_df[[TARGET_NAME_COLUMN, TARGET_ID_COLUMN]].values)
    label_id_to_subcat_name = dict(subcat_name_to_id_df[[TARGET_ID_COLUMN, TARGET_NAME_COLUMN]].values)
    labels = df_y[[TARGET_ID_COLUMN]]

    model = LinearSVC()
    x_train, x_test, y_train, y_test, indices_train, indices_test = train_test_split(features,
                                                                                     labels,
                                                                                     mapped_subcats_df.index,
                                                                                     test_size=0,#0.33,
                                                                                     random_state=0)
    print('fitting starts', time.asctime())
    model.fit(x_train, y_train.values.reshape(-1,)) # https://stackoverflow.com/q/34165731/1330974
    print('fitting ends', time.asctime())

    cols = COLUMNS_FOR_APAC if apac_country else COLUMNS_FOR_ALL_OTHERS
    mapped_df = pd.DataFrame(columns=cols.values(), index=None)
    for idx, row in unmapped_subcats_df.iterrows():
        input_str = combine_feature_columns_to_one_long_str(row)
        predicted_subcat = predict_using_svc(input_str,
                                              model,
                                              tfidf_vectorizer,
                                              label_id_to_subcat_name)
        row_headers = row.to_dict().keys()
        vals = [row[c] if c in row_headers else '' for c in cols.keys()]
        vals_with_raw_col_names = dict(zip(cols.keys(), vals))
        vals_with_adjusted_col_names = dict((cols[k], vals_with_raw_col_names[k]) for (k, v) in cols.items())

        if apac_country:
            # TODO: remove this silly stuff as soon as Jholman merged APAC system to our main DB
            vals_with_adjusted_col_names['Included'] = '2' if row.SOS_PRODUCT else '1'
            vals_with_adjusted_col_names['Global_Subcategory ID'] = subcat_name_to_id_ref_table[predicted_subcat]
            vals_with_adjusted_col_names['Global_Subcategory Name'] = predicted_subcat
            vals_with_adjusted_col_names['ExceptionStatus'] = 'New'
            vals_with_adjusted_col_names['Comments'] = 'mapped by Multinomial Naive Bayes algorithm'
        else:
            # this is for non-APAC countries
            vals_with_adjusted_col_names['MAPPING_PROCESS_TYPE'] = 'New_Product_Mapping'
            vals_with_adjusted_col_names[TARGET_ID_COLUMN] = subcat_name_to_id_ref_table[predicted_subcat]
            vals_with_adjusted_col_names[TARGET_NAME_COLUMN] = predicted_subcat
            vals_with_adjusted_col_names['LAST_MAPPED_BY'] = 'mapped by Multinomial Naive Bayes algorithm'

        mapped_df.loc[len(mapped_df)] = vals_with_adjusted_col_names

    mapped_df.to_csv(output_file, index=False, sep=',')
    print('Finished guessing the mappings. Results written to', output_file)
