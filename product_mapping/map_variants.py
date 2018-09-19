from mapping_utils import *
from queries import mapped_variants_q

DESC = '''
This program guesses variant names column based on multinomial naive bayes approach.
To find out how to run, use '-h' flag. Usage example:
>> python map_variants.py -i <file_that_has_subcategories_mapped.csv> -c "UNITED STATES"
'''

FEATURE_COLUMNS = ['GM_ADVERTISER_NAME', 'GM_SECTOR_NAME', 'GM_SUBSECTOR_NAME',
                   'GM_CATEGORY_NAME', 'GM_BRAND_NAME', 'GM_PRODUCT_NAME',
                   #'CP_CATEGORY_NAME',
                   'CP_SUBCATEGORY_NAME', 'CP_BRAND_NAME',
                   # 'CP_SUBBRAND_NAME'
                   ]
TARGET_NAME_COLUMN = 'CP_VARIANT_NAME'
TARGET_ID_COLUMN = 'CP_VARIANT_ID_1PH'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-c', # TODO: remove this when we have migrated and merged the APAC process with the primary flow
                        required=True,
                        type=str,
                        help="(Required) Enter the FULL name of the country as seen under [GM_COUNTRY_NAME] column in "
                             "the GM_CP_MASTER_PRODUCT_MAPPING table. E.g., python map_subcategories.py -c \"UNITED STATES\"")
    parser.add_argument('-t',
                        required=False,
                        type=str,
                        help="(Optional) Set this flag to '1' if the output file should be in TSV format. Default is xlsx.")
    parser.add_argument('-i',
                        required=True,
                        type=str,
                        help="(Required) Enter the FULL name of the input file, which must be placed in the folder "
                             "named 'input' and must contain data with mapped subcategories. "
                             "E.g., python map_variants.py -i mapped_subcats.csv")
    args = parser.parse_args()

    apac_country = False
    if args.c in APAC_COUNTRIES: # TODO: remove this when we have migrated all APAC countries into main database
        apac_country = True

    cur_dir_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(cur_dir_path, OUTPUT_DIR)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print('Loading mapped variant names from remote database using query:', mapped_variants_q)
    mapped_variants_df = get_dataframe_from_query(mapped_variants_q)

    print('Loading unmapped variants for', args.c, 'from local file named:', args.i)
    input_file = os.path.join(cur_dir_path, INPUT_DIR, args.i)
    if input_file.lower().endswith('.csv'):
        unmapped_variants_df = pd.read_csv(input_file , dtype=str, sep=',')
    else:
        unmapped_variants_df = pd.read_excel(input_file)

    print('Concatenating and cleaning column data starts:', time.asctime())
    df_x = (mapped_variants_df['GM_ADVERTISER_NAME'].astype('str').apply(tokenize)
            + mapped_variants_df['GM_SECTOR_NAME'].astype('str').apply(tokenize)
            + mapped_variants_df['GM_SUBSECTOR_NAME'].astype('str').apply(tokenize)
            + mapped_variants_df['GM_CATEGORY_NAME'].astype('str').apply(tokenize)
            + mapped_variants_df['GM_BRAND_NAME'].astype('str').apply(tokenize)
            + mapped_variants_df['GM_PRODUCT_NAME'].astype('str').apply(tokenize)
            # + mapped_variants_df['CP_CATEGORY_NAME'].astype('str').apply(tokenize) # we don't use that because it is inferred from cp_subcat
            + mapped_variants_df['CP_SUBCATEGORY_NAME'].astype('str').apply(tokenize)
            + mapped_variants_df['CP_BRAND_NAME'].astype('str').apply(tokenize)
            # we have 'subbrand' in the training set, but in the template that our team is using to feed as input, we don't have that
            + mapped_variants_df['CP_SUBBRAND_NAME'].astype('str').apply(tokenize))\
        .apply(' '.join)
    print('Concatenating and cleaning column data ends:', time.asctime())

    label_df, label_id_to_variant_name, variant_name_to_variant_id_ref_table = prepare_label_data(mapped_variants_df,
                                                                                                  TARGET_NAME_COLUMN,
                                                                                                  TARGET_ID_COLUMN)
    tfidf_vectorizer = TfidfVectorizer(
        sublinear_tf=True,  # TODO: we can remove this if log scale doesn't work out
        min_df=1,
        norm='l2', # L2 norm
        encoding='utf-8',
        ngram_range=(1, 2),
        stop_words='english'
    )
    model = fit_linear_svc_model(tfidf_vectorizer.fit_transform(df_x), label_df[[LABEL_ID_COLUMN]])

    raw_col_names = RAW_COLUMN_NAMES_FOR_APAC if apac_country else COLUMN_NAMES_FOR_ALL_OTHERS
    final_col_names = FINAL_COLUMN_NAMES_FOR_APAC if apac_country else COLUMN_NAMES_FOR_ALL_OTHERS # all other shares the same keys and vals
    mapped_df = pd.DataFrame(columns=final_col_names, index=None)
    for idx, row in unmapped_variants_df.iterrows():
        input_str = combine_feature_columns_to_one_long_str(row, FEATURE_COLUMNS)
        predicted_variant_name = predict_using_svc(input_str,
                                                   model,
                                                   tfidf_vectorizer,
                                                   label_id_to_variant_name)
        row_headers = row.to_dict().keys()
        vals_of_interest = [row[c] if c in row_headers else '' for c in raw_col_names]
        vals_with_adjusted_col_names = dict(zip(final_col_names, vals_of_interest))

        if apac_country:
            # TODO: remove this silly stuff as soon as Jholman merged APAC system to our main DB
            vals_with_adjusted_col_names['Included'] = '2' if row.SOS_PRODUCT else '1'
            vals_with_adjusted_col_names['Global_Subcategory ID'] = variant_name_to_variant_id_ref_table[predicted_variant_name]
            vals_with_adjusted_col_names['Global_Subcategory Name'] = predicted_variant_name
            vals_with_adjusted_col_names['ExceptionStatus'] = 'New'
            vals_with_adjusted_col_names['Comments'] = 'mapped by Multinomial Naive Bayes algorithm'
        else:
            # this is for non-APAC countries
            vals_with_adjusted_col_names['MAPPING_PROCESS_TYPE'] = 'New_Product_Mapping'
            vals_with_adjusted_col_names[TARGET_ID_COLUMN] = variant_name_to_variant_id_ref_table[predicted_variant_name]
            vals_with_adjusted_col_names[TARGET_NAME_COLUMN] = predicted_variant_name
            vals_with_adjusted_col_names['LAST_MAPPED_BY'] = 'mapped by Multinomial Naive Bayes algorithm'

        mapped_df.loc[len(mapped_df)] = vals_with_adjusted_col_names

    write_to_file(mapped_df, 'mapped_variants_', args.t)
