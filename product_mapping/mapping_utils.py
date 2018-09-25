import argparse
import os
import pickle
import re
import time

import pandas as pd
import pyodbc

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib

import account_info

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
EXCLUDED_WORDS = {'N/A', 'na', 'N', 'A', 'n', 'a'}
# TODO: extend this list; then remove this when we have migrated all APAC countries into main database
APAC_COUNTRIES = ['INDIA', 'SINGAPORE', 'THAILAND', 'INDONESIA']

LABEL_ID_COLUMN = 'LABEL_ID'
RAW_COLUMN_NAMES_FOR_APAC = [
'Included'
,'CategoryType'
,'GM_SECTOR_NAME'
,'GM_CATEGORY_NAME'
,'GM_ADVERTISER_NAME'
,'GM_BRAND_NAME'
,'GM_PRODUCT_NAME'
,'Comments'
,'Global_Category ID'
,'Global_Category Name'
,'Global_ProductCategory ID'
,'Global_ProductCategory Name'
,'Global_Subcategory ID'
,'Global_Subcategory Name'
,'Global_Brand ID'
,'Global_Brand Name'
,'Global_Subbrand ID'
,'Global_Subbrand Name'
,'Global_Variant ID'
,'Global_Variant Name'
,'ExceptionStatus'
,'GM_COUNTRY_ID'
,'GM_COUNTRY_NAME'
]

FINAL_COLUMN_NAMES_FOR_APAC = [
'Included'  # if SOS_PRODUCT = 0, then 1; if SOS_PRODUCT = 1, then 2
,'CategoryType'  # leave blank
,'Local_Section'
,'Local_Category'
,'Local_Advertiser'
,'Local_Brand'
,'Local_Product'
,'Comments'  # leave blank
,'Global_Category ID'  # leave blank
,'Global_Category Name'  # leave blank
,'Global_ProductCategory ID'  # leave blank
,'Global_ProductCategory Name'  # leave blank
,'Global_Subcategory ID'  # leave blank
,'Global_Subcategory Name'  # leave blank
,'Global_Brand ID'  # leave blank
,'Global_Brand Name'  # leave blank
,'Global_Subbrand ID'  # leave blank
,'Global_Subbrand Name'  # leave blank
,'Global_Variant ID'  # leave blank
,'Global_Variant Name'  # leave blank
,'ExceptionStatus'  # = 'New'
,'GM_COUNTRY_ID'
,'GM_COUNTRY_NAME'
]

COLUMN_NAMES_FOR_ALL_OTHERS = [
    'MAPPING_PROCESS_TYPE' # 'New_Product_Mapping'
    ,'GM_GLOBAL_PRODUCT_ID'
    ,'GM_COUNTRY_ID'
    ,'GM_COUNTRY_NAME'
    ,'GM_ADVERTISER_NAME'
    ,'GM_SECTOR_NAME'
    ,'GM_SUBSECTOR_NAME'
    ,'GM_CATEGORY_NAME'
    ,'GM_BRAND_NAME'
    ,'GM_PRODUCT_NAME'
    ,'SOS_PRODUCT'
    ,'CP_SUBCATEGORY_ID'
    ,'CP_SUBCATEGORY_NAME'
    ,'CP_VARIANT_ID_1PH'
    ,'CP_VARIANT_NAME'
    ,'CP_BRAND_ID' # leave empty
    ,'CP_BRAND_NAME' # leave empty
    ,'IS_BRAND_MAPPING_EXCEPTION' # leave empty
    ,'IS_QUESTIONABLE_MAPPING' # leave empty
    ,'IS_BRAND_FILTER_EXCEPTION' # leave empty
    ,'MAPPING_COMMENTS' # leave empty
    ,'LAST_MAPPED_BY' # 'Multinomial Naive Bayes algorithm'
]


def run_sql(sql):
    conn = pyodbc.connect(account_info.DM_1219)
    return pd.read_sql(sql, conn)


def get_dataframe_from_query(query):
    return run_sql(query)


def tokenize(s):
    # 1. replace commas and forward slashes with spaces
    # (this step must come first before step 2 below) for cases like 'ROLDA,GEL,(INT)'
    # 2. removes non-alphanumeric and double-or-more space characters;
    # and turn the str into lowercase
    # Note: alternatively, we can do simple thing like this r'\w+' instead
    return re.sub('[^0-9a-zA-Z\s]+', '', re.sub('[,//]+', ' ', s)).lower().split()


def predict_using_svc(input_str, model, vectorizer, id_to_name_dict):
    vectorized_str = vectorizer.transform([input_str])
    predicted_cat_id = model.predict(vectorized_str)[0]
    # print("Predicted =>", predicted_cat_id, ':', id_to_name_dict[predicted_cat_id])
    return id_to_name_dict[predicted_cat_id]


def combine_feature_columns_to_one_long_str(row_from_df, feature_cols):
    combined_str_from_columns = ' '.join(str(row_from_df[f]) for f in feature_cols)
    cleaned_str_tokens = tokenize(combined_str_from_columns)
    return ' '.join([t for t in cleaned_str_tokens if t not in EXCLUDED_WORDS])


def fit_linear_svc_model(features, labels):
    model = LinearSVC()
    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0, random_state=0)
    print('Model fitting starts:', time.asctime())
    model.fit(x_train, y_train.values.reshape(-1,)) # https://stackoverflow.com/q/34165731/1330974
    print('Model fitting ends:', time.asctime())
    return model


def prepare_label_data(mapped_df, target_name_col, target_id_col):
    """
    Takes in raw mapping data for training. Split it into label dataframe,
    label id to label name table, and label name to raw label id table.
    The latter two tables are used to get the raw ID of the target (as it
    appears in the SQL data table).
    """
    label_df = pd.DataFrame(mapped_df, columns=[target_name_col, target_id_col])
    label_df[LABEL_ID_COLUMN] = label_df[target_name_col].factorize()[0] # assign id labels

    target_name_to_target_id_df = label_df[[target_name_col, target_id_col, LABEL_ID_COLUMN]].drop_duplicates().sort_values(target_id_col)
    label_id_to_target_name = dict(target_name_to_target_id_df[[LABEL_ID_COLUMN, target_name_col]].values)
    target_name_to_target_id_ref_table = dict(target_name_to_target_id_df[[target_name_col, target_id_col]].values)
    return (label_df, label_id_to_target_name, target_name_to_target_id_ref_table)


def write_to_file(output_df, output_file, tsv=None):
    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(cur_dir_path, OUTPUT_DIR)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if tsv:
        out_file_name = ''.join([output_file, str(int(time.time())), '.csv'])
        output_file = os.path.join(output_dir, out_file_name)

        output_df.to_csv(os.path.join(output_dir, out_file_name), index=False, sep='\t')
    else:
        out_file_name = ''.join([output_file, str(int(time.time())), '.xlsx'])
        output_file = os.path.join(output_dir, out_file_name)
        writer = pd.ExcelWriter(output_file)
        output_df.to_excel(writer, index=False)
        writer.save()
    print('Finished guessing the mappings. Results written to', output_file)


def prepare_row_content(pd_row, raw_col_names, final_col_names,
                        predicted_target_name, predicted_target_id,
                        target_name_col, target_id_col,
                        apac_flag):
    # TODO: this method can be removed when we finished merging APAC to main ETL flow
    row_headers = pd_row.to_dict().keys()
    vals_of_interest = [pd_row[c] if c in row_headers else '' for c in raw_col_names]
    vals_with_final_col_names = dict(zip(final_col_names, vals_of_interest))
    vals_with_final_col_names[target_name_col] = predicted_target_name
    vals_with_final_col_names[target_id_col] = predicted_target_id

    if apac_flag:
        vals_with_final_col_names['Included'] = '2' if pd_row.SOS_PRODUCT else '1'
        vals_with_final_col_names['ExceptionStatus'] = 'New'
        vals_with_final_col_names['Comments'] = 'mapped by Multinomial Naive Bayes algorithm'
    else:
        # this is for non-APAC countries
        vals_with_final_col_names['MAPPING_PROCESS_TYPE'] = 'New_Product_Mapping'
        vals_with_final_col_names['LAST_MAPPED_BY'] = 'mapped by Multinomial Naive Bayes algorithm'

    return vals_with_final_col_names


def write_model(model, file_name):
    joblib.dump(model, file_name)
    print("Writing model to this file:", file_name)


def load_model(file_name):
    print("Loading model from this file:", file_name)
    return joblib.load(file_name)

